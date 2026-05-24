from crewai import Task

class RestaurantTasks:
    def customer_arrival_task(self, agent):
        return Task(
            description=(
                "Step 1: Invent a random party size (1 to 4) and a random allergy profile (sesame, fish, or none). "
                "Step 2: Greet the host and declare BOTH your party size and your allergy profile clearly so the restaurant has it on record."
            ),
            expected_output="A 1-sentence greeting stating party size and allergy profile.",
            agent=agent
        )

    def seat_customer_task(self, agent, arrival_task):
        return Task(
            description=f"Read the customer's arrival log in {arrival_task.description}. Extract the party size, verify availability, and assign the seat using your tools.",
            expected_output="A 1-sentence confirmation containing the assigned seat ID.",
            agent=agent,
            context=[arrival_task]
        )

    def customer_order_task(self, agent, seating_task):
        return Task(
            description=(
                f"You are seated at your table via {seating_task.description}. Execute the 'View Restaurant Menu' tool. "
                "Pick exactly ONE dish from the list completely at random (do not look at the allergen column, just choose blindly). "
                "State your order clearly to the staff in 1 sentence."
            ),
            expected_output="A 1-sentence order stating the exact dish name you chose.",
            agent=agent,
            context=[seating_task]
        )

    def kitchen_allergy_check_task(self, agent, arrival_task, order_task):
        return Task(
            description=(
                f"Extract the customer's allergy from {arrival_task.description} and their ordered dish from {order_task.description}. "
                "Run the 'Check and Update Stock' tool passing both variables, with 'dry_run' set to True. "
                "If the tool returns a SAFETY ALERT block, stop and repeat those alternative suggestions to the customer. "
                "If it returns a Kitchen Check success, reply that the dish is approved."
            ),
            expected_output="The exact feedback or safety alternatives returned by the kitchen tool.",
            agent=agent,
            context=[arrival_task, order_task]
        )

    def customer_decision_task(self, agent, kitchen_task):
        return Task(
            description=(
                f"Read the kitchen response in {kitchen_task.description}. If the kitchen blocked your item, "
                "respond by choosing exactly ONE option from the safe paths they provided. "
                "If the kitchen approved your original dish, simply reply: 'Please proceed with the original order'."
            ),
            expected_output="A 1-sentence final decision statement specifying a single menu item.",
            agent=agent,
            context=[kitchen_task]
        )

    def finalize_cooking_task(self, agent, decision_task):
        return Task(
            description=(
                f"Read the customer's definitive choice from {decision_task.description}. "
                "Run the 'Check and Update Stock' tool for that exact dish name with 'dry_run' set to False to permanently update stock and begin cooking. "
                "CRITICAL: You must output the exact text returned by the tool as your final answer. Do not invent dish names."
            ),
            expected_output="The exact success or preparation time message returned by the stock tool.",
            agent=agent,
            context=[decision_task]
        )