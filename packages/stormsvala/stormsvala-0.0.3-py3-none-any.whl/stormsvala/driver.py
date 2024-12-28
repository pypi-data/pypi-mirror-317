from itertools import batched
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection as Connection
from psycopg2 import sql
import logging
from typing import Iterable
from stormsvala.table import Table
from stormsvala.column import Column, CustomType


class PostgresDriver:
    def __init__(self, dsn: str, minconn: int = 1, maxconn: int = 10):
        """Initializes the PostgresDriver with a DSN connection string.

        Args:
            dsn (str): The DSN connection string (like a URL).
            minconn (int, optional): The minimum number of connections in the pool. Default is 1.
            maxconn (int, optional): The maximum number of connections in the pool. Default is 10.
        """
        self.dsn = dsn
        self.minconn = minconn
        self.maxconn = maxconn
        self.pool = None
        self._initialize_pool()

    def _initialize_pool(self):
        try:
            self.pool = SimpleConnectionPool(self.minconn, self.maxconn, self.dsn)
            if self.pool:
                logging.info(
                    f"Postgres connection pool created with min={self.minconn}, max={self.maxconn}"
                )
        except Exception as e:
            logging.error(f"Error initializing connection pool: {e}")
            raise Exception from e

    def get_connection(self) -> Connection:
        if self.pool:
            return self.pool.getconn()
        else:
            raise Exception("Connection pool not initialized")

    def release_connection(self, connection):
        if self.pool and connection:
            self.pool.putconn(connection)
            logging.info("Connection released back to the pool.")
        else:
            logging.error("Failed to release connection. Invalid pool or connection.")

    def close_pool(self):
        if self.pool:
            self.pool.closeall()
            logging.info("Connection pool closed.")
        else:
            logging.error("Failed to close connection pool. Pool not initialized.")

    def append(self, connection: Connection, table: Table, data: Iterable[tuple]):
        if not data:
            logging.info("No data to append.")
            return

        try:
            with connection.cursor() as cursor:
                logging.info(table.compose_insert_statement().as_string(context=connection))
                for batch in batched(data, table.batch_size):
                    cursor.executemany(table.compose_insert_statement(), batch)
                    logging.info(
                        f"Successfully inserted {len(batch)} records into {table.path.schema}.{table.path.name}"
                    )
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
            raise e

    def create_catalog_if_not_exists(self, connection: Connection, catalog: str):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [catalog]
            )
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(catalog))
                )
                logging.info(f"Catalog '{catalog}' created successfully.")
            else:
                logging.info(f"Catalog '{catalog}' already exists.")

    def get_current_catalog(self, connection: Connection) -> str:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database();")
            return cursor.fetchone()[0]

    def create_schema_if_not_exists(self, connection: Connection, schema: str):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    "SELECT 1 FROM information_schema.schemata WHERE schema_name = %s"
                ),
                [schema],
            )

            current_catalog = self.get_current_catalog(connection=connection)

            if not cursor.fetchone():
                cursor.execute(
                    sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema))
                )
                logging.info(
                    f"Schema '{schema}' created in catalog '{current_catalog}'."
                )
            else:
                logging.info(
                    f"Schema '{schema}' already exists in catalog '{current_catalog}'. Skipped."
                )

            connection.commit()

    def create_table_if_not_exists(self, connection: Connection, table: Table):
        schema = table.path.schema
        name = table.path.name

        with connection.cursor() as cursor:
            cursor.execute(table.compose_check_if_table_exists(), [schema, name])

            if not cursor.fetchone():
                logging.info(table.table_definition.as_string(context=connection))
                cursor.execute(table.table_definition)
                logging.info(f"Table '{name}' created in schema '{schema}'.")
            else:
                logging.info(
                    f"Table '{name}' already exists in schema '{schema}'. Skipped."
                )

    def create_type_if_not_exists(
        self, connection: Connection, custom_type: CustomType
    ):
        schema = custom_type.path.schema
        name = custom_type.path.name

        with connection.cursor() as cursor:
            cursor.execute(custom_type.compose_check_if_custom_type_exists())

            current_catalog = self.get_current_catalog(connection=connection)

            if not cursor.fetchone():
                self.create_schema_if_not_exists(
                    connection=connection, schema=custom_type.path.schema
                )

                cursor.execute(custom_type.compose_custom_type_definition())
                logging.info(
                    f"Type '{name}' created in schema '{schema}' in '{current_catalog}'."
                )
            else:
                logging.info(
                    f"Type '{name}' already exists in schema '{schema}' in '{current_catalog}'. Skipped."
                )

    def get_reserved_keywords(self, connection: Connection) -> list[str]:
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT word FROM pg_catalog.pg_get_keywords()"),
            )
            results = cursor.fetchall()
            return [item[0] for item in results]

    def validate_table_identifiers(self, connection: Connection, table: Table):
        reserved_keywords = self.get_reserved_keywords(connection=connection)
        column_names = [
            column.name for column in table.columns if isinstance(column, Column)
        ]
        custom_type_names = [
            column.path.name
            for column in table.columns
            if isinstance(column, CustomType)
        ]
        table_parts = [table.path.catalog, table.path.schema, table.path.name]
        for string in column_names + custom_type_names + table_parts:
            if string in reserved_keywords:
                raise ValueError(
                    f"{string} is not a valid name as it is one of postgres' reserved keywords"
                )

    def create_table(self, connection: Connection, table: Table):
        self.validate_table_identifiers(connection=connection, table=table)
        for custom_type in table.custom_types:
            self.create_type_if_not_exists(
                connection=connection, custom_type=custom_type
            )
        self.create_schema_if_not_exists(
            connection=connection, schema=table.path.schema
        )
        self.create_table_if_not_exists(connection=connection, table=table)

    def create_type(self, connection: Connection, custom_type: CustomType):
        self.create_schema_if_not_exists(
            connection=connection, schema=custom_type.path.schema
        )
        self.create_type_if_not_exists(connection=connection, custom_type=custom_type)

    # def handle_datetimeoffset(self, dto_value):
    #     # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    #     tup = struct.unpack(
    #         "<6hI2h", dto_value
    #     )  # e.g., (2017, 3, 16, 10, 35, 18, 500000000, -6, 0)
    #     return datetime(
    #         tup[0],
    #         tup[1],
    #         tup[2],
    #         tup[3],
    #         tup[4],
    #         tup[5],
    #         tup[6] // 1000,
    #         timezone(timedelta(hours=tup[7], minutes=tup[8])),
    #     )

    # def read(
    #     self,
    #     query: str,
    #     params: Optional[tuple] = None,
    #     batch_size: Optional[int] = 1000,
    #     database: Optional[str] = None,
    # ) -> Iterable[dict]:
    #     """Read data from database

    #     Parameters
    #         query: the query to run
    #         params: any params you might wish to use in the query
    #         batch_size: divide total read into smaller batches
    #         database: Useful when queries need a database context, such as when querying the INFORMATION_SCHEMA tables

    #     returns:
    #         Generator of dicts
    #     """
    #     self.conn.add_output_converter(-155, self.handle_datetimeoffset)
    #     with self.conn.cursor() as cursor:
    #         if database is not None:
    #             cursor.execute(f"USE {database};")
    #         if params is not None:
    #             cursor.execute(query, params)
    #         else:
    #             cursor.execute(query)

    #         columns = [column[0] for column in cursor.description]

    #         while True:
    #             rows = cursor.fetchmany(batch_size)
    #             if len(rows) == 0:
    #                 break
    #             for row in rows:
    #                 yield dict(zip(columns, row))

    # def execute(self, sql: str, *params: Any):
    #     """Internal function used to execute sql

    #     Parameters
    #         sql: the sql to run
    #     """
    #     with self.conn.cursor() as cursor:
    #         try:
    #             cursor.execute(sql, *params)
    #             cursor.commit()
    #         except Exception as e:
    #             raise Exception(f"Execute failed using query\n{sql}") from e

    # def write(
    #     self,
    #     sql: str,
    #     data: Iterable[dict],
    #     batch_size: int = 1000,
    #     fast_executemany: bool = False,
    # ):
    #     """Write to table from a generator of dicts

    #     Good to know: Pyodbc limitation for batch size: number_of_rows * number_of_columns < 2100

    #     Parameters:
    #         sql: the sql to run
    #         data: generator of dicts with the data itself
    #         batch_size: batches the data into manageable chunks for sql server
    #     """

    #     with self.conn.cursor() as cursor:
    #         cursor.fast_executemany = fast_executemany
    #         for rows in batched((tuple(row.values()) for row in data), batch_size):
    #             try:
    #                 cursor.executemany(sql, rows)
    #             except Exception as e:
    #                 raise Exception(f"Writing failed using query\n{sql}") from e

    # def create_schema_in_one_go(self, path: Path):
    #     """Pyodbc cant have these two statements in one go, so we have to execute them to the cursor separately"""
    #     with self.conn.cursor() as cursor:
    #         cursor.execute(f"USE {path.database};")
    #         cursor.execute(f"CREATE SCHEMA {path.schema};")

    # def merge_ddl(
    #     self,
    #     table: Table,
    # ) -> str:
    #     update_columns = table.non_unique_columns + table.default_columns

    #     if not table.unique_columns or not update_columns:
    #         raise ValueError("Unique columns and update columns cannot be empty.")

    #     on_conditions = " AND ".join(
    #         [f"target.{col.name} = source.{col.name}" for col in table.unique_columns]
    #     )
    #     update_clause = ", ".join(
    #         [f"target.{col.name} = source.{col.name}" for col in update_columns]
    #     )
    #     insert_columns = ", ".join([col.name for col in table._columns])
    #     insert_values = ", ".join([f"source.{col.name}" for col in table._columns])

    #     date_diff_condition = f"AND source.{table.destination_data_modified_column_name} > target.{table.destination_data_modified_column_name}"

    #     merge_ddl = f"""
    #         MERGE INTO {table.destination_path.to_str()} AS target
    #         USING {table.temp_table_path.to_str()} AS source
    #         ON {on_conditions}
    #         WHEN MATCHED {date_diff_condition} THEN
    #             UPDATE SET {update_clause}
    #         WHEN NOT MATCHED THEN
    #             INSERT ({insert_columns})
    #             VALUES ({insert_values});
    #     """

    #     return merge_ddl

    # def _schema_exists(self, path: Path) -> bool:
    #     """Create ddl to check if anything exists"""
    #     sql = f"""SELECT
    #         top 1 CASE
    #             WHEN EXISTS (
    #                 SELECT 1
    #                 FROM {path.database}.sys.schemas
    #                 WHERE name = '{path.schema}'
    #             )
    #             THEN 1
    #             ELSE 0
    #         END AS thing_exists;
    #         """

    #     schema_exists = False
    #     for row in self.read(query=sql):
    #         if row.get("thing_exists") == 1:
    #             return True

    #     return schema_exists

    # def _index_exists(self, path: Path, index_name: str) -> bool:
    #     """Create ddl to check if anything exists"""
    #     sql = f"SELECT i.name as index_name FROM {path.database}.sys.indexes i WHERE i.name = '{index_name}'"
    #     for row in self.read(query=sql):
    #         if row.get("index_name") == index_name:
    #             return True
    #     return False

    # def _table_exists(self, path: Path) -> bool:
    #     """Create ddl to check if anything exists"""
    #     sql = f"""SELECT
    #         top 1 CASE
    #             WHEN EXISTS (
    #                 SELECT 1
    #                 FROM [{path.database}].sys.tables t
    #                 LEFT JOIN [{path.database}].sys.schemas s on t.schema_id  = s.schema_id
    #                 WHERE t.name = '{path.table}'
    #                 AND s.name = '{path.schema}'
    #             )
    #             THEN 1
    #             ELSE 0
    #         END AS thing_exists;
    #         """

    #     table_exists = False
    #     for row in self.read(query=sql):
    #         if row.get("thing_exists") == 1:
    #             return True

    #     return table_exists

    # def _create_schema(self, path: Path):
    #     """Create schema if it does not already exist"""
    #     if not self._schema_exists(path=path):
    #         self.create_schema_in_one_go(path=path)

    # def create_table(self, path: Path, ddl: str, drop_first: Optional[bool] = False):
    #     """
    #     Parameters:
    #         Path: where the table would be located
    #         ddl: the ddl to create the table
    #         drop_first: do you want to drop the table before creating it (default: False)
    #     """

    #     if self._table_exists(path=path):
    #         if not drop_first:
    #             return
    #         self.execute(sql=f"DROP TABLE {path.to_str()};")

    #     self._create_schema(path=path)

    #     self.execute(sql=ddl)

    # def apply_indexes(self, table: Table, path: Path):
    #     """
    #     Apply indexes to a table if they do not already exist.
    #     This method iterates over the indexes defined for the table and checks if each index exists
    #     on the target database. If an index does not exist, it is created using the corresponding
    #     SQL definition.
    #     Args:
    #         table (Table): The table object containing the indexes to be applied.
    #         path (Path): The path object representing the destination database, schema, and table.
    #     """

    #     for index in table.indexes:
    #         if not self._index_exists(
    #             path=path, index_name=index.index_name(path=path)
    #         ):
    #             self.execute(sql=index.to_sql(path=path))

    # def truncate_write(self, table: Table, data: Iterable[dict]):
    #     """
    #     Perform a truncate and write operation for the table.
    #     This method creates the table, applies indexes, and writes the data into the table.
    #     It first truncates the existing data by recreating the table and then inserts the provided data.
    #     Args:
    #         table (Table): The table object representing the target table for the write operation.
    #         data (Iterable[dict]): The data to be written to the table, represented as an iterable of dictionaries.
    #     """
    #     path = table.destination_path
    #     self.create_table(path=path, ddl=table.table_ddl(path=path), drop_first=True)
    #     self.apply_indexes(table=table, path=path)

    #     self.write(
    #         sql=table.insert_sql(path=path),
    #         data=data,
    #         batch_size=table.batch_size,
    #         fast_executemany=table.fast_executemany,
    #     )

    # def append(self, table: Table, data: Iterable[dict]):
    #     """
    #     Perform an append write operation for the table.
    #     This method creates the table if it doesn't exist, applies indexes, and appends the provided data
    #     to the table.
    #     Args:
    #         table (Table): The table object representing the target table for the write operation.
    #         data (Iterable[dict]): The data to be appended to the table, represented as an iterable of dictionaries.
    #     """

    #     path = table.destination_path
    #     self.create_table(path=path, ddl=table.table_ddl(path=path))
    #     self.apply_indexes(table=table, path=path)

    #     self.write(
    #         sql=table.insert_sql(path=path),
    #         data=data,
    #         batch_size=table.batch_size,
    #         fast_executemany=table.fast_executemany,
    #     )

    # def merge(self, table: Table, data: Iterable[list]):
    #     """
    #     Creates destination schema + table if it does not already exist.
    #     Creates temporary and equivalent table to which data is inserted to.
    #     Data is then merged to destination table, and the temporary table is deleted.

    #     Parameters:
    #         table: the table to merge to
    #         data: the data itself
    #     """
    #     path = table.destination_path
    #     self.create_table(
    #         ddl=table.table_ddl(path=path),
    #         path=path,
    #     )
    #     self.apply_indexes(table=table, path=path)

    #     self.create_table(
    #         ddl=table.table_ddl(path=table.temp_table_path),
    #         path=table.temp_table_path,
    #     )
    #     self.apply_indexes(table=table, path=table.temp_table_path)

    #     self.write(
    #         sql=table.insert_sql(path=table.temp_table_path),
    #         data=data,
    #         batch_size=table.batch_size,
    #         fast_executemany=table.fast_executemany,
    #     )

    #     merge_sql = self.merge_ddl(
    #         table=table,
    #     )

    #     self.execute(sql=merge_sql)

    #     self.execute(sql=f"DROP TABLE {table.temp_table_path.to_str()};")

    # def write_using_modes(self, table: Table, data: Iterable[dict]):
    #     """
    #     Write data to a table using the specified write mode.

    #     This method delegates the writing operation to the appropriate method based on the table's write mode:
    #     - `APPEND`: Appends the data to the table.
    #     - `TRUNCATE_WRITE`: Clears the table and writes the data.
    #     - `MERGE`: Merges the data with the existing table content.

    #     Args:
    #         table (Table): The table object containing metadata, including the write mode.
    #         data (Iterable[dict]): The data to be written, represented as an iterable of dictionaries.
    #     """

    #     if table.write_mode == WriteMode.APPEND:
    #         self.append(table=table, data=data)
    #     elif table.write_mode == WriteMode.TRUNCATE_WRITE:
    #         self.truncate_write(table=table, data=data)
    #     elif table.write_mode == WriteMode.MERGE:
    #         self.merge(table=table, data=data)
