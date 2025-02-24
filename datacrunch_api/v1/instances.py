from enum import Enum
from urllib.parse import urlencode
from ._api_session import ApiSession
from .types.instance import Currency, DEFAULT_CURRENCY, Instance, InstanceAction


class Endpoints(str, Enum):
    """API endpoints for managing instances"""

    INSTANCE_AVAILABILITY = "instance-availability"
    INSTANCE_TYPES = "instance-types"
    INSTANCES = "instances"
    LOCATIONS = "locations"
    LONG_TERM = "long-term"
    PERIODS = "periods"
    PRICE_HISTORY = "price-history"


class Instances:
    """
    Client for managing instances in the DataCrunch API.
    """

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize instances client with API credentials
        """
        self.api_session = ApiSession(client_id, client_secret)

    def action(self, action: InstanceAction) -> None:
        """
        Perform an action on an instance
        """
        response = self.api_session.put_raw(
            Endpoints.INSTANCES.value, json=action.to_dict()  # type: ignore
        )
        if response.status_code != 202:
            raise self.api_session.RequestFailed(response.json())

    def delete_instance(self, instance_id: str) -> None:
        """
        Delete an instance
        """
        action = InstanceAction(action="delete", instance_id=instance_id)
        self.action(action)

    def deploy(self, instance: Instance) -> str:
        """
        Deploy a new instance
        """
        return str(
            self.api_session.post(
                Endpoints.INSTANCES.value, json=instance.to_dict()  # type: ignore
            )
        )

    def get_instance(self, instance_id: str) -> dict:
        """
        Get an instance by ID
        """
        return dict(self.api_session.get(f"{Endpoints.INSTANCES.value}/{instance_id}"))

    def get_instance_type_availabilities(
        self,
        is_spot: bool | None = None,
        location_code: str | None = None,
    ) -> list[dict] | bool:
        """
        Get the availability information for instance types.

        Args:
            instance_type: Optional specific instance type to check availability for.
                         If None, returns availability for all instance types.
            is_spot: Optional filter for spot instances.
                    If True, only returns spot instance availability.
                    If False, only returns on-demand instance availability.
                    If None, returns both spot and on-demand availability.
            location_code: Optional location code to filter availability by region.
                         If None, returns availability across all regions.

        Returns:
            A list of dictionaries containing availability information for the requested
            instance types, including details like capacity and pricing.

        Raises:
            InvalidRequest: If the request parameters are invalid
            RequestFailed: If the API request fails
        """
        params: dict[str, str | bool] = {}
        if is_spot is not None:
            params["is_spot"] = is_spot
        if location_code is not None:
            params["location_code"] = location_code
        return list(
            self.api_session.get(
                f"{Endpoints.INSTANCE_AVAILABILITY.value}?{urlencode(params)}"
            )
        )

    def get_instance_type_availability(
        self,
        instance_type: str,
        is_spot: bool | None = None,
        location_code: str | None = None,
    ) -> list[dict] | bool:
        """
        Get the availability information for instance types.

        Args:
            instance_type: Optional specific instance type to check availability for.
                         If None, returns availability for all instance types.
            is_spot: Optional filter for spot instances.
                    If True, only returns spot instance availability.
                    If False, only returns on-demand instance availability.
                    If None, returns both spot and on-demand availability.
            location_code: Optional location code to filter availability by region.
                         If None, returns availability across all regions.

        Returns:
            A list of dictionaries containing availability information for the requested
            instance types, including details like capacity and pricing.

        Raises:
            InvalidRequest: If the request parameters are invalid
            RequestFailed: If the API request fails
        """
        params: dict[str, str | bool] = {}
        if is_spot is not None:
            params["is_spot"] = is_spot
        if location_code is not None:
            params["location_code"] = location_code
        return bool(
            self.api_session.get(
                f"{Endpoints.INSTANCE_AVAILABILITY.value}/{instance_type}?{urlencode(params)}"
            )
        )

    def get_price_history(
        self, instance_type: str, currency: Currency | None = None
    ) -> dict[str, list[dict]]:
        """
        Get the price history for an instance type
        """
        actual_currency = currency or DEFAULT_CURRENCY
        return dict(
            self.api_session.get(
                f"{Endpoints.PRICE_HISTORY.value}/{instance_type}/{actual_currency}"
            )
        )

    def list_instance_types(self, currency: Currency | None = None) -> list[dict]:
        """
        Get all instance types
        """
        actual_currency = currency or DEFAULT_CURRENCY
        return list(
            self.api_session.get(
                f"{Endpoints.INSTANCE_TYPES.value}?currency={actual_currency}"
            )
        )

    def list_instances(self) -> list[dict]:
        """
        List all instances
        """
        return list(self.api_session.get(Endpoints.INSTANCES.value))

    def list_locations(self) -> list[dict[str, str]]:
        """
        List all locations
        """
        return list(self.api_session.get(Endpoints.LOCATIONS.value))

    def list_long_term_periods(self) -> list[dict[str, bool | int | str]]:
        """
        List all long-term periods
        """
        return list(self.api_session.get(Endpoints.LONG_TERM.value))
