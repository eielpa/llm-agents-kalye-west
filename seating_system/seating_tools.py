import pandas as pd
from datetime import datetime
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

@tool("Update Seat Status")
def update_seat_status(query: str) -> str:
    """Updates the status of a seat. Pass format: 'seat_id|status' (e.g. 'T1|free')."""
    try:
        seat_id, status = query.split("|")
        seat_id, status = seat_id.strip(), status.strip()
        df = pd.read_csv("seating_system/seats.csv")
        if seat_id in df['seat_id'].values:
            df.loc[df['seat_id'] == seat_id, 'status'] = status
            df.to_csv("seating_system/seats.csv", index=False)
            return f"Seat {seat_id} status updated to '{status}'."
        return f"Seat {seat_id} not found."
    except ValueError:
        return "Format error. Use 'seat_id|status' (e.g. 'T1|free')."

@tool("Save Reservation")
def save_reservation(query: str) -> str:
    """Logs a reservation. Pass format: 'seat_id|party_size' (e.g. 'T1|2')."""
    try:
        seat_id, party_size = query.split("|")
        seat_id, party_size = seat_id.strip(), party_size.strip()
        seats_df = pd.read_csv("seating_system/seats.csv")
        if seat_id not in seats_df['seat_id'].values:
            return f"Reservation error: seat {seat_id} does not exist."
        df = pd.read_csv("seating_system/reservations.csv")
        reservation_id = len(df) + 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = pd.DataFrame([{
            "reservation_id": reservation_id,
            "seat_id": seat_id,
            "party_size": party_size,
            "status": "confirmed",
            "timestamp": timestamp
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("seating_system/reservations.csv", index=False)
        return f"Reservation {reservation_id} saved: seat {seat_id}, party of {party_size}, confirmed at {timestamp}."
    except ValueError:
        return "Format error. Use 'seat_id|party_size' (e.g. 'T1|2')."