# # tests/test_users.py
# import pytest
# def user_payload(uid=1, name="Johannan", email="js@atu.ie", age=25, sid="S1234567"):
#  return {"user_id": uid, "name": name, "email": email, "age": age, "student_id": sid}

# #testing to see if user is created properly
# def test_create_user_ok(client):
#  r = client.post("/api/users", json=user_payload())
#  assert r.status_code == 201
#  data = r.json()
#  assert data["user_id"] == 1
#  assert data["name"] == "Johannan"

# #Tests to see if there is duplicate user ids
# def test_duplicate_user_id_conflict(client):
#  client.post("/api/users", json=user_payload(uid=2))
#  r = client.post("/api/users", json=user_payload(uid=2))
#  assert r.status_code == 409 # duplicate id -> conflict
#  assert "exists" in r.json()["detail"].lower()

# #testing for bad student ids using parameterized test
# @pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
# def test_bad_student_id_422(client, bad_sid):
#  r = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
#  assert r.status_code == 422 # pydantic validation error

# #testing to see if users can be got
# def test_get_user_404(client):
#  r = client.get("/api/users/999")
#  # pydantic validation error
#  assert r.status_code == 404 

# #testing to see if user can be deleted
# def test_delete_then_404(client):
#  client.post("/api/users", json=user_payload(uid=10))
#  r1 = client.delete("/api/users/10")
#  assert r1.status_code == 204
#  r2 = client.delete("/api/users/10")
#  # pydantic validation error
#  assert r2.status_code == 404 
 
#  #Testing Put(Update), creates a users and 
# def test_update_then_404(client):
#  client.post("/api/users", json=user_payload(uid=1, name="Sean", email="sm@atu.ie", age=22, sid="S1234567"))
#  r1 = client.put("/api/users/1", json=user_payload())
#  assert r1.status_code == 200
#  r2 = client.put("/api/users/2", json=user_payload())
#   # pydantic validation error
#  assert r2.status_code == 404

#  #testing for bad student names using parameterized test
#  @pytest.mark.parametrize("bad_name",["ab","Johan","A" * 51]) #Multiplys by 51 to make it too long
#  def test_bad_student_id_422(client,bad_name):
#   r = client.post("/api/user",json=user_payload(uid=3,sid=bad_name))
#   #pydantic validation
#   assert r.status_code == 422 