import os
from datetime import datetime
import pandas as pd
from crewai.tools import tool

MENU_PATH = "order_system/menu.csv"
ORDERS_PATH = "order_system/orders.csv"


def _ensure_orders_file():
    if not os.path.exists(ORDERS_PATH):
        df = pd.DataFrame(columns=[
            "order_id",
            "created_at",
            "dish",
            "allergen",
            "status"
        ])
        df.to_csv(ORDERS_PATH, index=False)


@tool("Check Menu and Allergens")
def check_allergens(query: str) -> str:
    """Pass a string formatted as 'Dish_Name|Allergen'. Checks if the dish contains the allergen."""
    try:
        dish_name, allergen = query.split('|')
        df = pd.read_csv(MENU_PATH)
        dish = df[df['dish'].str.lower() == dish_name.strip().lower()]

        if dish.empty:
            return "Dish not found on the menu."

        allergens = str(dish.iloc[0]['allergens']).split(',')

        if allergen.strip().lower() in [a.strip().lower() for a in allergens]:
            return f"WARNING: {dish_name} contains {allergen}!"

        return f"Safe: {dish_name} does not contain {allergen}."

    except Exception:
        return "Error reading menu. Ensure format is 'Dish|Allergen'."


@tool("Save Customer Order")
def save_order(query: str) -> str:
    """
    Pass a string formatted as 'Dish_Name|Allergen|Status'.
    Saves the customer order in order_system/orders.csv.
    Example: 'Tuna Roll|sesame|confirmed'
    """
    try:
        _ensure_orders_file()

        parts = query.split('|')
        if len(parts) != 3:
            return "Error saving order. Ensure format is 'Dish|Allergen|Status'."

        dish_name, allergen, status = [p.strip() for p in parts]

        orders_df = pd.read_csv(ORDERS_PATH)

        order_id = len(orders_df) + 1
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_order = pd.DataFrame([{
            "order_id": order_id,
            "created_at": created_at,
            "dish": dish_name,
            "allergen": allergen,
            "status": status
        }])

        orders_df = pd.concat([orders_df, new_order], ignore_index=True)
        orders_df.to_csv(ORDERS_PATH, index=False)

        return f"Order saved successfully. Order ID: {order_id}. Status: {status}."

    except Exception as e:
        return f"Error saving order: {str(e)}"


@tool("Check Order Status")
def check_order_status(query: str) -> str:
    """
    Pass an order id as a string.
    Returns the status of the order.
    Example: '1'
    """
    try:
        _ensure_orders_file()

        order_id = int(query.strip())
        orders_df = pd.read_csv(ORDERS_PATH)

        order = orders_df[orders_df["order_id"] == order_id]

        if order.empty:
            return "Order not found."

        status = order.iloc[0]["status"]
        dish = order.iloc[0]["dish"]

        return f"Order {order_id} for {dish} is currently: {status}."

    except Exception as e:
        return f"Error checking order status: {str(e)}"