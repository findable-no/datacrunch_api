import json

from datacrunch_api.v1 import Deployments
import typer  # type: ignore
from rich import print  # type: ignore
from rich.panel import Panel  # type: ignore

from .vllm_endpoint import VLLMEndpoint

CONTAINER_NAME = "deepseek-v3"
IMAGE = "docker.io/vllm/vllm-openai:v0.7.1"
MODEL = "deepseek-ai/DeepSeek-V3"
COMMAND = [
    "--model",
    MODEL,
    "--gpu-memory-utilization",
    "0.9",
    "--max-model-len",
    "8192",
    "--trust-remote-code",
]


def main(
    action: str = typer.Option(
        ..., help="Action to perform: create, delete, list, status, update"
    ),
    client_id: str = typer.Option(..., help="DataCrunch client ID"),
    client_secret: str = typer.Option(..., help="DataCrunch client secret"),
    huggingface_key: str = typer.Option(..., help="HuggingFace API key"),
    name: str = typer.Option(..., help="Name of the endpoint"),
):
    api = Deployments(client_id, client_secret)
    endpoint = VLLMEndpoint(api, huggingface_key, name)

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
