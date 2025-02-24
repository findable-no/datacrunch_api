import requests

BASE_URL = "https://api.datacrunch.io/v1"


class ApiSession:
    """
    Handles authentication and API requests to the DataCrunch API.
    Provides methods for making HTTP requests and validating responses.
    """

    class Conflict(Exception):
        """Raised when a request conflicts with an existing resource"""

        pass

    class InvalidRequest(Exception):
        """Raised when a request is malformed or contains invalid data"""

        pass

    class RequestFailed(Exception):
        """Raised when an API request fails for any other reason"""

        pass

    def __init__(self, client_id: str, client_secret: str, base_url: str = BASE_URL):
        """
        Initialize an API session with client credentials.

        Args:
            client_id: The client ID for authentication
            client_secret: The client secret for authentication
            base_url: Optional custom base URL for the API
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.authenticate(client_id, client_secret)

    def authenticate(self, client_id: str, client_secret: str) -> None:
        """
        Authenticate with the DataCrunch API using client credentials.
        Sets the authorization header for subsequent requests.

        Args:
            client_id: The client ID for authentication
            client_secret: The client secret for authentication
        """
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

    def delete(self, url: str, json: dict | None = None) -> None:
        """
        Send a DELETE request to the API.

        Args:
            url: The API endpoint URL

        Raises:
            RequestFailed: If the request fails
        """
        response = self.session.delete(f"{self.base_url}/{url}", json=json)
        if response.status_code < 200 or response.status_code >= 300:
            raise self.RequestFailed(response.json())

    def get(self, url: str) -> dict | list:
        """
        Send a GET request to the API.

        Args:
            url: The API endpoint URL

        Returns:
            The JSON response as a dict or list

        Raises:
            InvalidRequest: If the request is invalid
            Conflict: If there is a resource conflict
        """
        response = self.session.get(f"{self.base_url}/{url}")
        return self.validate_response(response.json())

    def patch(self, url: str, json: dict) -> dict:
        """
        Send a PATCH request to the API.

        Args:
            url: The API endpoint URL
            json: The request body as a dict

        Returns:
            The JSON response as a dict

        Raises:
            InvalidRequest: If the request is invalid
            Conflict: If there is a resource conflict
        """
        response = self.session.patch(f"{self.base_url}/{url}", json=json)
        return self.validate_response(response.json())

    def post(self, url: str, json: dict) -> dict | str:
        """
        Send a POST request to the API and validate the response.

        Args:
            url: The API endpoint URL
            json: The request body as a dict

        Returns:
            The validated JSON response as a dict

        Raises:
            InvalidRequest: If the request is invalid
            Conflict: If there is a resource conflict
        """
        response = self.post_raw(url, json)
        return self.validate_response(response.json())

    def post_raw(self, url: str, json: dict) -> requests.Response:
        """
        Send a POST request to the API without validating the response.

        Args:
            url: The API endpoint URL
            json: The request body as a dict

        Returns:
            The raw requests.Response object
        """
        response = self.session.post(f"{self.base_url}/{url}", json=json)
        return response

    def put(self, url: str, json: dict) -> dict:
        """
        Send a PUT request to the API and validate the response.

        Args:
            url: The API endpoint URL
            json: The request body as a dict

        Returns:
            The validated JSON response as a dict

        Raises:
            InvalidRequest: If the request is invalid
        """
        response = self.session.put(f"{self.base_url}/{url}", json=json)
        return self.validate_response(response.json())

    def put_raw(self, url: str, json: dict) -> requests.Response:
        """
        Send a PUT request to the API without validating the response.

        Args:
            url: The API endpoint URL
            json: The request body as a dict

        Returns:
            The raw requests.Response object
        """
        response = self.session.put(f"{self.base_url}/{url}", json=json)
        return response

    def validate_response(self, response: dict) -> dict:
        """
        Validate an API response and raise appropriate exceptions if needed.

        Args:
            response: The JSON response from the API

        Returns:
            The validated response dict

        Raises:
            InvalidRequest: If the response indicates an invalid request
            Conflict: If the response indicates a resource conflict
        """
        if "code" not in response:
            return response
        match response["code"]:
            case "invalid_request":
                raise self.InvalidRequest(response.get("message"))
            case "conflict":
                raise self.Conflict(response.get("message"))
            case _:
                return response
