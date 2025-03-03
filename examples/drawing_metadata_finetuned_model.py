import json
from dotenv import load_dotenv  
load_dotenv()
from datacrunch_api.v1 import Deployments
import typer  # type: ignore
from rich import print  # type: ignore
from rich.panel import Panel  # type: ignore
import requests
from os import environ

from .metadata_extraction_vllm_endpoint import VLLMEndpoint


CONTAINER_NAME = "drawing-metadata-extraction" 
IMAGE = "786001665406.dkr.ecr.eu-central-1.amazonaws.com/datacrunch:drawing-metadata-extraction" 

IS_PRIVATE_REPO = True


MODEL = "Qwen/Qwen2.5-VL-7B-Instruct"
COMMAND = [] # DOENST matter when using sync data on aws first since its overwritten


def add_env_vars(ENDPOINT_NAME):
    """sets the AWS env vars"""
    # Get access token
    token_url = "https://api.datacrunch.io/v1/oauth2/token"
    token_payload = {
        "grant_type": "client_credentials", 
        "client_id": environ["DATACRUNCH_CLIENT_ID"],
        "client_secret": environ["DATACRUNCH_CLIENT_SECRET"]
    }
    token_headers = {
        "Content-Type": "application/json"
    }

    token_response = requests.post(token_url, headers=token_headers, json=token_payload)
    ACCESS_TOKEN = token_response.json()["access_token"]

    url = f"https://api.datacrunch.io/v1/container-deployments/{ENDPOINT_NAME}/environment-variables"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Define the payload with container name and environment variables
    payload = {
        "container_name": CONTAINER_NAME,
        "env": [
            {"name": "AWS_ACCESS_KEY_ID", "value_or_reference_to_secret": "aws-access-key", "type": "secret"},
            {"name": "AWS_SECRET_ACCESS_KEY", "value_or_reference_to_secret": "aws-secret-key", "type": "secret"},
            {"name": "AWS_DEFAULT_REGION", "value_or_reference_to_secret": "eu-central-1", "type": "plain"},
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.json())


def main(
    action: str = typer.Option(
        ..., help="Action to perform: create, delete, list, status, update"
    ),
    client_id: str = typer.Option(
        None, 
        help="DataCrunch client ID", 
        envvar="DATACRUNCH_CLIENT_ID"
    ),
    client_secret: str = typer.Option(
        None, 
        help="DataCrunch client secret", 
        envvar="DATACRUNCH_CLIENT_SECRET"
    ),
    huggingface_key: str = typer.Option(
        None, 
        help="HuggingFace API key", # NOTE is just the name of the key, not the actul key
        envvar="HUGGINGFACE_API_KEY"
    ),
    name: str = typer.Option(..., help="Name of the endpoint"),
):
    api = Deployments(client_id, client_secret)
    endpoint = VLLMEndpoint(api, name, IS_PRIVATE_REPO)

    response: dict | list | None = None
    match action:
        case "create":
            print("Creating endpoint")
            response = endpoint.create_endpoint(CONTAINER_NAME, IMAGE, COMMAND)
            # print("Adding env vars")
            # add_env_vars(ENDPOINT_NAME=name)
        case "delete":
            endpoint.delete_endpoint()
        case "list":
            response = api.list_container_deployments()
        case "status":
            response = api.get_deployment_status(name)
        case "update":
            response = endpoint.update_endpoint(CONTAINER_NAME, IMAGE, COMMAND)
        case _:
            raise typer.Abort()
    print(
        Panel.fit(
            json.dumps(response, indent=2),
            title="Response",
            border_style="green",
        )
    )


if __name__ == "__main__":
    typer.run(main)
