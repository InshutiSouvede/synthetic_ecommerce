# ml/preprocess.py
import pandas as pd

def load_data(base_path: str):
    """Load and merge the main CSVs into one DataFrame for training."""
    customers = pd.read_csv(f"{base_path}/customers.csv")
    products = pd.read_csv(f"{base_path}/products.csv")
    orders = pd.read_csv(f"{base_path}/orders.csv")
    order_items = pd.read_csv(f"{base_path}/order_items.csv")
    
    # Merge order_items → orders → products → customers
    merged = (
        order_items
        .merge(orders, on="order_id", how="left")
        .merge(products, on="product_id", how="left")
        .merge(customers, on="customer_id", how="left")
    )

    # Drop columns you won't use
    merged = merged[[
        "quantity", "unit_price", "price", "category",
        "payment_method", "country", "total_amount"
    ]]

    # Handle missing values
    merged = merged.dropna()

    return merged