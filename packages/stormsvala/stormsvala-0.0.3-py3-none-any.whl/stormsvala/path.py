from dataclasses import dataclass
import re


class InvalidPathException(Exception):
    pass


@dataclass
class Path:
    """
    Args
        catalog: the catalog in postgres
        schema: the schema in postgres
        name: the name of the thing
    """

    catalog: str | None
    schema: str
    name: str

    def full_path_to_str(self) -> str:
        return f"{self.catalog}.{self.schema}.{self.name}"

    def schema_path_to_str(self) -> str:
        return f"{self.schema}.{self.name}"

    @staticmethod
    def validate_not_empty(string: str):
        if not string:
            raise ValueError("Name cannot be empty")

    def validate_part(string: str):
        pattern = r"^[a-zA-Z0-9_]+$"
        if not re.match(pattern, string):
            raise ValueError(
                f"Name '{string}' must contain only letters, numbers, or underscores"
            )

    def __post_init__(self):
        for string in [self.catalog, self.schema, self.name]:
            Path.validate_part(string)
