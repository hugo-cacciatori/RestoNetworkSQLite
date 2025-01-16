import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output
import dash

# Database connection (replace 'restaurant_data.db' with the actual path to your SQLite database)
DATABASE_PATH = "restaurant.db"

def fetch_data_from_db(query, params=None):
    """Helper function to fetch data from SQLite database."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        if params:
            return pd.read_sql_query(query, conn, params=params)
        return pd.read_sql_query(query, conn)

# Fetch Data From SQLite Database and Populate DataFrames
# 1. Last Orders Data
orders_query = """
    SELECT 
        client.first_name || ' ' || client.last_name AS Client,
        "orders".order_date AS Date_Commande,
        "orders".total_amount AS Montant_Total
    FROM
        "orders"
    JOIN
        client
    ON 
        "orders".client_id = client.client_id
    ORDER BY 
        "orders".order_date DESC
"""

orders_data = fetch_data_from_db(orders_query)

# 2. Inventory Data
inventory_query = """
    SELECT 
        delivery.product_name AS Nom_Produit,
        delivery.quantity AS Quantité,
        delivery.delivery_date AS Date_Livraison
    FROM 
        delivery
"""
inventory_data = fetch_data_from_db(inventory_query)

# 3. Employee Data
employee_query = """
    SELECT
        employee.position AS Poste,
        COUNT(employee.employee_id) AS Count,
        AVG(employee.salary) AS Average_Salary,
        restaurant.name AS Restaurant
    FROM
        employee
    JOIN
        restaurant
    ON
        employee.restaurant_id = restaurant.restaurant_id
    GROUP BY
        employee.position, restaurant.name
"""
employee_data = fetch_data_from_db(employee_query)

employee_distribution_query = """
    SELECT
        restaurant.name AS Restaurant,
        COUNT(employee.employee_id) AS Employee_Count
    FROM
        employee
    JOIN
        restaurant
    ON
        employee.restaurant_id = restaurant.restaurant_id
    GROUP BY
        restaurant.name
"""
restaurant_employee_distribution = fetch_data_from_db(employee_distribution_query)
restaurant_employee_distribution_dict = dict(
    zip(restaurant_employee_distribution["Restaurant"], restaurant_employee_distribution["Employee_Count"])
)

# 4. Menu Data
menu_query = """
    SELECT
        dish.name AS Nom,
        dish.price AS Prix
    FROM 
        dish
"""
menu_data = fetch_data_from_db(menu_query)

# Initialize Dash App
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(
    [
        html.H1("Restaurant Insights Dashboard", style={"textAlign": "center"}),

        # Bar Chart for Last Orders
        html.Div(
            [
                html.H3("Recent Orders and Total Amount"),
                dcc.Graph(
                    id="recent-orders-bar-chart",
                    figure=px.bar(
                        orders_data,
                        x="Client",
                        y="Montant_Total",
                        color="Date_Commande",
                        title="Recent Orders and Total Amount",
                        labels={
                            "Montant_Total": "Total Amount (€)",
                            "Client": "Client",
                            "Date_Commande": "Order Date",
                        },
                    ).update_layout(xaxis_type="category"),
                ),
            ]
        ),

        # Pie Chart for Revenue Distribution
        html.Div(
            [
                html.H3("Revenue Distribution by Food Item"),
                dcc.Graph(
                    id="revenue-pie-chart",
                    figure=px.pie(
                        menu_data,
                        names="Nom",
                        values="Prix",
                        title="Revenue Distribution by Food Item",
                    ),
                ),
            ]
        ),

        # Donut Chart for Employee Distribution
        html.Div(
            [
                html.H3("Employee Distribution by Restaurant"),
                dcc.Graph(
                    id="employee-donut-chart",
                    figure=go.Figure(
                        go.Pie(
                            labels=list(restaurant_employee_distribution_dict.keys()),
                            values=list(restaurant_employee_distribution_dict.values()),
                            hole=0.5,
                        )
                    ).update_layout(title_text="Employee Distribution by Restaurant"),
                ),
            ]
        ),

        # Bar Chart for Inventory Levels
        html.Div(
            [
                html.H3("Inventory Stock Levels"),
                dcc.Graph(
                    id="inventory-bar-chart",
                    figure=px.bar(
                        inventory_data,
                        x="Nom_Produit",
                        y="Quantité",
                        color="Nom_Produit",
                        title="Inventory Stock Levels",
                        labels={"Quantité": "Stock Quantity", "Nom_Produit": "Product"},
                    ),
                ),
            ]
        ),

        # Bar Chart for Employee Count by Role
        html.Div(
            [
                html.H3("Employee Count by Role"),
                dcc.Graph(
                    id="employee-count-bar-chart",
                    figure=px.bar(
                        employee_data,
                        x="Poste",
                        y="Count",
                        color="Poste",
                        title="Employee Count by Role",
                        labels={"Count": "Number of Employees", "Poste": "Role"},
                    ),
                ),
            ]
        ),

        # Bar Chart for Average Salary by Role
        html.Div(
            [
                html.H3("Average Salary by Role"),
                dcc.Graph(
                    id="average-salary-bar-chart",
                    figure=px.bar(
                        employee_data,
                        x="Poste",
                        y="Average_Salary",
                        color="Poste",
                        title="Average Salary by Role",
                        labels={"Average_Salary": "Salary (€)", "Poste": "Role"},
                    ),
                ),
            ]
        ),
    ]
)

# Run the App
if __name__ == "__main__":
    app.run_server(debug=True)
