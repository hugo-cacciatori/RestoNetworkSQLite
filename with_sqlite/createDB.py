from sqlalchemy import create_engine
import pandas as pd
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


def database_exists(database_url: str) -> bool:
    """
    Check if the database file exists.

    :param database_url: SQLite database URL.
    :return: True if the database file exists, False otherwise.
    """
    if database_url.startswith("sqlite:///"):
        db_file = database_url.replace("sqlite:///", "")
        return os.path.exists(db_file)
    return False


def apply_sql_script(database_url: str, script_path: str):
    """
    Applies an SQL script to initialize the database.

    :param database_url: SQLite database URL.
    :param script_path: Path to the SQL script to execute.
    """
    engine = create_engine(database_url)

    try:
        with open(script_path, "r") as file:
            sql_script = file.read()

        with engine.connect() as connection:
            connection.connection.executescript(sql_script)

        print("Applied SQL script successfully.")
    except Exception as e:
        print(f"An error occurred while applying the SQL script: {e}")


def initialize_database(database_url: str, up_script_path: str):
    """
    Initialize the database using the provided SQL script.

    :param database_url: SQLite database URL.
    :param up_script_path: Path to the SQL schema script.
    """
    if not database_exists(database_url):
        print("Database does not exist. Creating database and applying schema...")
        apply_sql_script(database_url, up_script_path)
    else:
        print("Database already exists. Skipping schema creation.")


def get_restaurant_id(engine, restaurant_name):
    """
    Get the restaurant_id from the `restaurant` table based on the restaurant name.

    :param engine: SQLAlchemy engine.
    :param restaurant_name: Name of the restaurant.
    :return: The corresponding restaurant_id.
    """
    query = text("SELECT restaurant_id FROM restaurant WHERE name=:name")
    with engine.connect() as conn:
        result = conn.execute(query, {"name": restaurant_name}).fetchone()
    return result[0] if result else None


