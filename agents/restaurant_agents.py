from crewai import Agent, LLM
from order_system.order_tools import view_restaurant_menu, check_menu_and_allergens, save_order, check_order_status
from kitchen_system.kitchen_tools import process_order_stock

groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.0
)

class RestaurantAgents:
    def waiter(self):
        return Agent(
            role="Waiter",
            goal="Validate customer orders for safety and menu availability, then communicate the result clearly and naturally.",
            backstory=(
                "You are a professional and friendly restaurant waiter. You check every order carefully for allergens "
                "and menu availability, and you always speak to guests in a warm, natural tone — never using codes or technical labels."
            ),
            tools=[view_restaurant_menu, check_menu_and_allergens, save_order, check_order_status],
            verbose=True,
            allow_delegation=False,
            max_iter=2,
            llm=groq_llm
        )

    def sushi_chef(self):
        return Agent(
            role="Sushi Chef",
            goal="Check stock and cook safe food, communicating results in natural, human language.",
            backstory=(
                "You are the head sushi chef. You use your tools to check ingredients and safety, "
                "then translate the results into clear, natural speech — as you would when briefing your team or speaking to a guest. "
                "Never invent dish names or assume success. Never copy tool output verbatim."
            ),
            tools=[process_order_stock],
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            llm=groq_llm
        )
