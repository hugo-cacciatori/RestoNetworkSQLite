```mermaid

erDiagram
    CLIENT {
        int id PK
        string first_name
        string last_name
        string email
        string phone
    }

    ORDER {
        int id PK
        int client_id FK
        date order_date
        decimal total_amount
    }

    PRODUCT {
        int product_id PK
        string product_name
        int quantity
        date delivery_date
    }

    RESTAURANT {
        int restaurant_id PK
        string restaurant_name
    }

    EMPLOYEE {
        int employee_id PK
        string first_name
        string last_name
        string email
        string phone
        date hire_date
    }

    EMPLOYEE_ASSIGNMENT {
        int id PK
        int employee_id FK
        int restaurant_id FK
        date start_date
        date end_date
    }

    SUPPLIER {
        int supplier_id PK
        string supplier_name
        string phone
        string email
        string address
    }

    SUPPLIER_PRODUCTS {
        int supplier_id FK
        int product_id FK
    }

    CLIENT ||--o{ ORDER : places
    ORDER }o--o| PRODUCT : contains
    EMPLOYEE ||--o{ EMPLOYEE_ASSIGNMENT : assigned_to
    RESTAURANT ||--o{ EMPLOYEE_ASSIGNMENT : hosts
    SUPPLIER ||--o{ SUPPLIER_PRODUCTS : supplies
    PRODUCT ||--o{ SUPPLIER_PRODUCTS : is_supplied_by
