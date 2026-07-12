# AssetFlow — Enterprise Asset & Resource Management System

Built for Odoo Hackathon 2026.

AssetFlow helps organizations track, allocate, book, and maintain physical assets
(laptops, vehicles, rooms, equipment) across departments — with role-based access,
audit visibility, and a maintenance workflow, instead of chasing this in spreadsheets.

## Team & Roles

| Area | Owner |
|---|---|
| Backend (API, DB, auth, business logic) | Rishabh |
| Frontend | *(add teammates here)* |

## Tech Stack

**Backend:** FastAPI · SQLAlchemy · SQLite · Pydantic · JWT (python-jose) · bcrypt (passlib)
**Frontend:** React (Vite) · React Router · Axios · Tailwind CSS · Recharts

## Roles

- **Admin** — full control, manages employees/roles, departments, categories
- **Asset Manager** — manages assets, allocations, transfers, maintenance
- **Department Head** — oversees department's assets and bookings
- **Employee** — requests bookings, views assigned assets, raises maintenance requests

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt

# One-time: bootstrap the first Admin account
python seed_admin.py
# -> admin@assetflow.com / Admin@123 (change after first login)

uvicorn app.main:app --reload --port 8000
```
API docs (Swagger UI): http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs at http://localhost:5173 by default. Make sure `frontend/.env` points at the
backend URL (`VITE_API_URL=http://localhost:8000` or similar).

## Core Features

- JWT authentication with role-guarded endpoints and bcrypt password hashing
- Employee, department, and asset-category management
- Asset registry with auto-generated tags (`AF-000N`) and lifecycle status
- **Allocation** — assign an asset to an employee; blocked with a 409 if the
  asset is already allocated (no double-booking of physical assets)
- **Booking** — reserve shared/bookable assets for a time window; overlap is
  checked with half-open-interval logic so back-to-back bookings are allowed
  but overlapping ones are rejected
- **Transfers** — move an asset between employees/departments with a request flow
- **Maintenance** — raise and track requests through a state machine
  (Pending → In Progress → Resolved, etc.)
- Notifications feed per user
- Reports: utilization, maintenance frequency, department summary, booking heatmap
- Every API response follows one envelope: `{ "success": bool, "message": str, "data": any }`

## API Overview

Full endpoint list and contract details are in [`backend/README.md`](backend/README.md)
and [`docs/api.md`](docs/api.md). Highlights:

| Method | Path | Notes |
|---|---|---|
| POST | `/auth/signup` / `/auth/login` | signup always creates an Employee; login returns a JWT |
| GET | `/dashboard` | KPI cards + overdue highlights |
| GET/POST/PUT/DELETE | `/employees`, `/departments`, `/categories`, `/assets` | directory & registry management |
| POST | `/allocation` | 409 if asset already allocated |
| POST | `/transfer` | raise a transfer request |
| POST | `/booking` | 409 on time-window overlap |
| POST | `/maintenance` | raise a request (starts Pending) |
| GET | `/notifications` | current user's feed |
| GET | `/reports` | utilization / maintenance / department / booking data |

## Project Structure

```
Odoo-Hackathon-2026/
├── backend/          FastAPI app (models, schemas, services, routers, auth)
│   ├── app/
│   ├── seed_admin.py
│   └── README.md
├── frontend/         React + Vite app
│   └── src/
│       ├── pages/    screens (scaffolded incrementally per domain)
│       ├── services/ API clients (one per domain)
│       ├── layouts/ routes/ context/ hooks/
│       └── components/common/
└── docs/
    └── api.md
```

## Known Limitations (hackathon scope)

- **Audit Cycle module** intentionally omitted — endpoint specs weren't finalized
  in time; the audit *log* (who-did-what trail) still exists and is captured.
- Frontend screens are being built incrementally; see `frontend/src/routes/AppRoutes.jsx`
  for which pages are wired vs. still scaffolded.
- SQLite is used for demo simplicity, not intended as the production datastore.

## Demo Flow

1. Log in as the seeded Admin (`admin@assetflow.com`)
2. View Dashboard KPIs
3. Register an asset, try allocating it twice → see the 409 block
4. Book the same asset for an overlapping time window → see the overlap block
5. Raise a maintenance request and walk through its status transitions