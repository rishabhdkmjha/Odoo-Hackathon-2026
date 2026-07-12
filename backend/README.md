# AssetFlow Backend

FastAPI + SQLAlchemy + SQLite backend for the AssetFlow Enterprise Asset & Resource
Management System. Frontend consumes this purely as REST/JSON — no server-rendered pages.

## Quick start

```bash
cd backend
pip install -r requirements.txt

# One-time: create the first Admin account (signup always creates a plain
# Employee, by design — this is the bootstrap account that promotes everyone else)
python seed_admin.py
# -> admin@assetflow.com / Admin@123  (change the password after first login)

uvicorn app.main:app --reload --port 8000
```

API docs (Swagger): http://localhost:8000/docs

## Response envelope

Every endpoint — success or error — returns:
```json
{ "success": true, "message": "...", "data": ... }
```
Validation errors (422) put the Pydantic error list in `data`.

## Auth

`POST /auth/login` returns a JWT. Send it as `Authorization: Bearer <token>` on every
other request. Token payload: `{"sub": "<user_id>", "role": "<role>"}`, expires in
`ACCESS_TOKEN_EXPIRE_MINUTES` (default 8h, tuned for a hackathon demo).

Roles: `admin`, `asset_manager`, `department_head`, `employee`.
Signup (`POST /auth/signup`) always creates an `employee`. Only an Admin can promote
someone via `PUT /employees/{id}` — that's the only place roles change.

## Endpoints delivered (frontend contract — unchanged names/paths)

| Method | Path | Notes |
|---|---|---|
| POST | /auth/signup | employee-only self-signup |
| POST | /auth/login | returns JWT + user |
| GET | /dashboard | KPI cards + overdue highlights |
| GET/POST | /employees | directory list / admin create |
| PUT/DELETE | /employees/{id} | admin update (role promotion happens here) / delete |
| GET/POST | /departments | list / admin create |
| GET/POST | /categories | list / admin create |
| GET/POST | /assets | search+filter / register (auto asset tag AF-000N) |
| PUT/DELETE | /assets/{id} | update (incl. lifecycle status) / delete |
| POST | /allocation | blocked 409 if already allocated |
| POST | /transfer | raise a transfer request |
| POST | /booking | blocked 409 on overlap |
| POST | /maintenance | raise a request (starts Pending) |
| GET | /notifications | current user's feed |
| GET | /reports | utilization, maintenance freq, dept summary, booking heatmap |

### Additive endpoints (needed by required features, don't touch the contract above)
- `GET /assets/{id}/history` — per-asset allocation + maintenance history
- `PUT /allocation/return`, `GET /allocation/overdue`
- `PUT /transfer/decision` — approve/reject a transfer
- `PUT /booking/{id}`, `GET /booking?asset_id=` — reschedule/cancel, calendar view
- `PUT /maintenance/{id}` — drives Pending → Approved/Rejected → Technician Assigned → In Progress → Resolved

## Business rules enforced in `services/`

- **No double allocation**: `allocation_service.allocate_asset` blocks with 409 if the
  asset already has an ACTIVE allocation, naming the current holder — frontend should
  show the "Transfer Request" CTA on that response.
- **Booking overlap**: `booking_service._has_overlap` — half-open interval check, so a
  slot starting exactly when another ends is allowed.
- **Asset lifecycle**: `asset_service.ALLOWED_TRANSITIONS` is a whitelist graph
  (Available/Allocated/Reserved/Maintenance/Lost/Disposed); illegal transitions 409.
- **Maintenance workflow**: `maintenance_service.NEXT_ALLOWED` enforces
  Pending → Approved/Rejected → Technician Assigned → In Progress → Resolved,
  auto-flips the asset to Maintenance on approval and back to Available on resolution.
- Every mutation writes an `AuditLog` row and, where relevant, a `Notification`.

## Folder structure

```
app/
  routers/     # thin — request/response only, no business logic
  services/    # all business rules live here
  models/      # SQLAlchemy ORM models + enums.py
  schemas/     # Pydantic request/response models
  auth/        # JWT + password hashing + role dependencies
  database/    # engine/session/Base
  utils/       # response envelope, custom exceptions, asset tag generator
  main.py      # app wiring, CORS, centralized exception handlers
seed_admin.py  # bootstrap first Admin
```

## Known gaps (flagged, not hidden)

- Full **Audit Cycle** module (Screen 8: create cycle, assign auditors, verify assets,
  auto-generate discrepancy report, close cycle) was **not** in the frontend's endpoint
  list, so it's out of this build to respect "don't change endpoint names." The
  `AuditLog` model here is the generic action trail, not that feature. Happy to add
  `/audits` endpoints if you want it in scope before the demo.
- `DELETE /employees/{id}` is a hard delete; if that user has allocations/bookings/
  maintenance history tied to them, consider switching to a soft-delete
  (status=inactive) for demo safety — hard delete can hit FK constraints.
- Email/reminder delivery is not implemented — notifications are in-app/DB only
  (matches the "Activity Logs & Notifications Screen" spec, which is a feed, not email).
