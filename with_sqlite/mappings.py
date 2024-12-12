# Column Mappings
column_mappings = {
    "menu_chez_martin": {"nom": "name", "prix": "price"},
    "employé": {
        "Nom": "last_name",
        "Prénom": "first_name",
        "Poste": "position",
        "Restaurant_ID": "restaurant_id",
        "Date_Embauche": "hiring_date",
        "Salaire": "salary",
    },
    "fournisseur": {
        "nom": "name",
        "email": "email",
        "téléphone": "phone",
        "adresse": "address",
    },
    "clients": {
        "Nom": "last_name",
        "Prénom": "first_name",
        "Email": "email",
        "Téléphone": "phone",
        "Date_Inscription": "inscription_date",
        "Date_Commande": "order_date",
        "Montant_Total": "total_amount",
        "Date": "date",
    },
    "stocks": {
        "nom_produit": "product_name",
        "quantité": "quantity",
        "date_livraison": "delivery_date",
    },
}

# Position Mapping
position_mapping = {
    "Serveur": "WAITER",
    "Cuisinier": "COOK",
    "Chef Cuisinier": "HEAD COOK",
    "Responsable": "MANAGER",
    "Plongeur": "DISHWASHER",
}
