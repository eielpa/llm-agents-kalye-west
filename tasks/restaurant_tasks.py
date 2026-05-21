from crewai import Task

class RestaurantTasks:
    def seat_customer_task(self, agent, party_size):
        return Task(
            description=f"A party of {party_size} just walked in. Check if there is an available seat for them. If so, assign it.",
            expected_output="Confirmation of the assigned seat ID or an apology that the restaurant is full.",
            agent=agent
        )

    def take_order_task(self, agent, dish, allergen):
        return Task(
            description=(
                f"Customer ordered {dish}. They are allergic to {allergen}. "
                f"First, verify if the dish is safe using the allergy checking tool. "
                f"If the dish is safe, save the order with status 'confirmed'. "
                f"If the dish contains the allergen, ask the Sushi Chef if the dish can be modified safely. "
                f"If the Chef confirms it can be made safely, save the order with status 'confirmed_without_allergen'. "
                f"If it cannot be made safely, do not save the order."
            ),
            expected_output=(
                "A clear confirmation or warning. If the order is accepted, include the saved order ID and status."
            ),
            agent=agent
        )

    def cook_order_task(self, agent, dish):
        return Task(
            description=f"The order for {dish} has been confirmed safe. Check the stock, deduct ingredients, and prepare the dish.",
            expected_output="Confirmation of preparation and estimated time, or notification of out-of-stock ingredients.",
            agent=agent
        )