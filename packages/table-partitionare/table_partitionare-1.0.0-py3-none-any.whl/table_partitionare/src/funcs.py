from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, text
from sqlalchemy.exc import SQLAlchemyError


from sqlalchemy.orm import sessionmaker
connection_string = "postgresql+psycopg2://postgres:apolo@localhost:5432/partition_project"

def read_from_existing_table(engine, table_name):
    """
    Reads data from an existing PostgreSQL table using SQLAlchemy.

    Args:
        connection_string (str): Database connection string in the format:
            'postgresql+psycopg2://username:password@host:port/database'
        table_name (str): Name of the table to read from.

    Returns:
        list[dict]: List of rows as dictionaries, where column names are keys.
    """
    try:

        # Reflect the existing table
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query all rows from the table
        results = session.query(table).all()

        # Convert rows to dictionaries
        rows = [{column: getattr(row, column) for column in table.columns.keys()} for row in results]

        return rows

    except Exception as e:
        print(f"Error reading from PostgreSQL: {e}")
        return []

    # finally:
    #     # Close the session
    #     session.close()

type_mapping = {
    String: 'VARCHAR',
    Integer: 'INTEGER',
    # Add more mappings as necessary
}

def create_partitioned_table(engine, table_name, columns, n_partitions):
    """
    Creates a table from the provided dictionary and partitions it by the 'part' column.

    Args:
        engine: SQLAlchemy engine.
        table_name (str): The name of the table to create.
        columns (dict): A dictionary where keys are column names and values are SQLAlchemy column types.
        n_partitions (int): The number of partitions to create.
    """
    metadata = MetaData()

    # Dynamically create the column definitions from the dictionary
    column_definitions = []
    for column_name, column_type in columns.items():
        # Get the PostgreSQL equivalent type from the mapping
        column_sql_type = type_mapping.get(column_type, None)
        if column_sql_type is None:
            raise ValueError(f"Unsupported column type: {column_type}")
        column_definitions.append(f"{column_name} {column_sql_type}")

    # Build the CREATE TABLE statement using the mapped column types
    column_defs_sql = ", ".join(column_definitions)
    
    # Create the main partitioned table SQL query
    create_table_sql = f"""
    CREATE TABLE {table_name}_partitioned (
        {column_defs_sql}
    )
    PARTITION BY LIST (part);
    """

    # Execute the SQL to create the partitioned table
    with engine.connect() as connection:
        connection.execute(text(create_table_sql))
        connection.commit()

    # Create partitions based on the range of 'part' column (1 to n_partitions)
    for i in range(1, n_partitions + 1):
        partition_name = f"{table_name}_part_{i}"
        partition_query = f"""
        CREATE TABLE {partition_name} PARTITION OF {table_name}_partitioned
        FOR VALUES IN ({i});
        """
        
        # Execute the partition creation
        with engine.connect() as connection:
            connection.execute(text(partition_query))
            connection.commit()

    print(f"Table '{table_name}_partitioned' partitioned by 'part' with {n_partitions} partitions created successfully!")







        




