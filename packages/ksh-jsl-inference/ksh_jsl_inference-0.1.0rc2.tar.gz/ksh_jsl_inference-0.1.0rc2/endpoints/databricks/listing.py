import requests
from requests.structures import CaseInsensitiveDict
from pyspark.sql.types import *
import json
import validators
import pandas as pd
from github import Github
import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class Marketplace_listings:
    def __init__(self, token, url):
        self.auth = BearerAuth(TOKEN)
        self.url = url

    def get_all_listings(self):
        end_point = "listings"
        call = self.url + end_point
        resp = requests.get(call, auth=self.auth).json()
        return resp

    def get_listing(self, listing_id):
        end_point = f"listings/{listing_id}"
        call = self.url + end_point
        resp = requests.get(call, auth=self.auth).json()
        return resp

    def create_notebook_file(self, listing_id):
        data_string = f'{{"marketplace_file_type": "EMBEDDED_NOTEBOOK", "file_parent": {{"parent_id":"{listing_id}" ,"file_parent_type": "LISTING"}},"mime_type":"text/html","display_name":"John Snow Labs Universal Notebook"}}'
        end_point = "files"
        call = self.url + end_point
        resp = requests.post(call, auth=self.auth, json=json.loads(data_string))
        return resp.json()

    def upload_notebook_file(self, signed_url, notebook_path):
        headers = CaseInsensitiveDict()
        headers["X-Amz-Server-Side-Encryption"] = "AES256"
        headers["Content-Type"] = f"text/html"
        if validators.url(notebook_path) == 1:
            notebook = requests.get(notebook_path, stream=True).content
        else:
            notebook = open(notebook_path, "rb").read()
        data = notebook
        resp = requests.put(signed_url, headers=headers, data=data)
        return resp

    def get_file(self, file_id):
        """
        Method to return file information. This will be used in the post_file method to return the file ID and URL of the notebook
        """
        end_point = f"files/{file_id}"
        call = self.url + end_point
        resp = requests.get(call, auth=self.auth)
        return resp.json()

    def update_listing_notebook(self, listing_id, notebook_file):
        """
        Method to add the notebook to a listing.
        """
        data = self.get_listing(listing_id)  # Get info for existing listing
        data["listing"]["detail"]["embedded_notebook_file_infos"] = {}
        data["listing"]["detail"]["embedded_notebook_file_infos"]["id"] = notebook_file
        data["listing"]["deployment_name"] = "N/A"
        data["listing"].pop("id")  # should not be part of the payload
        listing = json.dumps(data)
        end_point = f"listings/{listing_id}"
        call = self.url + end_point
        resp = requests.put(url=call, auth=self.auth, data=listing)
        return resp

    def post_listing_notebook(self, listing_id, notebook_path):
        """
        This function combines the create, upload and get_file methods creating the file link for an notebook
        and posting the file. We will then update the provider profile with the notebook
        Inputs:
        listing_id,
        notebook_path - This can be a local reference or link. File has to be an HTML file
        """

        upload_url = self.create_notebook_file(listing_id)
        uploaded_file = self.upload_notebook_file(
            upload_url["upload_url"], notebook_path
        )
        file_info = self.get_file(upload_url["file_info"]["id"])

        resp = self.update_listing_notebook(
            listing_id, file_info["file_info"]["id"]
        )  # post the file to the listing
        return file_info  # resp.json()


db_token = "dapia76b09b6666290c57daf1c9ee30b0e0a"
db_host = "https://dbc-f4eb4bcb-4ef3.cloud.databricks.com"
TOKEN = db_token
WORKSPACE_URL = db_host
URL = f"{WORKSPACE_URL}/api/2.0/marketplace-provider/"
# nb_path = "/home/ckl/data-server/backup_popos_workstation_2023/Documents/freelance/jsl/johnsnowlabs-4-real/notebooks/databricks_model_marketplace.ipynb"
nb_path = "/home/ckl/data-server/backup_popos_workstation_2023/Documents/freelance/jsl/johnsnowlabs-4-real/notebooks/Databricks Model Marketplace.html"

listing_id = "eb2042f5-8a50-459c-8884-e11f9573c618"


ML = Marketplace_listings(TOKEN, URL)

for l in ML.get_all_listings()["listings"]:
    if l["summary"]["created_by"] != "christian@johnsnowlabs.com":
        continue
    print(
        "https://dbc-f4eb4bcb-4ef3.cloud.databricks.com/marketplace/provider/listings/"
        + l["id"]
    )

    r = ML.post_listing_notebook(l["id"], nb_path)
    # print(r)
