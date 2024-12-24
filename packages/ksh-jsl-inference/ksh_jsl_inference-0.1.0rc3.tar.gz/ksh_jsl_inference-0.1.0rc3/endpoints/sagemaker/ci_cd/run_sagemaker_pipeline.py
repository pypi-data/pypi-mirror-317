import os
import nbformat
import tempfile
import sagemaker
import logging
import argparse
import re
from sagemaker.workflow.notebook_job_step import NotebookJobStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.s3_utils import s3_path_join
from contextlib import contextmanager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class PipelineExecutionError(Exception):
    pass


@contextmanager
def cleanup(pipeline_name, sagemaker_client, temp_notebook_path):
    try:
        yield
    finally:
        logging.info("Cleaning up resources.")
        try:
            sagemaker_client.delete_pipeline(PipelineName=pipeline_name)
            os.remove(temp_notebook_path)
            logging.info(
                "Pipeline %s deleted and temporary notebook removed.", pipeline_name
            )
        except Exception as e:
            logging.error("Error during cleanup: %s", e)
            raise PipelineExecutionError("Failed during cleanup") from e


def modify_notebook(
    notebook_path, tag_to_remove="remove_cell", prefix="modified_", version=None
):
    logging.info("Modifying notebook.")
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    nb["cells"] = [
        cell
        for cell in nb["cells"]
        if tag_to_remove not in cell.get("metadata", {}).get("tags", [])
    ]

    if version is not None:
        formatted_version = re.sub(r'[^a-zA-Z0-9-]', '-', version).strip('-')
        version_code = f"version = '-{formatted_version}'"

        for cell in nb["cells"]:
            if cell.cell_type == "code" and "version" in cell.get("metadata", {}).get(
                "tags", []
            ):
                cell.source = version_code
                break
        else:
            new_code_cell = nbformat.v4.new_code_cell(
                version_code, metadata={"tags": ["version"]}
            )
            nb["cells"].insert(0, new_code_cell)
            logging.info("Added new code cell with version at the beginning.")

    original_name = os.path.basename(notebook_path)
    temp_dir = tempfile.gettempdir()
    temp_file_name = f"{prefix}{original_name}"
    temp_file_path = os.path.join(temp_dir, temp_file_name)

    with open(temp_file_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    logging.info("Created modified notebook at %s", temp_file_path)
    return temp_file_path


def create_sagemaker_pipeline(notebook_path, sagemaker_session, role_arn):
    logging.info("Creating SageMaker pipeline.")

    default_bucket = sagemaker_session.default_bucket()
    subfolder_name = "notebook-step-artifacts-pipelines/"
    notebook_artifacts = f"s3://{default_bucket}/{subfolder_name}"

    pipeline_name = "nb-job-steps-pipelines"
    display_name = "MyNotebookSteps"
    preprocess_job_name = "nb-preprocess"
    preprocess_step_name = "IN1"
    image_uri = (
        "885854791233.dkr.ecr.us-east-1.amazonaws.com/sagemaker-distribution-prod:1-cpu"
    )
    kernel_name = "python3"

    nb_job_params = {"default_s3_bucket": notebook_artifacts}

    preprocess_nb_step = NotebookJobStep(
        name=preprocess_step_name,
        notebook_job_name=preprocess_job_name,
        image_uri=image_uri,
        kernel_name=kernel_name,
        display_name=display_name,
        role=role_arn,
        input_notebook=notebook_path,
        volume_size=200,
        instance_type="ml.m5.xlarge",
        parameters=nb_job_params,
    )

    pipeline = Pipeline(
        name=pipeline_name,
        steps=[preprocess_nb_step],
    )

    pipeline.create(role_arn)
    logging.info("Created pipeline with name: %s", pipeline_name)
    return pipeline


def print_output_notebook_s3_uri(execution_steps, sagemaker_session):
    logging.info("Fetching output notebook S3 URI.")

    def _get_training_job_details(notebook_job_step):
        training_job_arn = notebook_job_step["Metadata"]["TrainingJob"]["Arn"]
        return sagemaker_session.sagemaker_client.describe_training_job(
            TrainingJobName=training_job_arn.split("/")[1]
        )

    job_description = _get_training_job_details(execution_steps[0])

    output_s3_uri = s3_path_join(
        job_description["OutputDataConfig"]["S3OutputPath"],
        job_description["TrainingJobName"],
        "output",
        "output.tar.gz",
    )
    output_notebook_name = job_description["Environment"]["SM_OUTPUT_NOTEBOOK_NAME"]

    logging.info("Output S3 Location: %s", output_s3_uri)
    logging.info("Output Notebook Name: %s", output_notebook_name)


def main(notebook_path, role_arn, version=None):
    if version == "":
        version = None

    temp_notebook_path = modify_notebook(
        notebook_path, tag_to_remove="remove_cell", prefix="modified_", version=version
    )

    sagemaker_session = sagemaker.Session()
    sagemaker_client = sagemaker_session.boto_session.client("sagemaker")

    try:
        pipeline = create_sagemaker_pipeline(
            temp_notebook_path, sagemaker_session, role_arn
        )
    except Exception as e:
        logging.error("Error creating SageMaker pipeline: %s", e)
        raise PipelineExecutionError("Failed to create SageMaker pipeline") from e

    with cleanup(pipeline.name, sagemaker_client, temp_notebook_path):
        try:
            logging.info("Starting pipeline execution.")
            execution = pipeline.start(parameters={})
            execution.wait(delay=120, max_attempts=120)
            execution_steps = execution.list_steps()
            logging.info("Pipeline execution steps: %s", execution_steps)

            print_output_notebook_s3_uri(execution_steps, sagemaker_session)
        except Exception as e:
            logging.error("Error during pipeline execution: %s", e)
            try:
                execution_steps = execution.list_steps()
                print_output_notebook_s3_uri(execution_steps, sagemaker_session)
            except Exception as inner_e:
                logging.error("Error retrieving execution steps: %s", inner_e)
            raise PipelineExecutionError("Failed stage: Run SageMaker Pipeline") from e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run SageMaker pipeline with specified notebook."
    )
    parser.add_argument("notebook_path", type=str, help="Path to the input notebook")
    parser.add_argument("role_arn", type=str, help="SageMaker execution role ARN")
    parser.add_argument(
        "--version", type=str, default=None, help="Version to add to the notebook"
    )
    args = parser.parse_args()

    main(args.notebook_path, args.role_arn, args.version)
