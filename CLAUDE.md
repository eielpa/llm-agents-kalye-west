# llm-agents-kalye-west — Note di sessione

## Cos'è il progetto
Simulazione autonoma di un ristorante sushi (Kalye West) costruita con **CrewAI** + **Groq LLaMA-3.3-70b-versatile**.
Progetto universitario di gruppo — 3 persone + parte comune.

## Team
| Persona | Parte | Branch remoto |
|---|---|---|
| **Simone** (sib002) | `seating_system/` | `seating_system` |
| **Luca** | `order_system/` | `order-system-luca` |
| **Eugenio** (eielpa) | `kitchen_system/` | `kitchen` |
| Tutti | `customer_system/`, `main.py`, `tasks/` | — |

Repo remoto: `https://github.com/eielpa/llm-agents-kalye-west.git`

---

## Architettura target (da WhatsApp + organizzazione.txt)

```
llm-agents-kalye-west/
├── main.py
├── CLAUDE.md
├── seating_system/
│   ├── __init__.py
│   ├── seating_agent.py       ← SeatingSystem class
│   ├── seating_tools.py       ← check_seat_availability, assign_seat, update_seat_status (manca)
│   ├── seats.csv
│   └── reservations.csv       ← manca
├── order_system/              ← Luca
│   ├── __init__.py            ← manca
│   ├── waiter_agent.py        ← manca (agente ancora in agents/restaurant_agents.py)
│   ├── order_tools.py
│   ├── menu.csv
│   └── orders.csv             ← manca
├── kitchen_system/            ← Eugenio
│   ├── __init__.py            ← manca
│   ├── chef_agent.py          ← manca (agente ancora in agents/restaurant_agents.py)
│   ├── kitchen_tools.py
│   └── stock.csv
├── customer_system/           ← parte comune, da creare
│   ├── __init__.py
│   ├── customer_agent.py      ← da spostare da agents/
│   └── demo_scenarios.py      ← manca
├── agents/                    ← cartella temporanea, sparirà quando tutti spostano i loro agenti
│   ├── restaurant_agents.py   ← rimangono solo waiter (Luca) e sushi_chef (Eugenio)
│   └── customer_agent.py      ← da spostare in customer_system/
└── tasks/
    └── restaurant_tasks.py
```

---

## Pipeline di esecuzione (6 step sequenziali)

```
Step 1 — Customer Agent
  Inventa party size (1-4) e allergia (fish/sesame/none)
  Output: "Party of 2, fish allergy"

Step 2 — Seating Manager (SIMONE)
  Chiama check_seat_availability(party_size)
  Chiama assign_seat(seat_id)
  Output: "Tavolo T1 assegnato"

Step 3 — Customer Agent
  Legge menu, sceglie piatto a caso
  Output: "Voglio il Tuna Roll"

Step 4 — Chef Agent (dry_run=True)
  Controlla allergia vs piatto senza toccare lo stock
  Se blocco: lista alternative sicure

Step 5 — Customer Agent
  Se bloccato sceglie alternativa, altrimenti conferma originale

Step 6 — Chef Agent (dry_run=False)
  Scala stock su stock.csv, restituisce tempo preparazione
```

---

## Stato attuale (25/05/2026)

### Fatto
- [x] Struttura base del progetto funzionante
- [x] `seating_system/seating_agent.py` creato — `SeatingSystem` class con `seating_manager()`
- [x] `seating_system/__init__.py` creato
- [x] `seating_system/seating_tools.py` — `check_seat_availability`, `assign_seat`
- [x] `seating_system/seats.csv` — S1,S2,S3 (counter 1p), T1 (table 2p), T2 (table 4p, già occupied)
- [x] `agents/restaurant_agents.py` — rimosso `seating_manager()`, rimangono waiter e chef
- [x] `main.py` — aggiornato import da `SeatingSystem`

### Manca (parte Simone)
- [ ] `seating_system/seating_tools.py` — aggiungere `update_seat_status(seat_id, status)` per liberare posti
- [ ] `seating_system/reservations.csv` — log prenotazioni (reservation_id, seat_id, party_size, status, timestamp)
- [ ] Aggiornare Step 2 in `tasks/restaurant_tasks.py` per salvare su reservations.csv

### Manca (Luca — order)
- [ ] `order_system/__init__.py`
- [ ] `order_system/waiter_agent.py` con classe `OrderSystem`
- [ ] `order_system/orders.csv`
- [ ] Spostare `waiter()` da `agents/restaurant_agents.py` a `order_system/waiter_agent.py`
- [ ] Task del waiter mancante nella pipeline (tra Step 3 e Step 4)

### Manca (Eugenio — kitchen)
- [ ] `kitchen_system/__init__.py`
- [ ] `kitchen_system/chef_agent.py` con classe `KitchenSystem`
- [ ] Spostare `sushi_chef()` da `agents/restaurant_agents.py` a `kitchen_system/chef_agent.py`

---

## Setup ambiente

### Requisito critico: Python 3.12 (NON 3.14)
CrewAI richiede `Python >=3.10, <3.14`. Python 3.14 non è supportato.

```powershell
# Scarica Python 3.12 da python.org, poi:
py --list                        # verifica che 3.12 sia presente
py -3.12 -m pip install crewai litellm pandas
py -3.12 main.py                 # per runnare
```

### API Key Groq
1. Registrati su console.groq.com (gratuito)
2. Sezione API Keys → Create API Key → copia `gsk_...`
3. Imposta su Windows:

```powershell
# Permanente (una volta sola, poi riavvia il terminale)
[System.Environment]::SetEnvironmentVariable("GROQ_API_KEY", "gsk_tuachiave...", "User")
```

---

## Note tecniche importanti

- Tutti i path nei tool sono **relativi** — il progetto va sempre lanciato dalla root `llm-agents-kalye-west/`
- `seats.csv` viene modificato su disco ad ogni run — resettare manualmente `T2` a `free` se si vuole ripartire da zero
- `stock.csv` viene decrementato ad ogni run completato (Step 6) — stessa cosa
- Il `waiter` agent esiste ma è **orfano** (nessun task assegnato) — Luca dovrà aggiungere il suo task
- `temperature=0.0` su tutti gli agenti tranne il Customer (`0.85`) per avere comportamento deterministico
