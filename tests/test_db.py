# tests/test_db.py
import pytest

def user_payload(name="User", email="user@atu.ie", age=20, sid="S9990001"):
 return {"name": name, "email": email, "age": age, "student_id": sid}

# robust: create user or find existing by student_id OR email
def ensure_user(client, name, sid, age=20):
 email = f"{name.lower()}_{sid.lower()}@atu.ie"  # unique per SID
 r = client.post("/api/users", json={"name": name, "email": email, "age": age, "student_id": sid})
 if r.status_code == 201:
  return r.json()["id"]
 # conflict or other -> list and find by sid or email
 r2 = client.get("/api/users")
 assert r2.status_code == 200
 for u in r2.json():
  if u.get("student_id") == sid or u.get("email") == email:
   return u["id"]
 assert False, "user not created and not found"


# ---------- USER PUT (do not change unique fields) ----------
def test_update_user_ok(client):
 # unique sid/email for this test
 sid = "S9991001"
 email = f"put_{sid.lower()}@atu.ie"

 # create
 client.post("/api/users", json=user_payload(name="OldUser", email=email, sid=sid))

 # PUT: keep same unique fields (email, student_id) -> no 409 even if DB is dirty
 r = client.put(f"/api/users/{sid}", json={
  "name": "NewUser",
  "email": email,
  "age": 21,
  "student_id": sid
 })
 assert r.status_code == 200
 data = r.json()
 assert data["name"] == "NewUser"
 assert data["email"] == email
 assert data["age"] == 21
 assert data["student_id"] == sid


# ---------- USER PATCH (change one non-unique field) ----------
def test_patch_user_ok(client):
 sid = "S9991002"
 email = f"patch_{sid.lower()}@atu.ie"

 client.post("/api/users", json=user_payload(name="OldUser", email=email, sid=sid))

 r = client.patch(f"/api/users/{sid}", json={"name": "PatchedUser"})
 assert r.status_code == 200
 data = r.json()
 assert data["name"] == "PatchedUser"
 assert data["email"] == email  # unchanged


# ---------- PROJECT PUT (owner ensured even if exists) ----------
def test_update_project_ok(client):
 sid = "S9992001"
 owner_id = ensure_user(client, name="Owner", sid=sid, age=22)

 # create project
 p = client.post("/api/projects", json={"name": "OldProj", "description": "old", "owner_id": owner_id})
 assert p.status_code == 201
 pid = p.json()["project_id"]

 # update project fully
 r = client.put(f"/api/projects/{pid}", json={"name": "NewProj", "description": "new", "owner_id": owner_id})
 assert r.status_code == 200
 data = r.json()
 assert data["name"] == "NewProj"
 assert data["description"] == "new"


# ---------- PROJECT PATCH (owner ensured even if exists) ----------
def test_patch_project_ok(client):
 sid = "S9992002"
 owner_id = ensure_user(client, name="Owner2", sid=sid, age=23)

 p = client.post("/api/projects", json={"name": "PatchProj", "description": "desc", "owner_id": owner_id})
 assert p.status_code == 201
 pid = p.json()["project_id"]

 r = client.patch(f"/api/projects/{pid}", json={"description": "updated desc"})
 assert r.status_code == 200
 data = r.json()
 assert data["description"] == "updated desc"
 assert data["name"] == "PatchProj"  # unchanged
