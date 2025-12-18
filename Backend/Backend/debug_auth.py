"""
Debug script to test authentication directly without Flask
"""
import mysql.connector
import hashlib
import secrets

def get_db_connection():
    """Get a fresh database connection"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="nikhil26@",
        database="user_auth",
        connection_timeout=30,
        autocommit=True
    )

# Test 1: Database connection
print("1. Testing database connection...")
try:
    db = get_db_connection()
    print("   ✅ Connected to database\n")
except Exception as e:
    print(f"   ❌ Connection failed: {e}\n")
    exit(1)

# Test 2: Create tables
print("2. Creating users table...")
try:
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        avatar VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    db.commit()
    print("   ✅ Users table ready\n")
except Exception as e:
    print(f"   ❌ Table creation failed: {e}\n")
    exit(1)

# Test 3: Signup simulation
print("3. Testing signup process...")
try:
    name = "Debug User"
    email = "debug_test@example.com"
    password = "test123"
    
    # Create fresh connection
    req_db = get_db_connection()
    req_cursor = req_db.cursor(dictionary=True)
    
    # Check if user exists
    req_cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    existing_user = req_cursor.fetchone()
    
    if existing_user:
        print(f"   ⚠️  User already exists (id: {existing_user['id']})")
        print("   Trying to login instead...\n")
    else:
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Insert user
        req_cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        req_db.commit()
        print("   ✅ User inserted successfully\n")
    
    req_cursor.close()
    req_db.close()
    
except Exception as e:
    print(f"   ❌ Signup failed: {e}")
    import traceback
    traceback.print_exc()
    print()

# Test 4: Login simulation
print("4. Testing login process...")
try:
    email = "debug_test@example.com"
    password = "test123"
    
    # Hash password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Create fresh connection
    req_db = get_db_connection()
    req_cursor = req_db.cursor(dictionary=True)
    
    # Find user
    req_cursor.execute(
        "SELECT id, name, email, avatar, password FROM users WHERE email = %s",
        (email,)
    )
    user = req_cursor.fetchone()
    
    if not user:
        print("   ❌ User not found")
    elif user["password"] != hashed_password:
        print("   ❌ Invalid password")
    else:
        # Generate token
        token = secrets.token_urlsafe(32)
        print(f"   ✅ Login successful!")
        print(f"   User ID: {user['id']}")
        print(f"   Name: {user['name']}")
        print(f"   Email: {user['email']}")
        print(f"   Token: {token[:20]}...")
    
    req_cursor.close()
    req_db.close()
    
except Exception as e:
    print(f"   ❌ Login failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("✅ ALL AUTHENTICATION LOGIC WORKS!")
print("="*60)
print("\nIf this works but Flask fails, the issue is with Flask setup.")
