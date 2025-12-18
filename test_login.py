import requests
import json

BASE_URL = "http://localhost:5000"

# Test health endpoint
print("Testing health endpoint...")
response = requests.get(f"{BASE_URL}/api/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test signup endpoint
print("Testing signup endpoint...")
signup_data = {
    "name": "Test User",
    "email": "testapi@example.com",
    "password": "test123"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/auth/signup",
        headers={"Content-Type": "application/json"},
        json=signup_data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
except Exception as e:
    print(f"Error: {e}\n")

# Test login endpoint
print("Testing login endpoint...")
login_data = {
    "email": "testapi@example.com",
    "password": "test123"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        headers={"Content-Type": "application/json"},
        json=login_data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
