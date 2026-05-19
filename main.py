import os
import litellm

# 1. Set your Groq API Key
os.environ["GROQ_API_KEY"] = "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"

# 2. BUG FIX: Intercept the API call and remove the 'cache_breakpoint' property 
# that CrewAI forces into the messages, which Groq's API strictly rejects.
original_completion = litellm.completion

def patched_completion(*args, **kwargs):
    if 'messages' in kwargs:
        for message in kwargs['messages']:
            if isinstance(message, dict):
                message.pop('cache_breakpoint', None)  # Strips the broken key safely
    return original_completion(*args, **kwargs)

litellm.completion = patched_completion

# 3. Now import the rest of the CrewAI components safely
from crewai import Crew, Process
from agents.restaurant_agents import RestaurantAgents
from tasks.restaurant_tasks import RestaurantTasks

def run_simulation(party_size: int, requested_dish: str, customer_allergen: str):
    print(f"\n--- NEW CUSTOMER SCENARIO ---")
    print(f"Party Size: {party_size} | Order: {requested_dish} | Allergy: {customer_allergen}\n")

    # Initialize Agents
    agents = RestaurantAgents()
    seating_agent = agents.seating_manager()
    waiter_agent = agents.waiter()
    chef_agent = agents.sushi_chef()

    # Initialize Tasks
    tasks = RestaurantTasks()
    seat_task = tasks.seat_customer_task(seating_agent, party_size)
    order_task = tasks.take_order_task(waiter_agent, requested_dish, customer_allergen)
    cook_task = tasks.cook_order_task(chef_agent, requested_dish)

    # Form the Crew
    restaurant_crew = Crew(
        agents=[seating_agent, waiter_agent, chef_agent],
        tasks=[seat_task, order_task, cook_task],
        process=Process.sequential
    )

    # Execute Workflow
    result = restaurant_crew.kickoff()
    
    print("\n--- FINAL SYSTEM OUTPUT ---")
    print(result)

if __name__ == "__main__":
    run_simulation(party_size=2, requested_dish="Tuna Roll", customer_allergen="sesame")