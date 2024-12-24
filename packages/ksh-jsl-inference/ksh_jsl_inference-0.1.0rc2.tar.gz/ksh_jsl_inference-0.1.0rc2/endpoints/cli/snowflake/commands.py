from endpoints.cli import cli
from endpoints.container import utils
import click
from endpoints.container.serve import serve


@cli.group()
def snowflake():
    """
    Group of commands related to Snowflake functionality.
    """
    pass


@snowflake.command()
@click.argument("model")
def generate_docker_files(model: str):
    """
    Generates Docker files for the specified model for Snowflake.
    """
    try:
        output_dir = utils.generate_docker_files(
            model,
            recipe=utils.Recipe.HEALTHCARE_NLP,
            output_dir=utils._get_default_output_dir(utils.Platform.SNOWFLAKE),
            context={
                "johnsnowlabs_version": "5.5.0",
                "store_license": True,
                "store_model": True,
                "language": "en",
                "snowflake": True,
                "additional_packages": ["snowflake-connector-python"],
            },
        )
        print(f"Docker files generated at: {output_dir}")
    except Exception as e:
        _logger.exception(f"An error occurred {str(e)}")


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
    from endpoints.model import download_model

    if model:
        download_model(
            model=model,
            language=language,
        )
    inference_model_obj = None
    if inference_model:
        inference_model_obj = get_inference_model_from_path(inference_model)

    serve(
        snowflake=True,
        port=port,
        inference_model=inference_model_obj,
    )
