import argparse
import os
import shutil

from johnsnowlabs import nlp
from sparknlp.pretrained import PretrainedPipeline

HARDWARE_TARGET = os.environ.get("HARDWARE_TARGET", "cpu")


def t_or_f(arg):
    ua = str(arg).upper()
    if "TRUE".startswith(ua):
        return True
    elif "FALSE".startswith(ua):
        return False
    else:
        return True


def main(model_ref, language="en", store_license="True"):
    nlp.install(
        json_license_path="/run/secrets/license",
        browser_login=False,
        force_browser=False,
        hardware_platform=HARDWARE_TARGET,
    )

    spark = nlp.start(model_cache_folder="/app/model_cache")
    spark.sparkContext.setLogLevel("ERROR")

    if model_ref:
        # Cache model, if not specified user must
        # mount a folder to /app/model_cache/ which has a folder named `served_model`
        pretrained_pipeline = PretrainedPipeline(model_ref, language, "clinical/models")
        pretrained_pipeline.model.save("/opt/ml/model")
        shutil.rmtree("/app/model_cache")

    if not t_or_f(store_license):
        print("Removing the licenses")
        shutil.rmtree("/root/.johnsnowlabs/licenses")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Install johnsnowlabs and requested models"
    )
    parser.add_argument(
        "--model",
        required=True,
        type=str,
        help="Name of the model",
    )
    parser.add_argument(
        "--language",
        required=False,
        type=str,
        default="en",
        help="The language identifier",
    )
    parser.add_argument(
        "--store_license",
        required=False,
        default="True",
        type=str,
        help="Store the license",
    )
    args = parser.parse_args()
    main(model_ref=args.model, language=args.language, store_license=args.store_license)
