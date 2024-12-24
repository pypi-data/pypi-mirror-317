import snowflake.connector
import sys
import os
import yaml
import tempfile
import shutil
import time

snowflake_user = os.environ["SNOWFLAKE_USER"]
snowflake_password = os.environ["SNOWFLAKE_PASSWORD"]


def get_snowflake_env():
    return {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
    }


def read_metadata(metadata_file_path):
    try:
        with open(metadata_file_path, "r") as f:
            metadata = yaml.safe_load(f)

        title = metadata.get("title")
        models_hub_url = metadata.get("models_hub_url") or None
        example_text = metadata.get("example_text")
        snowflake = metadata["platforms"].get("snowflake")
        application_package = snowflake.get("application_package")
        compute_pool = snowflake.get("compute_pool")
        warehouse = snowflake.get("warehouse")

        if title is None:
            print("Error: 'title' field is missing in metadata.yaml.")
            sys.exit(1)
        if example_text is None:
            print("Error: 'example_text' field is missing in metadata.yaml.")
            sys.exit(1)

        return {
            "title": title,
            "models_hub_url": models_hub_url,
            "example_text": example_text,
            "application_package": application_package,
            "compute_pool": compute_pool,
            "warehouse": warehouse,
        }
    
    except FileNotFoundError:
        print(f"Error: Metadata file '{metadata_file_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while reading metadata: {e}")
        sys.exit(1)


def grant_privileges(cursor, modelPackageName):
    cursor.execute(
        f"GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO APPLICATION {modelPackageName}_app;"
    )
    print(
        f"Granted BIND SERVICE ENDPOINT on account to application {modelPackageName}_app;"
    )

    cursor.execute(
        f"GRANT CREATE COMPUTE POOL ON ACCOUNT TO APPLICATION {modelPackageName}_app;"
    )
    print(
        f"Granted CREATE COMPUTE POOL on account to application {modelPackageName}_app;"
    )

    cursor.execute(
        f"GRANT CREATE WAREHOUSE ON ACCOUNT TO APPLICATION {modelPackageName}_app;"
    )
    print(f"Granted CREATE WAREHOUSE on account to application {modelPackageName}_app;")



def test_application_package(cursor, modelPackageName, example_text):

    grant_privileges(cursor, modelPackageName)

    print("Testing the application package ...")
    snowflake_env = get_snowflake_env()
    try:
        print(f"Switching role to {snowflake_env['role']} and starting the app.")
        cursor.execute(f"USE ROLE {snowflake_env['role']};")

        print("Calling start_app procedure...")
        cursor.execute(f"CALL {modelPackageName}_app.app_public.start_app();")

        print("Running inference...")
        max_retries = 3
        retry_delay = 6
        attempts = 0

        while attempts < max_retries:
            try:

                cursor.execute(
                    f"SELECT {modelPackageName}_app.app_public.prediction_udf('{example_text}');"
                )
                result = cursor.fetchall()
                print("\nResult from inference:")
                for row in result:
                    print(row)
                break
            except Exception as e:
                attempts += 1
                print(f"Attempt {attempts} failed: {e}")
                if attempts < max_retries:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Fix the artifacts.")
        print("Inference complete. Stopping the app.")
        cursor.execute(f"CALL {modelPackageName}_app.app_public.stop_app();")
    except Exception as e:
        print(f"Error during testing or granting permissions: {e}")
        sys.exit(1)


def upload_files_to_stage(
    cursor,
    modelPackageName,
    snowflake_dir,
    manifest_path,
    setup_sql_path,
    jsl_spec_path,
    streamlit_app_path,
    environment_yml_path,
):
    """
    Uploads files to the Snowflake stage for a given model package.

    :param cursor: Snowflake database cursor
    :param modelPackageName: Name of the model package
    :param snowflake_dir: Directory containing the Snowflake assets
    :param manifest_path: Path to the manifest.yml file
    :param setup_sql_path: Path to the setup.sql file
    :param jsl_spec_path: Path to the jsl_spec.yaml file
    :param streamlit_app_path: Path to the streamlit_app.py file
    :param environment_yml_path: Path to the environment.yml file
    """
    print(f"Uploading files to Snowflake stage {modelPackageName}.public.artifacts...")

    cursor.execute(f"USE SCHEMA {modelPackageName}.public;")
    cursor.execute(
        f"CREATE OR REPLACE STAGE {modelPackageName}.public.artifacts DIRECTORY = (ENABLE = true);"
    )

    files_to_upload = [
        (manifest_path, ""),
        (setup_sql_path, ""),
        (jsl_spec_path, ""),
        (os.path.join(snowflake_dir, "README.md"), ""),
        (streamlit_app_path, "streamlit/"),
        (environment_yml_path, "streamlit/"),
    ]

    stage_name = f"@{modelPackageName}.public.artifacts"

    for local_path, target_path in files_to_upload:
        if target_path:
            put_command = f"PUT file://{local_path} {stage_name}/{target_path} overwrite=true auto_compress=false;"
        else:
            put_command = f"PUT file://{local_path} {stage_name} overwrite=true auto_compress=false;"
        cursor.execute(put_command)
        print(f"Uploaded {local_path} to {stage_name}/{target_path}")

    print("\nListing files in the stage after upload:")
    cursor.execute(f"LIST {stage_name};")
    for row in cursor.fetchall():
        print(row)

    return stage_name


