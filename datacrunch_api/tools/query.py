import json

from datacrunch_api.v1 import (
    Deployments,
    Secrets,
    ServerlessCompute,
)
import typer
from rich import print
from rich.panel import Panel


def main(
    action: str = typer.Option(..., help="Action to perform: list, status"),
    client_id: str = typer.Option(..., help="DataCrunch client ID"),
    client_secret: str = typer.Option(..., help="DataCrunch client secret"),
    name: str = typer.Option("", help="Name of the query"),
):
    response: dict | list | None = None
    match action:
        case "list":
            deployments = Deployments(client_id, client_secret)
            response = deployments.list_container_deployments()
        case "status":
            deployments = Deployments(client_id, client_secret)
            response = deployments.get_deployment_status(name)
        case "list-secrets":
            secrets = Secrets(client_id, client_secret)
            response = secrets.list_secrets()
        case "list-serverless-compute":
            serverless_compute = ServerlessCompute(client_id, client_secret)
            response = serverless_compute.list_serverless_compute_resources()
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
