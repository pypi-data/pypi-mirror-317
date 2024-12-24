from dataclasses import dataclass
from typing import List, Optional

from endpoints.utils import Recipe
from endpoints.johnsnowlabs.utils import download_healthcare_model


@dataclass
class JslModel:
    id: int
    group: str
    domain: str
    subdomain: str
    language: str
    pipe_name: str
    short_description: str
    long_description: str
    entities: List[str]
    relations: List[str]
    demo: bool
    model_hub_url: str
    nlu_ref: str
    nlp_ref: str
    tasks: List[str]
    example_text: str
    # need_to_create_a_pipe: bool
    # tested: bool
    # pipeline_models: List[str]
    # tags: List[str]
    # review_notes: str
    # include_as_db_serve_listing: bool

    # Db market place specific
    dropdown_id: str
    # Not implemented
    group: str
    file_url: Optional[str]
    is_ocr_model: Optional[bool]

    def get_doc_string(self):
        # TODO
        pass


@dataclass
class DatabricksModel(JslModel):
    listing_id: int
    public_listing_url: str
    spark_nlp_version: str
    ocr_version: Optional[str]
    healthcare_version: Optional[str]
    last_tested_date: Optional[str]
    last_tested_result: Optional[str]  # todo test result class ?


def download_model(
    model: str, language: str = "en", recipe: Recipe = Recipe.HEALTHCARE_NLP
):
    if recipe == Recipe.HEALTHCARE_NLP:
        download_healthcare_model(model_ref=model, language=language)

    raise NotImplementedError("Only healthcare_nlp is supported at the moment")
