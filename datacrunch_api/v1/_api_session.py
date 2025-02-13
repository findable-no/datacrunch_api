import requests

BASE_URL = "https://api.datacrunch.io/v1"


class ApiSession:
    class Conflict(Exception):
        pass

    class InvalidRequest(Exception):
        pass

    class RequestFailed(Exception):
        pass

    def __init__(self, client_id: str, client_secret: str, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.authenticate(client_id, client_secret)

    def authenticate(self, client_id: str, client_secret: str):
        """Authenticate with the DataCrunch API using client credentials"""
        response = self.session.post(
            f"{self.base_url}/oauth2/token",
            json={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )
        token = response.json()["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def delete(self, url: str) -> None:
        response = self.session.delete(f"{self.base_url}/{url}")
        if response.status_code != 200:
            raise self.RequestFailed(response.json())

    def get(self, url: str) -> dict | list:
        response = self.session.get(f"{self.base_url}/{url}")
        return self.validate_response(response.json())

    def patch(self, url: str, json: dict) -> dict:
        response = self.session.patch(f"{self.base_url}/{url}", json=json)
        return self.validate_response(response.json())

    def post(self, url: str, json: dict) -> dict:
        response = self.post_raw(url, json)
        return self.validate_response(response.json())

    def post_raw(self, url: str, json: dict) -> requests.Response:
        response = self.session.post(f"{self.base_url}/{url}", json=json)
        return response

    def validate_response(self, response: dict) -> dict:
        if "code" not in response:
            return response
        match response["code"]:
            case "invalid_request":
                raise self.InvalidRequest(response.get("message"))
            case "conflict":
                raise self.Conflict(response.get("message"))
            case _:
                return response
