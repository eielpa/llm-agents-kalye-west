import pandas as pd
from crewai.tools import tool

@tool("Check Seat Availability")
def check_seat_availability(party_size: int) -> str:
    """Checks if there is a free seat for the requested party size."""
    df = pd.read_csv("seating_system/seats.csv")
    available = df[(df['status'] == 'free') & (df['capacity'] >= int(party_size))]
    
    if not available.empty:
        seat = available.iloc[0]
        return f"Seat {seat['seat_id']} ({seat['type']}, capacity: {seat['capacity']}) is available."
    return "No seats available for this party size."

@tool("Assign Seat")
def assign_seat(seat_id: str) -> str:
    """Assigns a seat and marks it as occupied in the system."""
    df = pd.read_csv("seating_system/seats.csv")
    if seat_id in df['seat_id'].values:
        df.loc[df['seat_id'] == seat_id, 'status'] = 'occupied'
        df.to_csv("seating_system/seats.csv", index=False)
        return f"Seat {seat_id} successfully assigned and marked as occupied."
    return "Seat not found."