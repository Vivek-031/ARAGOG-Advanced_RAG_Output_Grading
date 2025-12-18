import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nikhil26@",
        database="user_auth",
        connection_timeout=10
    )
    
    cursor = db.cursor(dictionary=True)
    
    # Test table creation
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
    
    print("✅ Database connection successful!")
    print("✅ Users table exists/created!")
    
    # Test insert
    import hashlib
    test_password = hashlib.sha256("test123".encode()).hexdigest()
    
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            ("Test User", "testdb@example.com", test_password)
        )
        db.commit()
        print("✅ Test user inserted!")
    except mysql.connector.IntegrityError as e:
        print(f"⚠️ User already exists (this is OK): {e}")
    
    # Test select
    cursor.execute("SELECT id, name, email FROM users WHERE email = %s", ("testdb@example.com",))
    user = cursor.fetchone()
    print(f"✅ User retrieved: {user}")
    
    cursor.close()
    db.close()
    print("\n✅ All database operations successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
