from sqlalchemy import create_engine, text


def test_select_queries(database_url: str):
    """
    Test a few SELECT queries to verify if data is properly inserted into the database.

    :param database_url: SQLite database URL (e.g., sqlite:///restaurant.db).
    """
    try:
        # Connect to the database
        engine = create_engine(database_url)
        with engine.connect() as connection:
            print("Connected to the database successfully!")

            # Test SELECT query on `client` table: Retrieve first 5 rows
            print("\nRunning SELECT query on `client` table:")
            result = connection.execute(text("SELECT * FROM client LIMIT 5"))
            rows = result.fetchall()
            for row in rows:
                print(row)

            # Test SELECT query on `order` table: Retrieve first 5 rows
            print("\nRunning SELECT query on `order` table:")
            result = connection.execute(
                text("SELECT * FROM 'order' LIMIT 5")
            )  # Use 'order' in quotes as it's a reserved word
            rows = result.fetchall()
            for row in rows:
                print(row)

            # Test JOIN query between `client` and `order` tables
            print("\nRunning SELECT query to join `client` and `order` tables:")
            query = """
            SELECT 
                client.first_name, 
                client.last_name, 
                client.email, 
                "order".order_date, 
                "order".total_amount
            FROM client
            INNER JOIN "order" ON client.client_id = "order".client_id
            LIMIT 5
            """
            result = connection.execute(text(query))
            rows = result.fetchall()
            for row in rows:
                print(row)

            # Test SELECT query on the `employee` table
            print("\nRunning SELECT query on `employee` table:")
            result = connection.execute(text("SELECT * FROM employee LIMIT 5"))
            rows = result.fetchall()
            for row in rows:
                print(row)

            # Test SELECT query on the `delivery` table
            print("\nRunning SELECT query on `delivery` table:")
            result = connection.execute(text("SELECT * FROM delivery LIMIT 5"))
            rows = result.fetchall()
            for row in rows:
                print(row)

    except Exception as e:
        print(f"An error occurred while executing SELECT queries: {e}")


if __name__ == "__main__":
    # Database URL (SQLite)
    database_url = "sqlite:///restaurant.db"  # Change this if your database URL differs

    # Run test SELECT queries
    test_select_queries(database_url)
