import os


def drop_database(database_path: str):
    """
    Drop the SQLite database by deleting the database file.

    :param database_path: Path to the SQLite database file (e.g., restaurant.db).
    """
    try:
        if os.path.exists(database_path):
            os.remove(database_path)
            print(f"Database '{database_path}' has been deleted successfully.")
        else:
            print(f"Database '{database_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting the database: {e}")


if __name__ == "__main__":
    # Path to the SQLite database file
    database_path = "restaurant.db"

    # Drop the database (delete the file)
    drop_database(database_path)
