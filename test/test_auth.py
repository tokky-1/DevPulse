def test_register_check(client):
    response = client.post("/User/register",json={"email": "string@gmail.com","username": "value","github_username": "value_git","password": "pass"})       
    assert response.status_code == 201       
   

def test_login_check(client):
    # First register the user so login has someone to authenticate
    client.post("/User/register", json={
        "email": "string@gmail.com",
        "username": "value",
        "github_username": "value_git",
        "password": "pass"
    })
    response = client.post("/User/login", data={
        "username": "value",
        "password": "pass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()