import sqlite3
import sys

def delete_restaurant_by_id(restaurant_id):
    """
    Delete a restaurant by its ID.

    :param restaurant_id: The ID of the restaurant to delete.
    """
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    # Execute the DELETE statement
    cursor.execute("""
        DELETE FROM restaurant
        WHERE restaurant_id = ?
    """, (restaurant_id,))

    # Provide feedback based on the operation
    if cursor.rowcount > 0:
        print(f"Restaurant with ID {restaurant_id} deleted successfully!")
    else:
        print(f"No restaurant found with ID {restaurant_id}.")

    conn.commit()
    conn.close()

# Handle command-line arguments
if __name__ == "__main__":
    # Check if the proper number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python delete_restaurant.py <restaurant_id>")
        sys.exit(1)

    # Get the restaurant_id from the command-line arguments
    try:
        restaurant_id = int(sys.argv[1])  # Cast to int for safety
        delete_restaurant_by_id(restaurant_id)
    except ValueError:
        print("Error: restaurant_id must be a valid integer.")
        sys.exit(1)
