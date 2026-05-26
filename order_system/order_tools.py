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
            "status",
            "notes"
        ])
        df.to_csv(ORDERS_PATH, index=False)


def _load_menu():
    return pd.read_csv(MENU_PATH)


@tool("View Restaurant Menu")
def view_restaurant_menu(query: str = "") -> str:
    """Returns the restaurant menu with dishes, ingredients, allergens, and prep time."""
    try:
        df = _load_menu()
        return df.to_string(index=False)
    except Exception as e:
        return f"Error reading menu: {str(e)}"


@tool
def check_menu_and_allergens(query: str) -> str:
    """
    Pass a string formatted as 'Dish_Name|Allergen'.
    Checks if the dish exists and whether it contains the allergen.
    """
    try:
        dish_name, allergen = query.split("|")
        dish_name = dish_name.strip()
        allergen = allergen.strip().lower()

        df = _load_menu()
        dish = df[df["dish"].str.lower() == dish_name.lower()]

        if dish.empty:
            available = ", ".join(df["dish"].tolist())
            return (
                f"ORDER_REJECTED: Dish '{dish_name}' is not on the menu. "
                f"Available dishes are: {available}."
            )

        allergens = str(dish.iloc[0]["allergens"]).lower()
        allergen_list = [a.strip() for a in allergens.split(",") if a.strip()]

        if allergen != "none" and allergen in allergen_list:
            return (
                f"ORDER_NEEDS_ALTERNATIVE: {dish_name} contains {allergen}. "
                f"The order is not safe as requested."
            )

        return f"ORDER_SAFE: {dish_name} is on the menu and does not contain {allergen}."

    except Exception as e:
        return f"ORDER_ERROR: Ensure format is 'Dish|Allergen'. Details: {str(e)}"


@tool
def save_order(query: str) -> str:
    """
    Pass a string formatted as 'Dish_Name|Allergen|Status|Notes'.
    Saves an accepted or rejected order in order_system/orders.csv.
    Example: 'Salmon Nigiri|sesame|confirmed|safe alternative accepted'
    """
    try:
        _ensure_orders_file()

        parts = query.split("|")
        if len(parts) != 4:
            return "ORDER_ERROR: Ensure format is 'Dish|Allergen|Status|Notes'."

        dish_name, allergen, status, notes = [p.strip() for p in parts]

        orders_df = pd.read_csv(ORDERS_PATH)
        order_id = len(orders_df) + 1
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_order = pd.DataFrame([{
            "order_id": order_id,
            "created_at": created_at,
            "dish": dish_name,
            "allergen": allergen,
            "status": status,
            "notes": notes
        }])

        orders_df = pd.concat([orders_df, new_order], ignore_index=True)
        orders_df.to_csv(ORDERS_PATH, index=False)

        return (
            f"ORDER_SAVED: Order ID {order_id}. "
            f"Dish: {dish_name}. Status: {status}. Notes: {notes}."
        )

    except Exception as e:
        return f"ORDER_ERROR: Could not save order. Details: {str(e)}"


@tool("Check Order Status")
def check_order_status(query: str) -> str:
    """
    Pass an order id as a string.
    Returns the saved order status.
    """
    try:
        _ensure_orders_file()

        order_id = int(query.strip())
        orders_df = pd.read_csv(ORDERS_PATH)

        order = orders_df[orders_df["order_id"] == order_id]

        if order.empty:
            return f"ORDER_NOT_FOUND: No order found with ID {order_id}."

        row = order.iloc[0]

        return (
            f"ORDER_STATUS: Order {row['order_id']} for {row['dish']} "
            f"is currently '{row['status']}'. Notes: {row['notes']}"
        )

    except Exception as e:
        return f"ORDER_ERROR: Could not check order status. Details: {str(e)}"