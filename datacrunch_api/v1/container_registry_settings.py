from dataclasses import dataclass

from .credentials import Credentials, CredentialsValue

ContainerRegistrySettingsValue = dict[str, bool | CredentialsValue]


@dataclass
class ContainerRegistrySettings:
    is_private: bool
    credentials: Credentials | None = None

    def to_dict(self) -> ContainerRegistrySettingsValue:
        response: ContainerRegistrySettingsValue = {
            "is_private": self.is_private,
        }
        if self.is_private:
            assert self.credentials is not None
            response["credentials"] = self.credentials.to_dict()
        return response
