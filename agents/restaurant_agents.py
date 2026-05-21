from crewai import Agent
from seating_system.seating_tools import check_seat_availability, assign_seat
from order_system.order_tools import check_allergens, save_order, check_order_status
from kitchen_system.kitchen_tools import process_order_stock

class RestaurantAgents:
    def seating_manager(self):
        return Agent(
            role="Seating Manager",
            goal="Efficiently manage restaurant capacity and seat customers.",
            backstory="You are a polite and highly organized host at Kalye West Sushi. You ensure parties are seated appropriately without double-booking.",
            tools=[check_seat_availability, assign_seat],
            verbose=True,
            allow_delegation=False,
            llm="groq/llama-3.3-70b-versatile"
        )

    def waiter(self):
        return Agent(
            role="Waiter",
            goal="Take customer orders accurately, check allergies, save confirmed orders, and track order status.",            
            backstory="You are a knowledgeable sushi waiter. You protect customers by verifying menu items against their dietary restrictions and recording safe orders.",
            tools=[check_allergens, save_order, check_order_status],
            verbose=True,
            allow_delegation=True,
            llm="groq/llama-3.3-70b-versatile"
        )

    def sushi_chef(self):
        return Agent(
            role="Sushi Chef",
            goal="Prepare high-quality sushi while managing ingredient stock.",
            backstory="You are an experienced Itamae. You strictly monitor your ingredient inventory and never promise a dish you cannot make.",
            tools=[process_order_stock],
            verbose=True,
            allow_delegation=False,
            llm="groq/llama-3.3-70b-versatile"
        )