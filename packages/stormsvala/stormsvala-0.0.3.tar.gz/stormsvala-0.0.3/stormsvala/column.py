from __future__ import annotations
from dataclasses import dataclass
from stormsvala.path import Path
from psycopg2 import sql
from psycopg2.sql import Composed


@dataclass
class CustomType:
    path: Path
    columns: list[Column]

    def compose_custom_type_definition(self) -> Composed:
        """Custom types don't have catalogs, they are created in the schema context"""
        columns_def = ", ".join(
            f"{col.name} {col.type} {col.constraint}" for col in self.columns
        )

        return sql.SQL("CREATE TYPE {}.{} AS ({})").format(
            sql.Identifier(self.path.schema),
            sql.Identifier(self.path.name),
            sql.SQL(columns_def),
        )

    def compose_check_if_custom_type_exists(self) -> Composed:
        query = (
            "SELECT 1 FROM pg_catalog.pg_type t "
            "JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace "
            "WHERE n.nspname = {} AND t.typname = {}"
        )
        return sql.SQL(query).format(
            sql.Literal(self.path.schema), sql.Literal(self.path.name)
        )


@dataclass
class Column:
    name: str
    type: str
    constraint: str = ""
