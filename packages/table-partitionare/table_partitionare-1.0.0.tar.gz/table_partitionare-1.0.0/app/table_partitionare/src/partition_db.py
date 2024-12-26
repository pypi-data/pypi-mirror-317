from .funcs import read_from_existing_table, create_partitioned_table, partition_existing_empty_table
from .help_funcs import map_python_to_sql, assign_segment_md5, get_connection_string
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, MetaData, Table


class TablePartitioner:
    def __init__(self, cred_path, num_partition):
        
        connection_string = get_connection_string(env_file_path=cred_path)
        
        self.connection_string = connection_string
        self.num_partition = num_partition
        self.engine = create_engine(self.connection_string)
        self.metadata = MetaData()
        
    def read_table(self, table_name):
        return read_from_existing_table(self.engine, table_name=table_name)

    def assign_partitions(self, records, partition_column):

        for record in records:
            record["part"] = assign_segment_md5(
                record[partition_column], self.num_partition
            )
        return records

    def create_partitioned_table(self, table_name, records):

        columns = {c: type(t) for c, t in zip(records[0].keys(), records[0].values())}
        sql_columns = map_python_to_sql(columns)
        print(f"Inferred SQL columns: {sql_columns}")
        
        create_partitioned_table(
            self.engine, table_name, sql_columns, self.num_partition
        )
        
    def move_data_to_partitioned_table(self, table_name, data):

        if not data:
            raise ValueError("Data is empty. Nothing to insert.")
        
        try:
            # Reflect the table structure from the database
            self.metadata.reflect(bind=self.engine)
            table = self.metadata.tables.get(table_name)
            
            if table is None:
                raise ValueError(f"Table {table_name} does not exist.")
            
            # Insert data using SQLAlchemy's connection
            with self.engine.connect() as connection:
                connection.execute(table.insert(), data)
            
            print(f"Data successfully inserted into {table_name}.")
        
        except SQLAlchemyError as e:
            print(f"Error inserting data into {table_name}: {e}")
            raise



