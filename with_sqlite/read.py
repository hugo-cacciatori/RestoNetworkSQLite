from sqlalchemy import create_engine, text
import pandas as pd


def query_table(database_url: str, table_name: str):
    """
    Query and display data from a given table in the database.

    :param database_url: SQLite database URL (e.g., sqlite:///restaurant.db).
    :param table_name: The name of the table to query.
    """
    try:
        # Connect to the database
        engine = create_engine(database_url)
        with engine.connect() as connection:
            print(f"\nFetching data from table: {table_name}")
            # Query data (use `text()` to execute raw SQL)
            query = text(
                f"SELECT * FROM {table_name} LIMIT 10;"
            )  # Limit the results to avoid large outputs
            data = pd.read_sql(query, connection)
            if data.empty:
                print(f"The table '{table_name}' is empty.")
            else:
                print(data)  # Display the fetched data
    except Exception as e:
        print(f"An error occurred while querying table '{table_name}': {e}")


def main():
    # Database URL
    database_url = "sqlite:///restaurant.db"

    # List of tables to query
    tables = [
        "restaurant",
        "menu_chez_martin",
        "employee",
        "supplier",
        "client_le_gourmet",
        "client_la_bonne_table",
        "client_chez_martin",
        "stocks_le_gourmet",
        "stocks_la_bonne_table",
        "stocks_chez_martin",
    ]

    # Query each table and display output
    for table in tables:
        query_table(database_url, table)


if __name__ == "__main__":
    main()
