import json
from dotenv import load_dotenv  
load_dotenv()
from datacrunch_api.v1 import Deployments
import typer  # type: ignore
from rich import print  # type: ignore
from rich.panel import Panel  # type: ignore

from .vllm_endpoint import VLLMEndpoint

CONTAINER_NAME = "base-image-with-sync-v4"

# IMAGE = "786001665406.dkr.ecr.eu-central-1.amazonaws.com/datacrunch:base-image-with-sync-v4" # private repo
CONTAINER_NAME = "base-vllm-image"
IMAGE = "786001665406.dkr.ecr.eu-central-1.amazonaws.com/datacrunch:base-vllm-image" # should work
# IMAGE = "786001665406.dkr.ecr.eu-central-1.amazonaws.com/datacrunch:hello-world-v2" # private repo

IS_PRIVATE_REPO = True

 

MODEL = "Qwen/Qwen2.5-VL-7B-Instruct"
COMMAND = [
    "--model",
    MODEL,
    "--gpu-memory-utilization",
    "0.9",
    "--max-model-len",
    "8192",
    "--trust-remote-code",
    "--enable-lora",
    "--lora-modules",
    "custom-adapter=/data/adapters"  # This is the container path
]



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
    aws_access_key: str = typer.Option(
        None,
        help="AWS access key",
        envvar="AWS_ACCESS_KEY"
    ),
    aws_secret_key: str = typer.Option(
        None,
        help="AWS secret key",
        envvar="AWS_SECRET_KEY"
    ),
    name: str = typer.Option(..., help="Name of the endpoint"),
):
    api = Deployments(client_id, client_secret)
    endpoint = VLLMEndpoint(api, huggingface_key, name)
    # endpoint = VLLMEndpoint(api, huggingface_key, aws_access_key, aws_secret_key, name, is_private=IS_PRIVATE_REPO)

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
