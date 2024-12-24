import os
import shutil
import pytest
from click.testing import CliRunner
from endpoints.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_generate_docker_files(runner):
    model = "clinical_deidentification_multi_mode_output"
    output_dir = "/tmp/test_output"

    result = runner.invoke(
        cli,
        [
            "sagemaker",
            "generate-docker-files",
            model,
            "--johnsnowlabs-version",
            "5.5.0",
            "--store-license",
            "--store-model",
            "--language",
            "en",
            "--output-dir",
            output_dir,
        ],
    )

    assert result.exit_code == 0
    assert f"Docker files generated at: {output_dir}" in result.output
    assert os.path.isdir(output_dir)
    assert os.path.isfile(os.path.join(output_dir, "Dockerfile"))

    shutil.rmtree(output_dir, ignore_errors=True)


def test_build_docker_image(runner, license_path, tmp_path):
    if not license_path:
        pytest.skip("No license path provided. Skipping test_build_docker_image.")

    model = "clinical_deidentification_multi_mode_output"

    test_license_file = tmp_path / "license.txt"
    shutil.copyfile(license_path, test_license_file)

    result = runner.invoke(
        cli,
        [
            "sagemaker",
            "build-docker-image",
            model,
            "--johnsnowlabs-version",
            "5.5.0",
            "--store-license",
            "--store-model",
            "--language",
            "en",
            "--license-path",
            str(test_license_file),
        ],
    )

    assert result.exit_code == 0
    assert f"Docker image '{model}:latest' built successfully!" in result.output
