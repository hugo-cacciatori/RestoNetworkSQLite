import sqlite3
import sys

def update_restaurant_by_id(restaurant_id, name=None, address=None):
    """
    Update the name and/or address of a restaurant by its ID.

    :param restaurant_id: The ID of the restaurant to update.
    :param name: The new name of the restaurant (optional).
    :param address: The new address of the restaurant (optional).
    """
    if name is None and address is None:
        print("Error: At least one of `name` or `address` must be provided to update.")
        return

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    # Generate the dynamic UPDATE statement based on provided fields
    update_fields = []
    params = []
    if name:
        update_fields.append("name = ?")
        params.append(name)
    if address:
        update_fields.append("address = ?")
        params.append(address)

    # Add restaurant_id to params for the WHERE clause
    params.append(restaurant_id)

    # Combine the update fields into a single SQL statement
    update_statement = f"""
        UPDATE restaurant
        SET {', '.join(update_fields)}
        WHERE restaurant_id = ?
    """

    # Execute the UPDATE statement
    cursor.execute(update_statement, params)

    # Provide feedback based on the operation
    if cursor.rowcount > 0:
        print(f"Restaurant with ID {restaurant_id} updated successfully!")
    else:
        print(f"No restaurant found with ID {restaurant_id}.")

    conn.commit()
    conn.close()


# Handle command-line arguments
if __name__ == "__main__":
    # Example command usage:
    # python update_restaurant.py 1 "New Name" "New Address"
    # Check if the proper number of arguments is provided
    if len(sys.argv) < 2:
        print("Usage: python update_restaurant.py <restaurant_id> [<name>] [<address>]")
        sys.exit(1)

    try:
        # Get the restaurant_id from the command-line
        restaurant_id = int(sys.argv[1])  # Cast to int for safety

        # Get the name and address if provided
        name = sys.argv[2] if len(sys.argv) > 2 else None
        address = sys.argv[3] if len(sys.argv) > 3 else None

        # Call the `update` function with the provided arguments
        update_restaurant_by_id(restaurant_id, name=name, address=address)
    except ValueError:
        print("Error: restaurant_id must be a valid integer.")
        sys.exit(1)
