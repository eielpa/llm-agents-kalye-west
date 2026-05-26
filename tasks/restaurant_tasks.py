from crewai import Task

class RestaurantTasks:
    def customer_arrival_task(self, agent):
        return Task(
            description=(
                "Step 1: Invent a random party size (1 to 4) and a random allergy profile (sesame, fish, or none). "
                "Step 2: Greet the host naturally and declare both your party size and your allergy profile clearly."
            ),
            expected_output="A natural 1-sentence greeting stating party size and allergy profile.",
            agent=agent
        )

    def seat_customer_task(self, agent, arrival_task):
        return Task(
            description=(
                "From the previous step, extract the party size the customer declared. "
                "Call 'Check Seat Availability' with that party size. "
                "If no seat is available, politely let the customer know. "
                "If a seat is available, call 'Assign Seat' with the seat_id returned, "
                "then call 'Save Reservation' with format 'seat_id|party_size' to log the reservation. "
                "Only use seat IDs returned by the availability tool — never invent seat IDs. "
                "Respond as a friendly host would."
            ),
            expected_output="A natural 1-sentence confirmation with the assigned seat and reservation ID, or a polite notice that no seats are available.",
            agent=agent,
            context=[arrival_task]
        )

    def customer_order_task(self, agent, seating_task, menu_string=""):
        return Task(
            description=(
                "Read the seating result from the previous step. If no seat was available, stop.\n"
                f"Otherwise, look at this restaurant menu:\n\n{menu_string}\n\n"
                "Pick exactly ONE dish from this list completely at random. "
                "Tell the staff your order in one natural sentence. "
                "Do NOT mention your allergy or party size — just state the dish you want."
            ),
            expected_output="A 1-sentence order with only the dish name — do not repeat allergy or party size.",
            agent=agent,
            context=[seating_task]
        )

    def waiter_order_validation_task(self, agent, arrival_task, order_task):
        return Task(
            description=(
                "Validate the customer's order before it goes to the kitchen. "
                "From the previous context extract: 1) the customer's allergy, 2) the exact dish ordered. "
                "Call check_menu_and_allergens with format 'Dish|Allergen'. "
                "If the dish is not on the menu, politely decline and explain. "
                "If the dish contains the allergen, politely tell the guest you cannot serve it and that they need to choose a safe alternative — do not save the order. "
                "If the dish is safe, call save_order with format 'Dish|Allergen|confirmed|validated by waiter' and confirm the order. "
                "Respond in friendly, natural English as a waiter speaking to a guest. "
                "As soon as the tool indicates an allergy conflict, write your response immediately and stop — do not call any tool again."
            ),
            expected_output=(
                "A natural, friendly sentence. If safe: confirm the order was placed. "
                "If unsafe: explain the issue and mention that an alternative is needed. "
                "If not on menu: politely decline."
            ),
            agent=agent,
            context=[arrival_task, order_task]
        )

    def kitchen_allergy_check_task(self, agent, waiter_task):
        return Task(
            description=(
                "Read the waiter's response from the previous step.\n\n"
                "1. If the waiter said the dish is not on the menu, stop immediately and pass on the same message.\n"
                "2. If the waiter said the dish contains an allergen and a safe alternative is needed, run 'Check and Update Stock' "
                "ONCE with the original dish name and the customer's allergen, with dry_run=True. "
                "The tool will return safe alternatives automatically — report those alternatives to the team. "
                "Do NOT run the tool again for each alternative.\n"
                "3. If the waiter confirmed the order, run 'Check and Update Stock' with dry_run=True for the confirmed dish. "
                "If the tool flags an allergy issue, list the safe alternatives. "
                "If the tool confirms the dish is safe and in stock, approve it.\n"
                "Respond naturally as a chef briefing the team."
            ),
            expected_output=(
                "A natural sentence from the chef. If rejected: pass on the rejection. "
                "If an alternative is needed: list the safe options returned by the tool. "
                "If confirmed: confirm the dish is approved and ready."
            ),
            agent=agent,
            context=[waiter_task]
        )

    def customer_decision_task(self, agent, waiter_task, kitchen_task):
        return Task(
            description=(
                "Read the waiter's and kitchen's responses from the previous steps carefully. "
                "If the waiter said the dish cannot be served due to an allergy conflict, "
                "and the kitchen offered safe alternatives, you MUST choose exactly ONE dish from those alternatives — "
                "you cannot have the original dish. State only the dish name you are choosing. "
                "Only say 'Please proceed with the original order' if both the waiter AND the kitchen confirmed "
                "the original dish is fully safe and approved."
            ),
            expected_output="A 1-sentence statement naming the exact dish you are ordering.",
            agent=agent,
            context=[waiter_task, kitchen_task]
        )

    def finalize_cooking_task(self, agent, order_task, decision_task):
        return Task(
            description=(
                "From the previous steps, identify the exact dish the customer finally chose. "
                "If the customer named a specific dish, use that exact name. "
                "If the customer said 'proceed with the original order', look at the original order context to find the exact dish name. "
                "Also extract the customer's allergen from context. "
                "Call 'Check and Update Stock' with dry_run=False and the allergen to begin cooking. "
                "Translate the tool's response into a natural sentence for the guest — do not copy the tool output verbatim."
            ),
            expected_output="A natural sentence confirming the dish being prepared and the estimated time.",
            agent=agent,
            context=[order_task, decision_task]
        )
