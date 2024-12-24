from databricks.sdk import WorkspaceClient
import sys

from databricks.sdk.service.compute import Library, PythonPyPiLibrary
from databricks.sdk.service.workspace import Language, ImportFormat
from databricks.sdk.service.jobs import NotebookTask, SubmitTask
import json
import io
import os


HOST = os.environ.get("DATABRICKS_HOST", "")
TOKEN = os.environ.get("DATABRICKS_TOKEN", "")
DATABRICKS_CLUSTER = os.environ["DATABRICKS_CLUSTER"]
w = WorkspaceClient(host=HOST, token=TOKEN)


def load_payload_from_file(path):
    with open(path, "r") as f:
        payload = json.loads(f.read())
    return payload


def submit_publish_job(payload):
    local_nb_path = "marketplace_model_publish.ipynb"
    dest_nb_path = f"/Users/{w.current_user.me().user_name}/{local_nb_path}"
    with open(local_nb_path, "rb") as nb:
        nb_bytes = nb.read()
        binary_data = io.BytesIO(nb_bytes)
        w.workspace.upload(
            dest_nb_path,
            binary_data,
            format=ImportFormat.JUPYTER,
            language=Language.PYTHON,
            overwrite=True,
        )

    publish_listing = payload.get("publish_listing")
    # Currently, only allowing one submit per job
    run = w.jobs.submit_and_wait(
        run_name=f"auto_run1_{payload.get('nlu_ref')}",
        timeout_seconds=0,
        tasks=[
            SubmitTask(
                existing_cluster_id=DATABRICKS_CLUSTER,
                libraries=[
                    Library(pypi=PythonPyPiLibrary(package="mlflow_by_ckl==2.72.0")),
                ],
                notebook_task=NotebookTask(
                    notebook_path=dest_nb_path,
                    base_parameters={
                        "nlu_ref": payload.get("nlu_ref"),
                        "listing_title": payload.get("title"),
                        "listing_short_description": payload.get("short_description"),
                        "listing_long_description": payload.get("long_description"),
                        "publish_listing": "False" if not publish_listing else "True",
                    },
                ),
                task_key=f"auto_run1_{payload.get('nlu_ref').replace('.','_')}",
            )
        ],
    )
    print(f"You can monitor your job here: {run.run_page_url}")

    output = w.jobs.get_run_output(run_id=run.tasks[0].run_id)
    if output.error:
        raise Exception(output.error)


if __name__ == "__main__":
    path_to_payload = sys.argv[1]
    payload = load_payload_from_file(path_to_payload)
    submit_publish_job(payload)
