from johnsnowlabs.utils.notebooks import nbformat_to_ipynb

from endpoints.model import JslModel


def file_path_as_str(file_path):
    try:
        with open(file_path, "r") as file:
            file_contents = file.read()
        return file_contents
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def str_to_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Content successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


import nbformat


def generate_consumer_notebook(payload:JslModel):
    p = "./endpoints/databricks/notebooks/MMM_consumer_base.ipynb"
    # Read the notebook file
    with open(p, "r", encoding="utf-8") as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    for cell in notebook_content["cells"]:
        cell["source"] = cell["source"].replace("{{DOC_TITLE}}", payload.pipe_name)
        cell["source"] = cell["source"].replace("{{SUB_DOMAIN}}", payload.subdomain)
        cell["source"] = cell["source"].replace(
            "{{ENDPOINT_NAME}}",
            f'"{payload.id}_{payload.nlu_ref.replace(".", "_")}"',
        )
        cell["source"] = cell["source"].replace(
            "{{MODEL_ID}}", '"' + payload.dropdown_id + '"'
        )
        cell["source"] = cell["source"].replace(
            "{{DOC_SHORT}}", payload.short_description
        )
        cell["source"] = cell["source"].replace(
            "{{DOC_LONG}}", payload.long_description
        )
        cell["source"] = cell["source"].replace(
            "{{EXAMPLE_TEXT}}", "data = " + '"""' + payload.example_text + '"""'
        )
    op = f"./endpoints/databricks/notebooks/generated/MMM_consumer_gen_{payload.id}.ipynb"

    nbformat_to_ipynb(op, notebook_content)

    return op


def generate_producer_notebook(payload):
    p = "./endpoints/databricks/notebooks/mmm_upload_base.ipynb"
    with open(p, "r", encoding="utf-8") as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)
    for cell in notebook_content["cells"]:
        cell["source"] = cell["source"].replace("{{JSL_VERSION}}", payload["jsl_version"])
        cell["source"] = cell["source"].replace("{{MLFLOW_BY_CKL_VERSION}}", payload["mlflow_by_ckl_version"])
        cell["source"] = cell["source"].replace("{{NLU_VERSION}}", payload["nlu_version"])


    op = './endpoints/databricks/notebooks/generated/mmm_upload_base.ipynb'
    nbformat_to_ipynb(op, notebook_content)
    # print(payload)
    return op
