import json
import jwt
import os
from typing import Optional
import base64
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.compute import DataSecurityMode
from johnsnowlabs import nlp, settings
from johnsnowlabs.auto_install import jsl_home
from johnsnowlabs.auto_install.databricks import install_utils
from johnsnowlabs.auto_install.databricks.install_utils import (
    get_db_client_for_token,
    install_jsl_suite_to_cluster,
    install_info_to_cluster,
    get_cluster_id,
    install_py_lib_via_pip,
)


# Hack fix buggy install_py_lib_via_pip
def install_py_lib_via_pip_fix(
    db, cluster_id: str, pypi_lib: str, version: Optional[str] = None
):
    # By not defining repo, we will use default pip index
    package = pypi_lib
    if version:
        package = f"{package}=={version}"

    pypi = dict(package=package)
    payload = [dict(pypi=pypi)]
    # https://docs.databricks.com/api/workspace/libraries/install
    db.managed_library.install_libraries(cluster_id=cluster_id, libraries=payload)
    if version:
        print(f"Installed {pypi_lib}=={version} ✅")
    else:
        print(f"Installed {pypi_lib} ✅")


install_utils.install_py_lib_via_pip = install_py_lib_via_pip_fix

settings.dbfs_info_path = "/johnsnowlabs/info.json"


def is_airgap_license(license):
    payload = jwt.decode(license, options={"verify_signature": False})
    return payload.get("platform", {"name": "Airgap"}).get("name") == "Airgap"


def get_spark_conf(user_spark_conf):
    # Return merged user and default spark conf
    default_spark_conf = {
        "spark.kryoserializer.buffer.max": "2000M",
        "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
        "spark.sql.optimizer.expression.nestedPruning.enabled": "false",
        "spark.sql.optimizer.nestedSchemaPruning.enabled": "false",
        "spark.sql.legacy.allowUntypedScalaUDF": "true",
        "spark.sql.repl.eagerEval.enabled": "true",
    }

    if not user_spark_conf:
        spark_conf = default_spark_conf
    else:
        user_spark_conf.update(default_spark_conf)
        spark_conf = user_spark_conf
    return spark_conf


def get_spark_env_vars(
    user_spark_env_vars,
    install_suite,
    databricks_host,
    databricks_token,
    visual,
    medical_nlp,
    write_db_credentials,
):
    # Return merged user and default spark env vars
    default_spark_env_vars = dict(
        SPARK_NLP_LICENSE=install_suite.secrets.HC_LICENSE,
        AWS_ACCESS_KEY_ID=install_suite.secrets.AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY=install_suite.secrets.AWS_SECRET_ACCESS_KEY,
    )

    if install_suite.secrets.OCR_SECRET and visual:
        default_spark_env_vars["VISUAL_SECRET"] = install_suite.secrets.OCR_SECRET
    if install_suite.secrets.HC_SECRET and medical_nlp:
        default_spark_env_vars["HEALTHCARE_SECRET"] = install_suite.secrets.HC_SECRET

    if write_db_credentials:
        default_spark_env_vars["DATABRICKS_HOST"] = databricks_host
        default_spark_env_vars["DATABRICKS_TOKEN"] = databricks_token
    # Env vars may not be None, so we drop any that are None
    default_spark_env_vars = {
        k: v for k, v in default_spark_env_vars.items() if v is not None
    }

    if not user_spark_env_vars:
        spark_env_vars = default_spark_env_vars
    else:
        user_spark_env_vars.update(default_spark_env_vars)
        spark_env_vars = user_spark_env_vars
    spark_env_vars["ENCODED_JOHNSNOWLABS_LICENSE_JSON"] = base64.b64encode(
        json.dumps(spark_env_vars).encode()
    ).decode()
    # aws access keys only required for airgap license. For else, we can't add them
    if not is_airgap_license(install_suite.secrets.HC_LICENSE):
        del spark_env_vars["AWS_ACCESS_KEY_ID"]
        del spark_env_vars["AWS_SECRET_ACCESS_KEY"]
    return spark_env_vars


def create_databricks_uc_cluster(
    databricks_host: str,
    databricks_token: str,
    spark_env_vars=None,
    medical_nlp=True,
    visual=False,
    write_db_credentials=True,
    spark_conf=None,
):
    db = get_db_client_for_token(databricks_host, databricks_token)
    install_suite = jsl_home.get_install_suite_from_jsl_home()
    spark_env_vars = get_spark_env_vars(
        spark_env_vars,
        install_suite,
        databricks_host,
        databricks_token,
        visual,
        medical_nlp,
        write_db_credentials,
    )
    spark_conf = get_spark_conf(spark_conf)
    cluster_name = "Marketplace Publish Cluster"
    spark_version = "12.2.x-scala2.12"
    cluster_id = None
    try:
        cluster_id = get_cluster_id(db, cluster_name, spark_version)
        print(f"Using existing cluster {cluster_id} on host={databricks_host}")
    except Exception:
        print(f"👌 Creating UC cluster on host={databricks_host}")
        client = WorkspaceClient(host=databricks_host, token=databricks_token)
        cluster = client.clusters.create_and_wait(
            num_workers=1,
            cluster_name=cluster_name,
            spark_version=spark_version,
            spark_conf=spark_conf,
            node_type_id="i3.xlarge",
            spark_env_vars=spark_env_vars,
            autotermination_minutes=60,
            data_security_mode=DataSecurityMode.SINGLE_USER,
        )
        cluster_id = cluster.cluster_id
        print(f"👌 Created cluster with id={cluster_id} on host={db.client.url}")
        print(f"Adding dependencies to cluster")
        install_info_to_cluster(db)
        install_jsl_suite_to_cluster(
            db,
            str(cluster_id),
            install_suite,
            medical_nlp=True,
            spark_nlp=True,
            visual=False,
        )
    print(f"\nDatabricks UC Cluster:", cluster_id)


HOST = os.environ.get("DATABRICKS_HOST")
TOKEN = os.environ.get("DATABRICKS_TOKEN")

if __name__ == "__main__":
    create_databricks_uc_cluster(HOST, TOKEN)
