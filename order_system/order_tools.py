import pandas as pd
from crewai.tools import tool

@tool("Check Menu and Allergens")
def check_allergens(query: str) -> str:
    """Pass a string formatted as 'Dish_Name|Allergen'. Checks if the dish contains the allergen."""
    try:
        dish_name, allergen = query.split('|')
        df = pd.read_csv("order_system/menu.csv")
        dish = df[df['dish'].str.lower() == dish_name.strip().lower()]
        
        if dish.empty:
            return "Dish not found on the menu."
            
        allergens = str(dish.iloc[0]['allergens']).split(',')
        if allergen.strip().lower() in [a.strip().lower() for a in allergens]:
            return f"WARNING: {dish_name} contains {allergen}!"
        return f"Safe: {dish_name} does not contain {allergen}."
    except Exception as e:
        return "Error reading menu. Ensure format is 'Dish|Allergen'."