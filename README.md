# Campus Lost & Found + Event Seat Reservation APIs

This repository contains two FastAPI REST API tasks for a college campus:

- **Task 1:** Campus Lost & Found API
- **Task 2:** Campus Event Seat Reservation API

Both tasks use **SQLite** for persistent storage and **SQLModel** for database models and operations.

## Technologies Used

- Python 3.10+
- FastAPI
- Uvicorn
- SQLModel
- SQLite
- Pydantic validation
- Swagger UI / OpenAPI

## Project Structure

```text
campus_fastapi_assignment/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── items.py
│       └── events.py
│
├── screenshots/
│   └── README.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Open PowerShell in the project folder.

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate it

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Run the FastAPI Application

From the project root:

```powershell
python -m uvicorn app.main:app --reload
```

The API will normally run at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The SQLite database file `campus.db` is automatically created in the project root when the application starts.

## Task 1 - Lost & Found Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/items` | Create a lost/found report |
| GET | `/items` | Get all reports |
| GET | `/items/{item_id}` | Get one report |
| PUT | `/items/{item_id}` | Update a report |
| DELETE | `/items/{item_id}` | Delete a report |
| GET | `/items/status/{item_status}` | Filter by Lost, Found or Returned |
| GET | `/items/category/{category}` | Filter by category |

### Example POST /items body

```json
{
  "title": "Black Wallet",
  "description": "Black leather wallet found near the library entrance.",
  "category": "Accessories",
  "location": "Central Library",
  "reported_by": "Rahul Sharma",
  "status": "Found"
}
```

### Task 1 application logic

1. **SQLite creation:** `database.py` uses `create_engine("sqlite:///./campus.db")`. `SQLModel.metadata.create_all(engine)` runs during FastAPI startup.
2. **SQLModel:** `Item` is a SQLModel table model. FastAPI receives validated request data and a SQLModel `Session` inserts, queries, updates and deletes database records.
3. **Filtering:** status filtering uses `select(Item).where(Item.status == item_status)`. Category filtering uses `select(Item).where(Item.category == category)`.
4. **Missing item:** `session.get(Item, item_id)` is checked. If no record exists, the API returns HTTP `404 Not Found`.
5. **Status validation:** `ItemStatus` is an enum containing only `Lost`, `Found`, and `Returned`. FastAPI/Pydantic rejects other values with HTTP `422 Unprocessable Entity`.

## Task 2 - Event & Reservation Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/events` | Create an event |
| GET | `/events` | Get all events |
| GET | `/events/{event_id}` | Get one event |
| PUT | `/events/{event_id}` | Update an event |
| DELETE | `/events/{event_id}` | Delete an event |
| POST | `/events/{event_id}/reserve` | Reserve a seat |
| GET | `/events/{event_id}/reservations` | Get reservations for an event |
| DELETE | `/reservations/{reservation_id}` | Cancel a reservation |
| GET | `/events/{event_id}/availability` | Get capacity/booked/remaining seats |

### Example POST /events body

```json
{
  "title": "AI Workshop",
  "venue": "Seminar Hall 2",
  "capacity": 2,
  "organizer": "CSE Department",
  "status": "Open"
}
```

### Example POST /events/{event_id}/reserve body

```json
{
  "student_name": "Shubham Tyagi",
  "roll_number": "2200320100123",
  "email": "shubham@example.com"
}
```

### Example availability response

```json
{
  "capacity": 2,
  "booked": 1,
  "remaining": 1
}
```

### Task 2 application logic

1. **Event existence:** before a reservation is created, `session.get(Event, event_id)` checks whether the event exists. A missing event returns HTTP `404`.
2. **Booked and remaining seats:** reservations are selected using the event ID. `booked` is the number of matching reservations and `remaining = capacity - booked`.
3. **Overbooking prevention:** when `booked >= event.capacity`, the API rejects the reservation with HTTP `409 Conflict`.
4. **Closed event prevention:** if `event.status` is `Closed`, the API rejects the reservation with HTTP `400 Bad Request`.
5. **SQLModel Session:** FastAPI injects a SQLModel `Session` using `get_session()`. The session performs `get`, `select`, `add`, `delete`, `commit` and `refresh` operations against SQLite.

## Validation

Examples of invalid requests:

- Empty title/description -> HTTP `422`
- Invalid item status such as `"Missing"` -> HTTP `422`
- Capacity `0` or negative -> HTTP `422`
- Invalid email -> HTTP `422`
- Reservation for a missing event -> HTTP `404`
- Reservation for a closed event -> HTTP `400`
- Reservation when the event is full -> HTTP `409`

## Proof of Work / Screenshots

The `screenshots` folder should contain screenshots captured from Swagger UI after running the application.

Recommended screenshot names:

1. `01_post_item.png`
2. `02_get_items.png`
3. `03_get_item_by_id.png`
4. `04_put_item.png`
5. `05_delete_item.png`
6. `06_status_filter.png`
7. `07_category_filter.png`
8. `08_invalid_item_validation.png`
9. `09_post_event.png`
10. `10_get_events.png`
11. `11_successful_reservation.png`
12. `12_event_reservations.png`
13. `13_event_availability.png`
14. `14_cancel_reservation.png`
15. `15_full_event_error.png`

Each screenshot should clearly show the endpoint, request body (where applicable), status code, and response.

## Important Demo Tip

For Task 2, create an event with a small capacity such as `2`. Then create exactly two reservations. Use the availability endpoint to show:

```json
{
  "capacity": 2,
  "booked": 2,
  "remaining": 0
}
```

Then make a third reservation. Swagger should show HTTP `409` with:

```json
{
  "detail": "Event is full. No more reservations are allowed."
}
```

This proves that the API prevents overbooking.

## GitHub Upload

From PowerShell, inside this project folder:

```powershell
git init
git add .
git commit -m "Complete FastAPI campus assignment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/campus-fastapi-assignment.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

Do **not** upload `.venv/` or `campus.db`; they are excluded by `.gitignore`.

After adding screenshots, run:

```powershell
git add .
git commit -m "Add API proof screenshots"
git push
```
