from crewai import Agent, LLM
from seating_system.seating_tools import check_seat_availability, assign_seat

groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.0
)

class SeatingSystem:
    def seating_manager(self):
        return Agent(
            role="Seating Manager",
            goal="Seat arriving groups instantly using 1 sentence.",
            backstory="Host at Kalye West. You extract the group size, run your tools once, and output the table assignment.",
            tools=[check_seat_availability, assign_seat],
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            llm=groq_llm
        )
