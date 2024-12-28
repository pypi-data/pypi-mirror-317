from stormsvala.column import Column, CustomType
from stormsvala.path import Path
from dataclasses import dataclass, field
from psycopg2.sql import Composed, SQL, Identifier, Placeholder


@dataclass
class Table:
    path: Path
    columns: list[Column]
    custom_types: list[CustomType]
    table_definition: Composed = None
    batch_size: int = 5000
    attributes: list[Column | CustomType] = field(default_factory=list)

    def __post_init__(self):
        self.attributes = self.custom_types + self.columns
        self.table_definition = self.compose_table_definition()

    def compose_check_if_table_exists(self) -> Composed:
        """Has two placeholders, expects schema and table"""
        return SQL(
            "SELECT 1 FROM information_schema.tables WHERE table_schema = {} AND table_name = {}"
        ).format(Placeholder(), Placeholder())

    def compose_table_definition(self) -> Composed:
        table_def = SQL("CREATE TABLE {}.{} (").format(
            Identifier(self.path.schema), Identifier(self.path.name)
        )

        table_attributes = []

        for custom_type in self.custom_types:
            table_attributes.append(
                SQL("{} {}").format(
                    Identifier(custom_type.path.name),
                    SQL(f"{custom_type.path.schema}.{custom_type.path.name}"),
                )
            )

        for column in self.columns:
            table_attributes.append(
                SQL("{} {} {}").format(
                    Identifier(column.name), SQL(column.type), SQL(column.constraint)
                )
            )

        table_def = table_def + SQL(",\n").join(table_attributes)
        table_def = table_def + SQL(");")

        return table_def

    def compose_insert_statement(self) -> Composed:
        attribute_names = []
        values_placeholders = []

        for typ in self.custom_types:
            attribute_names.append(Identifier(typ.path.name))
            custom_type_placeholders = [Placeholder() for _ in typ.columns]
            values_placeholders.append(
                SQL("({})").format(SQL(", ").join(custom_type_placeholders))
            )

        for col in self.columns:
            attribute_names.append(Identifier(col.name))
            values_placeholders.append(Placeholder())

        insert_statement = SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
            Identifier(self.path.schema),
            Identifier(self.path.name),
            SQL(", ").join(attribute_names),
            SQL(", ").join(values_placeholders),
        )

        return insert_statement