def populate_database(database_url: str, excel_file_path: str):
    engine = create_engine(database_url)

    try:
        data = pd.read_excel(excel_file_path, sheet_name=None)  # Load all sheets

        ### Populate `restaurant` table
        restaurant_df = data["restaurant"]
        restaurant_df.rename(
            columns={"Nom": "name", "Adresse": "address"}, inplace=True
        )
        restaurant_df.to_sql("restaurant", con=engine, if_exists="append", index=False)

        ### Populate `dish` table
        for sheet_name, restaurant_name in [
            ("menu_le_gourmet", "Le Gourmet"),
            ("menu_la_bonne_table", "La Bonne Table"),
            ("menu_chez_martin", "Chez Martin"),
        ]:
            if sheet_name in data:
                restaurant_id = get_restaurant_id(engine, restaurant_name)
                df = data[sheet_name]
                df["restaurant_id"] = restaurant_id
                df.rename(columns={"Nom": "name", "Prix": "price"}, inplace=True)
                df[["restaurant_id", "name", "price"]].to_sql(
                    "dish", con=engine, if_exists="append", index=False
                )

        ### Populate `client` table
        for sheet_name, restaurant_name in [
            ("client_le_gourmet", "Le Gourmet"),
            ("client_la_bonne_table", "La Bonne Table"),
            ("client_chez_martin", "Chez Martin"),
        ]:
            if sheet_name in data:
                # Get `restaurant_id` for the current restaurant
                restaurant_id = get_restaurant_id(engine, restaurant_name)

                # Load the data for the current sheet
                df = data[sheet_name]

                # Strip any extra spaces from column names for safety
                df.columns = df.columns.str.strip()

                # Debugging: Print the columns after cleaning
                print(
                    f"Processing sheet '{sheet_name}' with columns: {df.columns.tolist()}"
                )

                # Rename the columns to match the database schema
                df.rename(
                    columns={
                        "Prénom": "first_name",
                        "Nom": "last_name",
                        "Email": "email",
                        "Téléphone": "phone",
                        "Date_Inscription": "inscription_date",
                    },
                    inplace=True,
                )

                # Debugging: Print the renamed columns to ensure renaming worked
                print(f"Renamed columns for '{sheet_name}': {df.columns.tolist()}")

                # Add the `restaurant_id` column
                df["restaurant_id"] = restaurant_id

                # Define the relevant columns for the `client` table
                client_columns = [
                    "restaurant_id",
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "inscription_date",
                ]

                # Check if all required columns exist after renaming
                if all(col in df.columns for col in client_columns):
                    # Write the relevant data to the `client` table
                    df[client_columns].to_sql(
                        "client", con=engine, if_exists="append", index=False
                    )
                    print(
                        f"Successfully populated `client` table from sheet '{sheet_name}'."
                    )
                else:
                    # If required columns are missing, print error information
                    missing_cols = [
                        col for col in client_columns if col not in df.columns
                    ]
                    print(f"Missing columns in sheet '{sheet_name}': {missing_cols}")
                    raise ValueError(f"Missing columns: {missing_cols}")

        ### Populate `employee` table
        if "employé" in data:
            employee_df = data["employé"]

            # Rename columns to match the database schema
            employee_df.rename(
                columns={
                    "Prénom": "first_name",  # Correcting "Prénom" to "first_name"
                    "Nom": "last_name",
                    "Poste": "position",
                    "Date_Embauche": "hiring_date",
                    "Salaire": "salary",
                    "Restaurant_ID": "restaurant_name",
                },
                inplace=True,
            )

            # Translate French positions to English
            position_translation = {
                "Serveur": "WAITER",
                "Cuisinier": "COOK",
                "Plongeur": "DISHWASHER",
                "Responsable": "MANAGER",
                "Chef Cuisinier": "HEAD COOK",
            }
            employee_df["position"] = employee_df["position"].map(position_translation)

            # Debugging: Check if all position translations were successful
            print(f"Translated positions: {employee_df['position'].unique()}")

            # Map the `restaurant_id` using `restaurant_name`
            employee_df["restaurant_id"] = employee_df["restaurant_name"].apply(
                lambda name: get_restaurant_id(engine, name)
            )

            # Select relevant columns for the `employee` table
            employee_df = employee_df[
                [
                    "restaurant_id",
                    "first_name",
                    "last_name",
                    "position",
                    "hiring_date",
                    "salary",
                ]
            ]

            # Write the data to the `employee` table
            employee_df.to_sql("employee", con=engine, if_exists="append", index=False)

        ### Populate `order` table
        for sheet_name, restaurant_name in [
            ("client_le_gourmet", "Le Gourmet"),
            ("client_la_bonne_table", "La Bonne Table"),
            ("client_chez_martin", "Chez Martin"),
        ]:
            if sheet_name in data:
                # Load the data for the current sheet
                df = data[sheet_name]

                # Strip any extra spaces from column names for safety
                df.columns = df.columns.str.strip()

                # Debugging: Print column names before processing orders
                print(
                    f"Processing orders from sheet '{sheet_name}' with columns: {df.columns.tolist()}"
                )

                # Rename the relevant columns for the `order` table
                df.rename(
                    columns={
                        "Date_Commande": "order_date",
                        "Montant_Total": "total_amount",
                    },
                    inplace=True,
                )

                # Use a connection to fetch `email-to-client_id` mapping
                with engine.connect() as connection:
                    result = connection.execute(
                        text("SELECT email, client_id FROM client")
                    )
                    email_to_client_id_df = pd.DataFrame(
                        result.fetchall(), columns=["email", "client_id"]
                    )

                # Convert the DataFrame to a dictionary for fast lookup
                email_to_client_id = dict(email_to_client_id_df.values)

                # Map `client_id` to each order based on `email`
                df["client_id"] = df["email"].map(email_to_client_id)

                # Debugging: Check for unmatched emails
                if df["client_id"].isna().any():
                    print("Unmapped emails found in orders:")
                    print(
                        df[df["client_id"].isna()][
                            ["email", "order_date", "total_amount"]
                        ]
                    )

                # Drop rows with missing `order_date`, `total_amount`, or `client_id`
                initial_row_count = len(df)
                df = df.dropna(subset=["client_id", "order_date", "total_amount"])
                final_row_count = len(df)

                # Debugging: Show how many rows were dropped
                print(
                    f"Dropped {initial_row_count - final_row_count} rows due to missing data in 'client_id', 'order_date', or 'total_amount'."
                )

                # Select only order-related columns
                order_columns = ["client_id", "order_date", "total_amount"]

                # Check if required columns exist
                if all(col in df.columns for col in order_columns):
                    # Write data to the `order` table
                    df[order_columns].to_sql(
                        "order", con=engine, if_exists="append", index=False
                    )
                    print(
                        f"Successfully populated `order` table from sheet '{sheet_name}'."
                    )
                else:
                    missing_cols = [
                        col for col in order_columns if col not in df.columns
                    ]
                    print(
                        f"Missing columns for orders in sheet '{sheet_name}': {missing_cols}"
                    )
                    raise ValueError(f"Missing columns: {missing_cols}")

        ### Populate `supplier` table
        if "fournisseur" in data:
            supplier_df = data["fournisseur"]
            supplier_df.rename(
                columns={
                    "Nom": "name",
                    "Email": "email",
                    "Téléphone": "phone",
                    "Adresse": "address",
                },
                inplace=True,
            )
            supplier_df.to_sql("supplier", con=engine, if_exists="append", index=False)

        print("Populated database successfully.")

    except Exception as e:
        print(f"An error occurred while populating the database: {e}")


def main():
    # Database URL (SQLite)
    database_url = "sqlite:///restaurant.db"

    # Paths to the SQL schema and Excel file
    up_script_path = "up.sql"
    excel_file_path = "restaurant_data.xlsx"

    # Step 1: Initialize the database
    initialize_database(database_url, up_script_path)

    # Step 2: Populate the database with data
    populate_database(database_url, excel_file_path)


if __name__ == "__main__":
    main()
