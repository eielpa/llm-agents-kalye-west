import pandas as pd
from crewai.tools import tool

@tool("Check and Update Stock")
def process_order_stock(dish_name: str) -> str:
    """Checks if there are enough ingredients for a dish and deducts them if possible."""
    menu_df = pd.read_csv("order_system/menu.csv")
    stock_df = pd.read_csv("kitchen_system/stock.csv")
    
    dish = menu_df[menu_df['dish'].str.lower() == dish_name.lower()]
    if dish.empty:
        return f"Dish {dish_name} unknown."
        
    ingredients = dish.iloc[0]['ingredients'].split(',')
    
    # Check availability
    for ing in ingredients:
        ing = ing.strip()
        stock_item = stock_df[stock_df['ingredient'] == ing]
        if stock_item.empty or int(stock_item.iloc[0]['quantity']) < 1:
            return f"Cannot prepare {dish_name}: Out of {ing}."
            
    # Deduct stock
    for ing in ingredients:
        ing = ing.strip()
        stock_df.loc[stock_df['ingredient'] == ing, 'quantity'] -= 1
        
    stock_df.to_csv("kitchen_system/stock.csv", index=False)
    prep_time = dish.iloc[0]['prep_time']
    return f"{dish_name} is being prepared. Estimated time: {prep_time} minutes."