import json

from datacrunch.v1 import Secret, Secrets
import typer
from rich import print
from rich.panel import Panel


def main(
    action: str = typer.Option(..., help="Action to perform"),
    client_id: str = typer.Option(..., help="DataCrunch client ID"),
    client_secret: str = typer.Option(..., help="DataCrunch client secret"),
    name: str = typer.Option("", help="Name of the secret"),
    value: str = typer.Option("", help="Value of the secret"),
):
    api = Secrets(client_id, client_secret)
    match action:
        case "list":
            response = api.list_secrets()
        case "create":
            response = api.create_secret(Secret(name, value))
        case "delete":
            response = api.delete_secret(name)
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
