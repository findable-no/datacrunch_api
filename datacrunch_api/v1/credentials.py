from dataclasses import dataclass

CredentialsValue = dict[str, str]


@dataclass
class Credentials:
    name: str

    def to_dict(self) -> CredentialsValue:
        return {
            "name": self.name,
        }
