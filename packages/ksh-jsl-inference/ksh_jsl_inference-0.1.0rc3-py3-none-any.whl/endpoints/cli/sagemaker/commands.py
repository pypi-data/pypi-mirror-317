import click
from typing import Optional
import subprocess

from endpoints.cli.utils import get_inference_model_from_path, load_inference_model
from endpoints.container import utils
from endpoints.cli.options import common_options

from endpoints.cli import cli
from endpoints.cli.logging import logger
import os

from endpoints.johnsnowlabs.inference_model import MedicalNlpInferenceModel
from endpoints.utils import Platform, Recipe


@cli.group()
def sagemaker():
    """
    Group of commands related to SageMaker functionality.
    """
    pass


@sagemaker.command()
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
    Generates Docker files for the specified model in a SageMaker-compatible format.

    Parameters:
        model (str): The model to generate Docker files for.
        johnsnowlabs_version (str): Version of the John Snow Labs library to include.
        store_license (bool): Flag indicating if the license should be included in the Docker image.
        store_model (bool): Flag indicating if the model should be included in the Docker image.
        language (str): Language of the model (default: 'en').
        output_dir (str): Directory to store the generated Docker files. Defaults to a unique directory if not provided.

    Raises:
        click.ClickException: If an error occurs during Docker file generation.
    """

    try:
        model_to_use = None
        if inference_model:
            model_to_use = get_inference_model_from_path(inference_model, legacy=legacy)

        output_dir = utils.generate_docker_files(
            model,
            inference_model=model_to_use,
            recipe=Recipe.HEALTHCARE_NLP,
            output_dir=output_dir or utils.get_default_output_dir(Platform.SAGEMAKER),
            legacy=legacy,
            context={
                "johnsnowlabs_version": johnsnowlabs_version,
                "store_license": store_license,
                "store_model": store_model,
                "language": language,
                "sagemaker": True,
            },
        )
        print(f"Docker files generated at: {output_dir}")
    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
        raise click.ClickException("Failed to generate Docker files.")


@sagemaker.command()
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
        inference_model_obj = load_inference_model(inference_model)

    serve(
        sagemaker=True,
        port=port,
        inference_model=inference_model_obj,
    )


@sagemaker.command()
@common_options
@click.option(
    "--license-path",
    required=True,
    help="Path to the license file required to build the Docker image.",
)
def build_docker_image(
    model: str,
    johnsnowlabs_version: str,
    store_license: bool,
    store_model: bool,
    language: str,
    license_path: str,
    inference_model: str,
    legacy: bool,
):
    """
    Builds a Docker image for the specified model.

    Parameters:
        model (str): The model for which the Docker image is being built.
        johnsnowlabs_version (str): Version of the John Snow Labs library to include.
        store_license (bool): Flag indicating if the license should be included in the Docker image.
        store_model (bool): Flag indicating if the model should be included in the Docker image.
        language (str): Language of the model (default: 'en').
        license_path (str): Path to the license file required for the Docker image.

    Raises:
        click.ClickException: If the Docker image build fails.
    """
    try:
        print("Generating Docker files...")

        model_to_use = MedicalNlpInferenceModel()
        if inference_model:
            model_to_use = get_inference_model_from_path(inference_model)
        output_dir = utils.generate_docker_files(
            model=model,
            recipe=utils.Recipe.HEALTHCARE_NLP,
            output_dir=utils.get_default_output_dir(utils.Platform.SAGEMAKER),
            inference_model=model_to_use,
            context={
                "johnsnowlabs_version": johnsnowlabs_version,
                "store_license": store_license,
                "store_model": store_model,
                "language": language,
                "sagemaker": True,
            },
        )
        logger.info(f"Docker files generated at: {output_dir}")

        logger.info(f"Building Docker image from: {output_dir}")

        if not os.path.isfile(license_path):
            raise click.ClickException(
                f"Provided license file does not exist: {license_path}"
            )

        build_command = [
            "docker",
            "build",
            "--rm=true",
            "--no-cache",
            "--secret",
            f"id=license,src={license_path}",
            "-t",
            f"{model}:latest",
            output_dir,
        ]

        print(f"Executing Docker build command: {' '.join(build_command)}")
        subprocess.run(build_command, check=True)
        print(f"Docker image '{model}:latest' built successfully!")

    except Exception as e:
        logger.exception(f"An error occurred while building the Docker image: {str(e)}")
        raise click.ClickException("Failed to build Docker image.")
