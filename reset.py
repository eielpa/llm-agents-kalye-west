import pandas as pd

# Reset seats: all free
seats = pd.DataFrame([
    {"seat_id": "S1", "type": "counter", "capacity": 1, "status": "free"},
    {"seat_id": "S2", "type": "counter", "capacity": 1, "status": "free"},
    {"seat_id": "S3", "type": "counter", "capacity": 1, "status": "free"},
    {"seat_id": "T1", "type": "table",   "capacity": 2, "status": "free"},
    {"seat_id": "T2", "type": "table",   "capacity": 4, "status": "free"},
    {"seat_id": "T3", "type": "table",   "capacity": 4, "status": "free"},
    {"seat_id": "T4", "type": "table",   "capacity": 3, "status": "free"},
])
seats.to_csv("seating_system/seats.csv", index=False)

# Reset reservations: empty
reservations = pd.DataFrame(columns=["reservation_id", "seat_id", "party_size", "status", "timestamp"])
reservations.to_csv("seating_system/reservations.csv", index=False)

# Reset stock: original quantities
stock = pd.DataFrame([
    {"ingredient": "salmon",   "quantity": 10},
    {"ingredient": "tuna",     "quantity": 10},
    {"ingredient": "rice",     "quantity": 10},
    {"ingredient": "nori",     "quantity": 10},
    {"ingredient": "sesame",   "quantity": 10},
    {"ingredient": "cucumber", "quantity": 10},
])
stock.to_csv("kitchen_system/stock.csv", index=False)

print("Reset complete: seats, reservations and stock restored.")
