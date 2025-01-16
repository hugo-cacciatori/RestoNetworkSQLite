import sqlite3
import sys

def create_restaurant(name, address):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    # Insert the new restaurant, letting SQLite auto-generate the restaurant_id
    cursor.execute("""
        INSERT INTO restaurant (name, address)
        VALUES (?, ?)
    """, (name, address))

    conn.commit()
    conn.close()
    print(f"Restaurant '{name}' created successfully!")

# Handle command-line arguments
if __name__ == "__main__":
    # Check if the proper number of arguments is provided (script name, name, address)
    if len(sys.argv) != 3:
        print("Usage: python create_restaurant.py <name> <address>")
        sys.exit(1)

    # Read name and address from command-line arguments
    restaurant_name = sys.argv[1]
    restaurant_address = sys.argv[2]

    # Call the function with the provided arguments
    create_restaurant(restaurant_name, restaurant_address)
