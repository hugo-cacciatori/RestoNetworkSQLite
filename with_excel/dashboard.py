import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sample Orders Data to simulate "last orders" dataset (replace with actual file parsing)
orders_data = pd.DataFrame(
    {
        "Client": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "Date_Commande": [
            "2024-11-01",
            "2024-11-03",
            "2024-11-01",
            "2024-11-05",
            "2024-11-04",
        ],
        "Montant_Total (€)": [45.5, 80.0, 30.0, 60.0, 75.0],
    }
)

# Inventory Data (no changes)
inventory_data = pd.DataFrame(
    {
        "Nom_Produit": [
            "Tomates",
            "Pâtes",
            "Beurre",
            "Oeufs",
            "Farine",
            "Poisson",
            "Sel",
        ],
        "Quantité": [38, 112, 30, 95, 67, 131, 180],
        "Date_Livraison": ["2024-12-10"] * 7,
    }
)

# Employee Data (no changes)
employee_data = pd.DataFrame(
    {
        "Poste": ["Serveur", "Cuisinier", "Plongeur", "Responsable"],
        "Count": [5, 4, 3, 4],
        "Average_Salary": [1720, 2060, 1650, 2650],
        "Restaurant": ["Chez Martin", "Le Gourmet", "La Bonne Table", "Chez Martin"],
    }
)

# Menu Data (no changes)
menu_data = pd.DataFrame(
    {
        "Nom": ["Burger Gourmet", "Salade César", "Pizza Margherita", "Poulet Curry"],
        "Prix (€)": [10, 13.54, 15.32, 18.68],
    }
)

restaurant_employee_distribution = {
    "Le Gourmet": 6,
    "Chez Martin": 8,
    "La Bonne Table": 7,
}

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(
    [
        html.H1("Restaurant Insights Dashboard", style={"textAlign": "center"}),
        # Bar Chart for last orders
        html.Div(
            [
                html.H3("Recent Orders and Total Amount"),
                dcc.Graph(
                    id="recent-orders-bar-chart",
                    figure=px.bar(
                        orders_data.sort_values("Date_Commande", ascending=False),
                        x="Client",
                        y="Montant_Total (€)",
                        color="Date_Commande",
                        title="Recent Orders and Total Amount",
                        labels={
                            "Montant_Total (€)": "Total Amount (€)",
                            "Client": "Client",
                            "Date_Commande": "Order Date",
                        },
                    ).update_layout(
                        xaxis_type="category"
                    ),  # Ensure x-axis is categorical
                ),
            ]
        ),
        # Pie Chart for revenue distribution
        html.Div(
            [
                html.H3("Revenue Distribution by Food Item"),
                dcc.Graph(
                    id="revenue-pie-chart",
                    figure=px.pie(
                        menu_data,
                        names="Nom",
                        values="Prix (€)",
                        title="Revenue Distribution by Food Item",
                    ),
                ),
            ]
        ),
        # Donut Chart for employee distribution
        html.Div(
            [
                html.H3("Employee Distribution by Restaurant"),
                dcc.Graph(
                    id="employee-donut-chart",
                    figure=go.Figure(
                        go.Pie(
                            labels=list(restaurant_employee_distribution.keys()),
                            values=list(restaurant_employee_distribution.values()),
                            hole=0.5,  # Turns it into a donut chart
                        )
                    ).update_layout(title_text="Employee Distribution by Restaurant"),
                ),
            ]
        ),
        # Bar Chart for inventory levels
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
        # Bar Chart for employee count by role
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
        # Bar Chart for average salary by role
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

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
