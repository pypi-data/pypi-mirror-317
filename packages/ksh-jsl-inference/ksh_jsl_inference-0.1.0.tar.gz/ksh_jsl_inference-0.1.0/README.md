# endpoints

## Databricks Development

see `databricks_tests.py` 
1. Start up a Databricks Cluster producer. Once Started you must **manually enable it to Unity Catalog**
2. Submit publisher job
3. Once completed, need to go to provider UI and publish the model to either private or public exchange
4. Once published, **you must manually import the listing on consumer end form the UI and accept the Terms of usage**. Then model can be tested via consumer jobs



## SageMaker Development

In order to add a new JSL model to the SageMaker Marketplace models, the following steps are expected.

1.  Create the necessary docker image that exposes an `/invocations` endpoints. The model and all its artifacts are expected to be in a specific structure so that's easy to introduce automation in the future.

    To create the expected directory and file structure for the new model, developer is expected to run this command

        python generate_sagemaker_models.py <name_of_model>

    This will generate the necessary base directory and files in the configured structure.

    The developer is expected to change the generated Docker image with the invocations particular to the models design.

2.  Add a notebook that creates the docker image on AWS SageMaker and also tests and creates a Model Package that will be later used for publishing.

3.  Add inputs/outputs specific to the model. Add documentation (if necessary) for the input and output schema. Also, a buyer facing notebook is to be added that buyers can easily run to run the Marketplace Model

### Toolkit

To get some information on the available models and its details, use this helper command

<small>Please make sure to install dependencies before. See tools/requirements.txt </small>
```python
python tools/models_info.py
```
You can also refer the help for this toolkit
```python
python tools/models_info.py --help
```
