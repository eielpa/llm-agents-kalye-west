import pandas as pd
from crewai import Agent, LLM
from crewai.tools import tool

groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.85 # High temperature for diverse runtime options
)

@tool("View Restaurant Menu")
def view_restaurant_menu(confirm: str = "yes") -> str:
    """Reads the menu file and returns the real options available to order."""
    try:
        df = pd.read_csv("order_system/menu.csv")
        return df.to_string(index=False)
    except Exception as e:
        return f"Error reading menu: {str(e)}"

class CustomerSystem:
    def customer_agent(self):
        return Agent(
            role="Restaurant Customer",
            goal="Secure a table, state your profile, and order a dish blindly from the menu.",
            backstory=(
                "You are a dining guest. At the start of the simulation, you must instantly invent a random party size (1-4) "
                "and a random allergy (sesame, fish, or none) and declare them to the restaurant immediately. "
                "When browsing the menu table, select ONE dish completely at random. Do NOT check if it triggers your allergy; "
                "be totally oblivious to the ingredients. If the kitchen flags an allergy block later, you must strictly pick "
                "ONLY ONE of the safe options they explicitly listed. Respond in exactly 1 short sentence."
            ),
            tools=[view_restaurant_menu],
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            llm=groq_llm
        )