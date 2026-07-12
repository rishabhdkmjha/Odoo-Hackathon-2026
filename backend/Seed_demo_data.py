"""
Seeds realistic demo data through the live API so the dashboard, asset list,
and reports aren't all zeros on camera.

Run this AFTER seed_admin.py, AND after the backend is already running
(uvicorn app.main:app --reload --port 8000) - this script is a client of
the API, it doesn't touch the DB directly.

Usage:
    pip install requests   # if not already installed
    python seed_demo_data.py
"""
import sys
import requests

BASE = "http://localhost:8000"
ADMIN_EMAIL = "admin@assetflow.com"
ADMIN_PASSWORD = "Admin@123"


def check(resp, label):
    if resp.status_code >= 400:
        print(f"FAILED: {label} -> [{resp.status_code}] {resp.text}")
        sys.exit(1)
    body = resp.json()
    print(f"OK: {label}")
    return body["data"]


def main():
    session = requests.Session()

    # --- login as admin ---
    r = session.post(f"{BASE}/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    data = check(r, "login as admin")
    token = data["access_token"]
    session.headers.update({"Authorization": f"Bearer {token}"})

    # --- departments ---
    departments = {}
    for name in ["Engineering", "Marketing", "Finance", "Operations"]:
        r = session.post(f"{BASE}/departments", json={"name": name})
        if r.status_code == 400:
            # already exists from a previous run - fetch it instead
            existing = check(session.get(f"{BASE}/departments"), f"fetch departments (for {name})")
            departments[name] = next(d["id"] for d in existing if d["name"] == name)
        else:
            departments[name] = check(r, f"create department '{name}'")["id"]

    # --- categories ---
    categories = {}
    for name in ["Electronics", "Furniture", "Vehicles", "Meeting Rooms"]:
        r = session.post(f"{BASE}/categories", json={"name": name})
        if r.status_code == 400:
            existing = check(session.get(f"{BASE}/categories"), f"fetch categories (for {name})")
            categories[name] = next(c["id"] for c in existing if c["name"] == name)
        else:
            categories[name] = check(r, f"create category '{name}'")["id"]

    # --- employees (signup creates plain Employee accounts) ---
    employees = {}
    people = [
        ("Priya Menon", "priya@company.com"),
        ("Raj Kapoor", "raj@company.com"),
        ("Sana Sheikh", "sana@company.com"),
        ("Dev Iyer", "dev@company.com"),
    ]
    for name, email in people:
        r = session.post(f"{BASE}/auth/signup", json={"name": name, "email": email, "password": "Pass123!"})
        if r.status_code == 400:
            existing = check(session.get(f"{BASE}/employees"), f"fetch employees (for {name})")
            employees[name] = next(e["id"] for e in existing if e["email"] == email)
        else:
            employees[name] = check(r, f"signup employee '{name}'")["id"]

    # --- assets ---
    asset_specs = [
        ("Dell Latitude 5440", categories["Electronics"], departments["Engineering"], False),
        ("MacBook Pro 14\"", categories["Electronics"], departments["Marketing"], False),
        ("HP LaserJet Pro", categories["Electronics"], departments["Operations"], False),
        ("Office Chair - Herman Miller", categories["Furniture"], departments["Finance"], False),
        ("Company Vehicle - Innova KA05", categories["Vehicles"], departments["Operations"], True),
        ("Conference Room B2", categories["Meeting Rooms"], departments["Engineering"], True),
        ("Projector - Epson EB-X06", categories["Electronics"], departments["Marketing"], True),
    ]
    assets = {}
    for name, category_id, dept_id, is_bookable in asset_specs:
        r = session.post(
            f"{BASE}/assets",
            json={
                "name": name,
                "category_id": category_id,
                "department_id": dept_id,
                "is_bookable": is_bookable,
                "condition": "good",
                "location": "HQ - Bangalore",
            },
        )
        body = check(r, f"register asset '{name}'")
        assets[name] = body["id"]
        print(f"   -> tag: {body['asset_tag']}")

    # --- allocations (2 of the non-bookable assets) ---
    check(
        session.post(
            f"{BASE}/allocation",
            json={
                "asset_id": assets["Dell Latitude 5440"],
                "employee_id": employees["Priya Menon"],
                "expected_return_date": "2026-08-15",
            },
        ),
        "allocate Dell Latitude to Priya",
    )
    check(
        session.post(
            f"{BASE}/allocation",
            json={
                "asset_id": assets["MacBook Pro 14\""],
                "employee_id": employees["Sana Sheikh"],
                "expected_return_date": "2026-08-20",
            },
        ),
        "allocate MacBook Pro to Sana",
    )

    # --- a pending transfer request (Raj wants Priya's laptop) ---
    check(
        session.post(
            f"{BASE}/transfer",
            json={"asset_id": assets["Dell Latitude 5440"], "to_employee_id": employees["Raj Kapoor"]},
        ),
        "raise transfer request (Raj wants the Dell Latitude)",
    )

    # --- bookings on bookable assets ---
    check(
        session.post(
            f"{BASE}/booking",
            json={
                "asset_id": assets["Conference Room B2"],
                "start_time": "2026-08-01T09:00:00Z",
                "end_time": "2026-08-01T10:00:00Z",
                "purpose": "Sprint planning",
            },
        ),
        "book Conference Room B2 (9-10am)",
    )
    check(
        session.post(
            f"{BASE}/booking",
            json={
                "asset_id": assets["Conference Room B2"],
                "start_time": "2026-08-01T14:00:00Z",
                "end_time": "2026-08-01T15:00:00Z",
                "purpose": "Client demo",
            },
        ),
        "book Conference Room B2 (2-3pm)",
    )
    check(
        session.post(
            f"{BASE}/booking",
            json={
                "asset_id": assets["Company Vehicle - Innova KA05"],
                "start_time": "2026-08-02T08:00:00Z",
                "end_time": "2026-08-02T18:00:00Z",
                "purpose": "Client site visit",
            },
        ),
        "book Company Vehicle",
    )

    # --- a maintenance request, approved (so an asset shows 'Under Maintenance') ---
    mr = check(
        session.post(
            f"{BASE}/maintenance",
            json={
                "asset_id": assets["HP LaserJet Pro"],
                "issue_description": "Paper jam, toner leaking",
                "priority": "high",
            },
        ),
        "raise maintenance request for HP LaserJet",
    )
    check(
        session.put(f"{BASE}/maintenance/{mr['id']}", json={"status": "approved"}),
        "approve maintenance request (asset -> Under Maintenance)",
    )

    # --- one more maintenance request left pending, for variety ---
    check(
        session.post(
            f"{BASE}/maintenance",
            json={
                "asset_id": assets["Office Chair - Herman Miller"],
                "issue_description": "Armrest is loose",
                "priority": "low",
            },
        ),
        "raise second maintenance request (left pending)",
    )

    print("\nDone. Refresh the dashboard - KPIs, assets, bookings, and")
    print("maintenance should now show real, non-zero data.")


if __name__ == "__main__":
    main()