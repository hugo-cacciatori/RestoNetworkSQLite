from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
import os
import sqlite3
from mappings import column_mappings, position_mapping


def database_exists(database_url: str) -> bool:
    """
    Check if the database file exists.

    :param database_url: SQLite database URL (e.g., sqlite:///restaurant.db).
    :return: True if the database file exists, False otherwise.
    """
    # Extract the SQLite file path from the URL
    if database_url.startswith("sqlite:///"):
        db_file = database_url.replace("sqlite:///", "")
        return os.path.exists(db_file)
    return False


def apply_sql_script(database_url: str, script_path: str):
    """
    Apply a given SQL script to the database.

    :param database_url: SQLite database URL (e.g., sqlite:///restaurant.db).
    :param script_path: Path to the SQL script to execute.
    """
    # Create a database engine
    engine = create_engine(database_url)

    try:
        # Read the SQL script
        with open(script_path, "r") as file:
            sql_script = file.read()

        # Apply the SQL script using executescript
        with engine.connect() as connection:
            connection.connection.executescript(
                sql_script
            )  # Use executescript for multi-statement SQL

        print("Applied SQL script successfully.")
    except Exception as e:
        print(f"An error occurred while applying the SQL script: {e}")


def initialize_database(database_url: str, up_script_path: str):
    """
    Initialize the database using the provided up.sql script.

    :param database_url: SQLite database URL (e.g., sqlite:///restaurant.db).
    :param up_script_path: Path to the SQL script that creates the schema.
    """
    # Check if the database already exists
    if not database_exists(database_url):
        print("Database does not exist. Creating database and applying schema...")
        apply_sql_script(database_url, up_script_path)
    else:
        print("Database already exists. Skipping schema creation.")


def populate_database(database_url: str, excel_file_path: str):
    """
    Populate the database with data from an Excel file.

    :param database_url: SQLite database URL (e.g., sqlite:///restaurant.db).
    :param excel_file_path: Path to the Excel file containing the data to populate the database.
    """
    # Create a database engine
    engine = create_engine(database_url)

    # Load Excel data
    data = pd.ExcelFile(excel_file_path)

    # Menu table for Chez Martin
    menu_chez_martin_df = data.parse(sheet_name="menu_chez_martin")
    # Rename the French columns using mappings
    menu_chez_martin_df.rename(
        columns=column_mappings["menu_chez_martin"], inplace=True
    )
    # Insert data
    menu_chez_martin_df.to_sql(
        "menu_chez_martin", con=engine, if_exists="append", index=False
    )

    # Employee table
    employee_df = data.parse(sheet_name="employé")
    # Rename the French columns using mappings
    employee_df.rename(columns=column_mappings["employé"], inplace=True)

    # Apply position mapping
    employee_df["position"] = employee_df["position"].map(position_mapping)

    # Validate that all positions have been mapped
    if employee_df["position"].isnull().any():
        unmapped_positions = employee_df[employee_df["position"].isnull()]["position"]
        raise ValueError(f"Unmapped positions found: {unmapped_positions.tolist()}")

    # Format `hiring_date` as YYYY-MM-DD
    employee_df["hiring_date"] = pd.to_datetime(
        employee_df["hiring_date"], errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # Format `salary` as numeric (convert € to float)
    employee_df["salary"] = (
        employee_df["salary"]
        .str.replace("€", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # Insert employee data
    employee_df.to_sql("employee", con=engine, if_exists="append", index=False)

    # Supplier table
    fournisseur_df = data.parse(sheet_name="fournisseur")
    # Rename the French columns using mappings
    fournisseur_df.rename(columns=column_mappings["fournisseur"], inplace=True)
    # Insert data
    fournisseur_df.to_sql("supplier", con=engine, if_exists="append", index=False)

    # Client tables
    client_sheets = ["client_le_gourmet", "client_la_bonne_table", "client_chez_martin"]
    for sheet_name in client_sheets:
        client_df = data.parse(sheet_name=sheet_name)
        # Rename the French columns using mappings
        client_df.rename(columns=column_mappings["clients"], inplace=True)

        # Format dates
        client_df["inscription_date"] = pd.to_datetime(
            client_df["inscription_date"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")
        client_df["order_date"] = pd.to_datetime(
            client_df["order_date"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        # Insert data
        table_name = f"client_{sheet_name.split('_')[-1]}"
        client_df.to_sql(table_name, con=engine, if_exists="append", index=False)

    # Stock tables
    stock_sheets = ["stocks_le_gourmet", "stocks_la_bonne_table", "stocks_chez_martin"]
    for sheet_name in stock_sheets:
        stock_df = data.parse(sheet_name=sheet_name)
        # Rename the French columns using mappings
        stock_df.rename(columns=column_mappings["stocks"], inplace=True)

        # Format `delivery_date` as YYYY-MM-DD
        stock_df["delivery_date"] = pd.to_datetime(
            stock_df["delivery_date"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")
        # Insert data
        stock_df.to_sql(sheet_name, con=engine, if_exists="append", index=False)

    print("Database populated with data from the Excel file.")


def main():
    # Database URL (SQLite)
    database_url = "sqlite:///restaurant.db"

    # Paths to the SQL scripts and Excel file
    up_script_path = "up.sql"  # SQL script to create the schema
    excel_file_path = (
        "restaurant_data.xlsx"  # Excel file with the data to populate the tables
    )

    # Step 1: Initialize the database
    initialize_database(database_url, up_script_path)

    # Step 2: Populate the database
    populate_database(database_url, excel_file_path)


if __name__ == "__main__":
    main()
