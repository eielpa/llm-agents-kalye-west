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
            description=f"Customer ordered {dish}. They are allergic to {allergen}. Verify if the dish is safe.",
            expected_output="A safety confirmation or a warning to the customer about their allergy.",
            agent=agent
        )

    def cook_order_task(self, agent, dish):
        return Task(
            description=f"The order for {dish} has been confirmed safe. Check the stock, deduct ingredients, and prepare the dish.",
            expected_output="Confirmation of preparation and estimated time, or notification of out-of-stock ingredients.",
            agent=agent
        )