import requests
import random

BASE_URL = "http://localhost:5000"

# Generate unique email
random_num = random.randint(1000, 9999)
email = f"user{random_num}@example.com"

print(f"Testing fresh signup with: {email}\n")

# Test signup
signup_data = {
    "name": "Fresh User",
    "email": email,
    "password": "test123"
}

print("1. Testing SIGNUP...")
response = requests.post(
    f"{BASE_URL}/api/auth/signup",
    headers={"Content-Type": "application/json"},
    json=signup_data
)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}\n")

if response.status_code == 201:
    print("✅ Signup successful!\n")
    
    # Test login with same credentials
    print("2. Testing LOGIN with same credentials...")
    login_data = {
        "email": email,
        "password": "test123"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        headers={"Content-Type": "application/json"},
        json=login_data
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✅ Login successful!")
        print("\n🎉 AUTHENTICATION WORKING PERFECTLY!")
    else:
        print("\n❌ Login failed")
else:
    print("❌ Signup failed")
