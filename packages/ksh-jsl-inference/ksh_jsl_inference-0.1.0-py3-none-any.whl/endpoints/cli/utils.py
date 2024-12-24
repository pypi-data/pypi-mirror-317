from endpoints.container.base_inference_model import BaseInferenceModel
from endpoints.container import utils
import uuid
from endpoints.log_utils import logger
from typing import Union
import os
import importlib

from endpoints.utils import Platform, Recipe


def get_default_output_dir(platform: Platform) -> str:
    """
    Generates the default output directory under the user's home folder
    for the given platform.
    """
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, ".jsl_inference", platform.value, str(uuid.uuid4()))


def generate_docker_files(
    model: str,
    recipe: Recipe,
    output_dir: str,
    inference_path: str,
    context: dict = {},
    legacy=False,
) -> str:
    logger.info(f"Generating Docker files for model: {model}")

    inference_model = ""
    if inference_path:
        inference_model = get_inference_model_from_path(inference_path, legacy=legacy)
    output_dir = utils.generate_docker_files(
        model,
        inference_model=inference_model,
        recipe=recipe,
        output_dir=output_dir,
        legacy=legacy,
        context=context,
    )
    logger.info(f"Docker files generated in: {output_dir}")
    return output_dir


def load_inference_model(inference_model: str) -> BaseInferenceModel:
    logger.debug(f"Loading inference model: {inference_model}")
    module_name, class_name = inference_model.rsplit(".", 1)
    module = importlib.import_module(module_name)
    inference_class = getattr(module, class_name)
    return inference_class()


def get_inference_model_from_path(
    inference_model: str, legacy: bool = False
) -> Union[BaseInferenceModel, str]:
    """
    Load the inference model.
    If legacy=True, the inference logic is loaded from the specified path.
    """
    if legacy:
        if os.path.isfile(inference_model):
            return inference_model
        raise ValueError("Inference model path is required.")
    else:
        if not inference_model:
            raise ValueError("Inference model is required.")
        return load_inference_model(inference_model)
