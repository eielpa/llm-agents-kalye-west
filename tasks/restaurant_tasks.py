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
            description=(
                f"Read the customer's arrival log in {arrival_task.description}. "
                "Extract the party size, then call 'Check Seat Availability' with that party size. "
                "If no seat is available, stop immediately and reply 'No seats available for this party size.' "
                "If a seat is available, call 'Assign Seat' with the seat_id returned, "
                "then call 'Save Reservation' with format 'seat_id|party_size' to log the reservation. "
                "Only use seat IDs returned by the availability tool — never invent seat IDs."
            ),
            expected_output="A 1-sentence confirmation containing the assigned seat ID and the reservation ID, or a notice that no seats are available.",
            agent=agent,
            context=[arrival_task]
        )

    def customer_order_task(self, agent, seating_task):
        return Task(
            description=(
                "Read the seating result from the previous context. "
                "If the seating result contains 'No seats available', output exactly: "
                "'NO_SEATS: Cannot order, no table was assigned.' and stop — do not call any tool. "
                "Otherwise, execute the 'View Restaurant Menu' tool. "
                "Pick exactly ONE dish from the list completely at random (do not look at the allergen column, just choose blindly). "
                "State your order clearly to the staff in 1 sentence."
            ),
            expected_output="A 1-sentence order stating the exact dish name you chose.",
            agent=agent,
            context=[seating_task]
        )

    def waiter_order_validation_task(self, agent, arrival_task, order_task):
        return Task(
            description=(
                "Validate the customer's order before it goes to the kitchen. "
                "Use the previous context to extract: "
                "1) the customer's allergy profile, "
                "2) the exact dish ordered by the customer. "
                "Then call the tool named `check_menu_and_allergens` with input format 'Dish|Allergen'. "
                "If the dish is not on the menu, reject the order and do not save it. "
                "If the dish contains the customer's allergen, return ORDER_NEEDS_ALTERNATIVE and do not save it as confirmed. "
                "If the dish is safe, call the tool named `save_order` with format "
                "'Dish|Allergen|confirmed|validated by waiter'. "
                "Your final answer must start with exactly one of these labels: "
                "ORDER_CONFIRMED, ORDER_REJECTED, or ORDER_NEEDS_ALTERNATIVE. " \
                "As soon as the tool returns ORDER_NEEDS_ALTERNATIVE, write your final answer "
                "immediately starting with ORDER_NEEDS_ALTERNATIVE, include the dish name and "
                "the allergen, and stop — do not call any tool again."
                "Always include the exact dish name and allergy in your final answer."
            ),
            expected_output=(
                "A short order validation result. If safe, include the saved order ID. "
                "If unsafe or unavailable, explain why the order was not confirmed."
            ),
            agent=agent,
            context=[arrival_task, order_task]
        )

    def kitchen_allergy_check_task(self, agent, waiter_task):
        return Task(
            description=(
                "Read the Waiter order validation result from the previous context. "
                "If the Waiter result starts with ORDER_REJECTED, stop immediately and return the same rejection reason. "
                "Do not check stock, do not suggest alternatives, and do not prepare any dish. "
                "If the Waiter result starts with ORDER_NEEDS_ALTERNATIVE, suggest safe alternatives only. "
                "Do not prepare the unsafe dish. "
                "If the Waiter result starts with ORDER_CONFIRMED, extract the exact confirmed dish and allergy, then run the "
                "'Check and Update Stock' tool with dry_run set to True. "
                "If the tool returns a safety alert, repeat the safe alternatives. "
                "If it returns a Kitchen Check success, reply that the dish is approved."
            ),
            expected_output=(
                "If rejected: the same ORDER_REJECTED message from the Waiter. "
                "If alternative needed: safe alternatives only. "
                "If confirmed: the exact kitchen dry-run feedback."
            ),
            agent=agent,
            context=[waiter_task]
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