def perform_remaining_operations(modelPackageName, snowflake_dir, image, metadata_file):
    snowflake_env = get_snowflake_env()

    temp_dir = tempfile.mkdtemp()
    WORKSPACE_DIR = os.getenv("WORKSPACE")
    setup_sql_path = os.path.join(snowflake_dir, "setup.sql")
    jsl_spec_path = os.path.join(snowflake_dir, "jsl_spec.yaml")
    manifest_path = os.path.join(snowflake_dir, "manifest.yml")
    streamlit_app_path = os.path.join(snowflake_dir, "streamlit/streamlit_app.py")
    environment_yml_path = os.path.join(snowflake_dir, "streamlit/environment.yml")
    base_file_dir = os.path.join(
        os.path.join(WORKSPACE_DIR, "endpoints", "snowflake", "templates")
    )

    try:
        metadata = read_metadata(metadata_file_path=metadata_file)
        title = metadata["title"]
        models_hub_url = metadata["models_hub_url"]
        example_text = metadata["example_text"]
        snowflake_compute_pool = metadata["compute_pool"]
        snowflake_application_package = metadata["application_package"]
        snowflake_warehouse = metadata["warehouse"]
        # Set names using metadata values or defaults
        modelPackageName = snowflake_application_package or modelPackageName
        compute_pool_name = snowflake_compute_pool or f"COMPUTE_POOL_{modelPackageName.upper()}"
        warehouse_name = snowflake_warehouse or f"{modelPackageName.upper()}_WAREHOUSE"

        print(f"Using application package name: {modelPackageName}")
        print(f"Using compute pool name: {compute_pool_name}")
        print(f"Using warehouse name: {warehouse_name}")

        print(
            f"Extracted Metadata:\nTitle: {title}\nModels Hub URL: {models_hub_url}\nText: {example_text}"
        )

        conn = snowflake.connector.connect(
            account=snowflake_env["account"],
            user=snowflake_user,
            password=snowflake_password,
            role=snowflake_env["role"],
        )

        cursor = conn.cursor()

        cursor.execute(f"USE DATABASE {snowflake_env['database']};")
        cursor.execute(f"USE SCHEMA {snowflake_env['schema']};")
        cursor.execute(f"USE WAREHOUSE {snowflake_env['warehouse']};")

        if not os.path.exists(manifest_path):

            with open(os.path.join(base_file_dir, "manifest.yml"), "r") as f:
                manifest_content = f.read()

            manifest_content = manifest_content.replace(
                "<<IMAGE_PATH>>", "/".join(image.split("/")[1:])
            )

            print("Creating manifest.yml:")
            print(manifest_content)
            manifest_path = os.path.join(temp_dir, "manifest.yml")
            with open(manifest_path, "w") as temp_file:
                temp_file.write(manifest_content)

        if not os.path.exists(jsl_spec_path):

            with open(os.path.join(base_file_dir, "jsl_spec.yaml"), "r") as f:
                jsl_spec_content = f.read()

            jsl_spec_content = jsl_spec_content.replace("<<IMAGE_PATH>>", image)

            print("Creating jsl_spec.yaml:")
            print(jsl_spec_content)
            jsl_spec_path = os.path.join(temp_dir, "jsl_spec.yaml")
            with open(jsl_spec_path, "w") as temp_file:
                temp_file.write(jsl_spec_content)

        if not os.path.exists(setup_sql_path):
            with open(os.path.join(base_file_dir, "setup.sql"), "r") as f:
                setup_sql_content = f.read()

            replacements = {
                "<<COMPUTE_POOL_NAME>>": compute_pool_name,
                "<<WAREHOUSE_NAME>>": warehouse_name,
            }

            for placeholder, value in replacements.items():
                setup_sql_content = setup_sql_content.replace(placeholder, value)

            print("Creating setup.sql:")
            print(setup_sql_content)
            setup_sql_path = os.path.join(temp_dir, "setup.sql")
            with open(setup_sql_path, "w") as temp_file:
                temp_file.write(setup_sql_content)

        if not os.path.exists(streamlit_app_path):
            print("Creating streamlit_app.py dynamically from base dir")

            with open(os.path.join(base_file_dir, "streamlit_app.py"), "r") as f:
                streamlit_app_content = f.read()

            variables_code = {
                "<<TITLE>>": title,
                "<<MODELS_HUB_URL>>": models_hub_url if models_hub_url else "",
                "<<EXAMPLE_TEXT>>": example_text,
            }

            for placeholder, actual_value in variables_code.items():
                streamlit_app_content = streamlit_app_content.replace(
                    placeholder, actual_value
                )

            streamlit_app_path = os.path.join(temp_dir, "streamlit_app.py")

            with open(streamlit_app_path, "w") as temp_file:
                temp_file.write(streamlit_app_content)

        if not os.path.exists(environment_yml_path):
            base_environment_yml = os.path.join(base_file_dir, "environment.yml")
            environment_yml_path = base_environment_yml
            print("Using environment.yml from base dir")

        print("\nChecking existing image repositories:")
        cursor.execute("SHOW IMAGE REPOSITORIES")
        for row in cursor.fetchall():
            print(row)

        try:
            print("Creating Application Package")

            cursor.execute(f"CREATE APPLICATION PACKAGE {modelPackageName};")

            stage_name = upload_files_to_stage(
                cursor,
                modelPackageName,
                snowflake_dir,
                manifest_path,
                setup_sql_path,
                jsl_spec_path,
                streamlit_app_path,
                environment_yml_path,
            )

            cursor.execute(
                f'ALTER APPLICATION PACKAGE {modelPackageName} ADD VERSION "v1_0" USING {stage_name};'
            )

            print("Creating Application")
            cursor.execute(
                f'CREATE APPLICATION {modelPackageName}_app FROM APPLICATION PACKAGE {modelPackageName} USING VERSION "v1_0" DEBUG_MODE = TRUE;'
            )

            test_application_package(cursor, modelPackageName, example_text)

            print("Testing complete.")

            print("Granting necessary permissions.")
            cursor.execute(
                f"GRANT ATTACH LISTING ON APPLICATION PACKAGE {modelPackageName} TO ROLE accountadmin;"
            )
            cursor.execute(
                f"ALTER APPLICATION PACKAGE {modelPackageName} SET DISTRIBUTION = EXTERNAL;"
            )

        except snowflake.connector.errors.ProgrammingError as e:
            if "already exists" in str(e):
                print(f"Application package {modelPackageName} already exists.")
                stage_name = upload_files_to_stage(
                    cursor,
                    modelPackageName,
                    snowflake_dir,
                    manifest_path,
                    setup_sql_path,
                    jsl_spec_path,
                    streamlit_app_path,
                    environment_yml_path,
                )

                print("Adding patch version...")

                cursor.execute(
                    f'ALTER APPLICATION PACKAGE {modelPackageName} ADD PATCH FOR VERSION "v1_0" USING {stage_name};'
                )

                print(f"Checking if application {modelPackageName}_app exists...")

                cursor.execute(f"SHOW APPLICATIONS LIKE '{modelPackageName}_app';")
                app_result = cursor.fetchone()

                if app_result is not None:
                    print(
                        f"Upgrading application {modelPackageName}_app to new version."
                    )
                    cursor.execute(
                        f'ALTER APPLICATION {modelPackageName}_app UPGRADE USING VERSION "v1_0";'
                    )
                else:
                    print(
                        f"Application {modelPackageName}_app does not exist. Creating it."
                    )
                    cursor.execute(
                        f'CREATE APPLICATION {modelPackageName}_app FROM APPLICATION PACKAGE {modelPackageName} USING VERSION "v1_0" DEBUG_MODE = TRUE;'
                    )

                test_application_package(cursor, modelPackageName, example_text)
                print("Testing complete.")

                print("Granting necessary permissions.")
                cursor.execute(
                    f"GRANT ATTACH LISTING ON APPLICATION PACKAGE {modelPackageName} TO ROLE accountadmin;"
                )
                cursor.execute(
                    f"ALTER APPLICATION PACKAGE {modelPackageName} SET DISTRIBUTION = EXTERNAL;"
                )
            else:
                print(f"Error during Snowflake operations: {e}")
                sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                print(f"\nTemporary directory '{temp_dir}' removed.")
            cursor.close()
            conn.close()
        except:
            pass


if __name__ == "__main__":
    modelPackageName = sys.argv[1]
    snowflake_dir = sys.argv[2]
    image = sys.argv[3]
    metadata_file = sys.argv[4]
    
    perform_remaining_operations(
        modelPackageName,
        snowflake_dir,
        image,
        metadata_file,
    )
