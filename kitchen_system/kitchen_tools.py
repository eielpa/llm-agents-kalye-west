import pandas as pd
from crewai.tools import tool

@tool("Check and Update Stock")
def process_order_stock(dish_name: str, customer_allergy: str = "none", dry_run: bool = False) -> str:
    """Checks ingredient availability and allergen safety. 
    
    Set dry_run=True for preliminary safety checks without deducting stock.
    Set dry_run=False to finalize the order and permanently update inventory.
    """
    try:
        # --- AGGIUNGI QUESTO FIX DA QUI ---
        if isinstance(dry_run, str):
            dry_run = dry_run.strip().lower() in ['true', '1', 'yes']
        # --- A QUI ---

        menu_df = pd.read_csv("order_system/menu.csv")
        stock_df = pd.read_csv("kitchen_system/stock.csv")
        
        clean_dish = str(dish_name).strip().replace("'", "").replace('"', "")
        clean_allergy = str(customer_allergy).strip().lower()
        
        dish = menu_df[menu_df['dish'].str.lower() == clean_dish.lower()]
        if dish.empty:
            return f"Kitchen Error: Dish '{clean_dish}' is not on our menu."
            
        allergens = str(dish.iloc[0]['allergens']).split(',')
        cleaned_allergens = [a.strip().lower() for a in allergens if a.strip()]
        
        # Allergy checking layer - The Chef is the ultimate safety net
        if clean_allergy != "none" and clean_allergy in cleaned_allergens:
            ingredients_list = str(dish.iloc[0]['ingredients']).split(',')
            cleaned_ingredients = [i.strip().lower() for i in ingredients_list]
            can_remove = clean_allergy in cleaned_ingredients
            
            safe_dishes_df = menu_df[~menu_df['allergens'].astype(str).str.lower().str.contains(clean_allergy, na=False)]
            safe_alternatives = safe_dishes_df['dish'].tolist()
            
            feedback = f"I can't prepare {clean_dish} for this guest — the dish contains {clean_allergy}, which is flagged in their allergy profile. "
            if can_remove:
                feedback += f"We could make it without {clean_allergy} if needed. "
            if safe_alternatives:
                feedback += f"Safe alternatives from our menu: {', '.join(safe_alternatives)}."
            return feedback

        # Stock check layer
        ingredients = dish.iloc[0]['ingredients'].split(',')
        for ing in ingredients:
            ing = ing.strip()
            stock_item = stock_df[stock_df['ingredient'] == ing]
            if stock_item.empty or int(stock_item.iloc[0]['quantity']) < 1:
                return f"Unfortunately I can't prepare {clean_dish} right now — we're out of {ing}."

        if dry_run:
            return f"{clean_dish} is safe for this guest and we have all the ingredients in stock. Ready to prepare whenever confirmed."
            
        for ing in ingredients:
            ing = ing.strip()
            stock_df.loc[stock_df['ingredient'] == ing, 'quantity'] -= 1
            
        stock_df.to_csv("kitchen_system/stock.csv", index=False)
        prep_time = dish.iloc[0]['prep_time']
        return f"The {clean_dish} is now being prepared. It'll be ready in about {prep_time} minutes."

    except Exception as e:
        return f"Kitchen error: {str(e)}"