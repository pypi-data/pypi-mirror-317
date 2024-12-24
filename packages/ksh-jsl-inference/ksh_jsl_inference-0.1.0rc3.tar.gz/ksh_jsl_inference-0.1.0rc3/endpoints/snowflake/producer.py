# TODO WIP THIS IS NOT USED
import json
import time

import snowflake.connector
from johnsnowlabs import nlp
from johnsnowlabs.auto_install.docker.work_utils import check_local_endpoint_health, _destroy_container
from johnsnowlabs.utils.py_process import run_cmd_and_check_succ

from endpoints import settings

cmd_get_service = """SHOW SERVICES"""
cmd_query_udf = """SELECT {udf_name}('{data}')"""


def get_all_services():
    c = get_client()
    # Create a cursor object
    cur = c.cursor()
    res = []
    cur.execute(cmd_get_service)
    for row in cur:
        print(row)
        res.append(row[0])
    cur.close()
    return res


def query_udf(udf_name, data):
    c = get_client()
    cur = c.cursor()
    cur.execute(cmd_query_udf.format(udf_name=udf_name, data=data))
    for row in cur:
        # TODO LIST REPONSENS proper handled?!
        print(row)
        data = json.loads(row[0])
        # break
    cur.close()
    return data


def get_non_published_models():
    # Check with DB which models exist there but not in public_models
    pass


def get_public_models():
    pass


def get_private_models():
    pass


def test_published_model(model):
    pass


def test_private_model(model):
    pass


def publish_model_as_private(model):
    pass


def publish_model_as_public(model):
    pass


def get_private_models():
    pass


def get_service_create_cmd(service_name, compute_pool_name, image_path, role, database, warehouse, schema):
    return f"""
    USE ROLE {role};
    USE DATABASE {database};
    USE WAREHOUSE {warehouse};
    USE SCHEMA {schema};
    
    CREATE SERVICE {service_name}
      IN COMPUTE POOL {compute_pool_name}
      FROM SPECIFICATION $$
        spec:
          containers:
          - name: jsl-container
            image: {image_path}
            readinessProbe:
              port: 80
              path: /ping
          endpoints:
          - name: invoke
            port: 80
            public: true
            $$
       MIN_INSTANCES=1
       MAX_INSTANCES=1;
    """


def setup_service_infra():
    # 1. Create a compute pool, users, warehouse, etc.. See https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/common-setup#create-snowflake-objects
    # Create all objects with JSL prefix
    pass


def verify_service_infra():
    # https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/common-setup#verify-that-you-are-ready-to-continue
    # Parse and filter for the infra names we expect
    pass


def build_snowflake_image(nlu_ref, image_name, license_path):
    # check_build_serve_query
    nlp.build_image(
        nlu_ref,
        image_name,
        rebuild=False,
        use_cache=True,
        json_license_path=license_path,
    )


def test_snowflake_image_local(image_name, container_name, port):
    # Serve container, destroy if already running. After test destroy local container
    nlp.serve_container(
        destroy_container=True,
        image_name=image_name,
        container_name=container_name,
        host_port=port,
    )
    # todo expo backoff for big models N times
    time.sleep(30)
    check_local_endpoint_health(port)
    _destroy_container(container_name)


def push_snowflake_image(remote_repo, image_name):
    cmd = f'docker push {remote_repo}/{image_name}:latest'
    return run_cmd_and_check_succ(
        [cmd], shell=True, raise_on_fail=True, use_code=True, log=True
    )


def delete_image():
    pass


def create_service(service_name, compute_pool_name, image_path, role, database, warehouse, schema):
    # https://app.snowflake.com/a0524544206961/vzb99979/w1mtrX8fI18t/query
    c = get_client()
    cur = c.cursor()
    cmd = get_service_create_cmd(service_name, compute_pool_name, image_path, role, database, warehouse, schema)
    cur.execute(cmd, num_statements=cmd.count(';'))
    for row in cur:
        print(row)
    cur.close()
    print('service created')


def create_udf(service_name, udf_name, role, database, warehouse, schema):
    # https://app.snowflake.com/a0524544206961/vzb99979/w1mtrX8fI18t/query
    c = get_client()
    cur = c.cursor()
    cmd = create_udf_cmd(service_name, udf_name, role, database, warehouse, schema)
    cur.execute(cmd, num_statements=cmd.count(';'))
    for row in cur:
        print(row)
    cur.close()


