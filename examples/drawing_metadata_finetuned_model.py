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
COMMAND = [] # doesn't matter when using sync data on aws first since its overwritten



def main(
    action: str = typer.Option(
        ..., help="Action to perform: create, delete, list, status, update"
    ),
    client_id: str = typer.Option(..., help="DataCrunch client ID"),
    client_secret: str = typer.Option(..., help="DataCrunch client secret"),
    name: str = typer.Option(..., help="Name of the endpoint"),
):
    api = Deployments(client_id, client_secret)
    endpoint = VLLMEndpoint(api, name, IS_PRIVATE_REPO)

    response: dict | list | None = None
    match action:
        case "create":
            response = endpoint.create_endpoint(CONTAINER_NAME, IMAGE, COMMAND)
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
