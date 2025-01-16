import sqlite3

def read_restaurants():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM restaurant")
    rows = cursor.fetchall()
    
    conn.close()

    print("Restaurants:")
    for row in rows:
        print(row)

# Example usage
read_restaurants()
