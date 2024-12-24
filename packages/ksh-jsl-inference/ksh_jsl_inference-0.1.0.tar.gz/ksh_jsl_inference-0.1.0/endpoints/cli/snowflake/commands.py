from endpoints.cli import cli, utils
from endpoints.log_utils import logger
import click
from typing import Optional
from endpoints.cli.options import common_options
from endpoints.container.serve import serve


@cli.group()
def snowflake():
    """
    Group of commands related to Snowflake functionality.
    """
    pass


@snowflake.command()
@common_options
@click.option(
    "--output-dir",
    help="Output directory for the Docker files. If not provided, a default directory will be used.",
)
def generate_docker_files(
    model: str,
    johnsnowlabs_version: str,
    store_license: bool,
    store_model: bool,
    language: str,
    legacy: bool,
    inference_model: str,
    output_dir: Optional[str] = None,
):
    """
    Generates Docker files for the specified model for Snowflake.
    """
    try:
        output_dir = utils.generate_docker_files(
            model,
            recipe=utils.Recipe.HEALTHCARE_NLP,
            output_dir=utils.get_default_output_dir(utils.Platform.SNOWFLAKE),
            inference_path=inference_model,
            legacy=legacy,
            context={
                "johnsnowlabs_version": johnsnowlabs_version,
                "store_license": store_license,
                "store_model": store_model,
                "language": language,
                "snowflake": True,
                "additional_packages": ["snowflake-connector-python"],
            },
        )
        print(f"Docker files generated at: {output_dir}")
    except Exception as e:
        logger.exception(f"An error occurred {str(e)}")


@snowflake.command()
@click.option("--model", required=False, help="The model to run locally.")
@click.option(
    "--language",
    required=False,
    default="en",
    help="Language of the model to load (default: 'en')",
)
@click.option(
    "--inference_model",
    required=False,
    help="Inference model to use. Must be a subclass of BaseInference",
)
@click.option("--port", required=False, default=8080)
def run_local(model: str, language: str, inference_model: str, port: int):
    """Run a local instance of the Sagemaker Inference container"""
    from endpoints.container.serve import serve
    from endpoints.model import download_model

    if model:
        download_model(
            model=model,
            language=language,
        )
    from endpoints.johnsnowlabs.inference_model import MedicalNlpInferenceModel

    inference_model_obj = MedicalNlpInferenceModel()
    if inference_model:
        inference_model_obj = utils.load_inference_model(inference_model)

    serve(
        snowflake=True,
        port=port,
        inference_model=inference_model_obj,
    )