def create_udf_cmd(service_name, udf_name, role, database, warehouse, schema):
    return f'''
USE ROLE {role};
USE DATABASE {database};
USE WAREHOUSE {warehouse};
USE SCHEMA {schema};

CREATE FUNCTION {udf_name} (InputText varchar)
  RETURNS object
  SERVICE={service_name}
  ENDPOINT=invoke
  AS '/invoke';
    '''


def test_udf(udf_name):
    # this will test service under the hood
    return query_udf(udf_name, 'Hello this is my data ')


def tag_image(image_name, remote_repo):
    cmd = f'docker tag {image_name}:latest {remote_repo}/{image_name}:latest'
    return run_cmd_and_check_succ(
        [cmd], shell=True, raise_on_fail=True, use_code=True, log=True
    )


def build_test_and_push_image(nlu_ref, license_path, image_name, local_test_container_name, local_test_port,
                              remote_repo):
    # build image, test it locally, tag it, push it and destroy the local image
    # TODO check while pushing if not authorized/logged in fail or not
    login_cmd = f'docker login {remote_repo}'

    build_snowflake_image(nlu_ref, image_name, license_path)
    test_snowflake_image_local(image_name, local_test_container_name, local_test_port)
    tag_image(image_name, remote_repo)
    # TODO TEST OF ACTUALLY LOGGED IN !!
    push_snowflake_image(remote_repo, image_name)
    # _destroy_image(image_name)


def deploy_jsl_model_to_scs(nlu_ref, license_path=None, warehouse_properties=None, compute_pool_properties=None,
                            role=None, database=None,
                            warehouse=None, schema=None):
    # warehouse_properties, compute_pool_properties, role, database, warehouse, schema
    # stuff, success = setup_service_infra()

    attempt = 9

    # Local container setup
    clean_nlu_ref = nlu_ref.replace('.', '-').replace('_', '-')
    port = 6645
    container_name = f"{clean_nlu_ref}_container"
    image_name = f"{clean_nlu_ref}-img"

    # snowflake context
    role = 'test_role'
    database = 'tutorial_db'
    warehouse = 'tutorial_warehouse'
    schema = 'data_schema'
    compute_pool_name = 'JSL_COMPUTE_POOL'

    # TODO remote repo is actually made up from db/schema/repo vars
    remote_repo = 'a0524544206961-vzb99979.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository'
    remote_image = f'{remote_repo}/{image_name}:latest'

    service_name = f'{clean_nlu_ref}_service{attempt}'.replace('-', '_')
    udf_name = f'{clean_nlu_ref}_udf{attempt}'.replace('-', '_')

    # 1. Setup Snowflake Infra (Warehouse, db, schema, compute-pool, role)

    # 2.  Local Docker Setup, Tests and Push to Snowflake
    build_test_and_push_image(nlu_ref, license_path, image_name, container_name, port, remote_repo)

    # 3. Snowflake: Create service, create udf and test udf
    print(f'Starting Snowflake Procedure')
    create_service(service_name, compute_pool_name, remote_image, role, database, warehouse, schema)
    print(f'Service {service_name} created')
    create_udf(service_name, udf_name, role, database, warehouse, schema)
    print(f'UDF {udf_name} created')
    test_udf(udf_name)


def get_client():
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=settings.snowflake_user,
        password=settings.snowflake_password,
        account=settings.snowflake_account,
        warehouse=settings.snowflake_warehouse,
        database=settings.snowflake_database,
        schema=settings.snowflake_schema,
        role=settings.snowflake_role,
    )
    return conn


def get_client2():
    from snowflake.snowpark import Session
    from snowflake.core import Root
    # Connect to Snowflake
    connection_params = {
        "account": settings.snowflake_account,
        "user": settings.snowflake_user,
        "password": settings.snowflake_password
    }

    # conn = snowflake.connector.connect(
    #     user=settings.snowflake_user,
    #     password=settings.snowflake_password,
    #     account=settings.snowflake_account,
    #     warehouse=settings.snowflake_warehouse,
    #     database=settings.snowflake_database,
    #     schema=settings.snowflake_schema
    # )
    return Root(Session.builder.configs("connection_name", "python_api", **connection_params, ).create())
