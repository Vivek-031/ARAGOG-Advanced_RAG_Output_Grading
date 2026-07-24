#!/usr/bin/env python3
"""
Test script to check SQLite database structure and content
"""

import sqlite3
import os

def test_database():
    db_path = os.path.join(os.path.dirname(__file__), 'chat_history.db')
    
    print(f"Database path: {db_path}")
    print(f"Database exists: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get schema
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\nDatabase Schema:")
        for table in tables:
            print(f"  {table[0]}")
        
        # Get sample data
        cursor.execute("SELECT COUNT(*) FROM chat_history")
        count = cursor.fetchone()[0]
        print(f"\nTotal messages: {count}")
        
        if count > 0:
            cursor.execute("SELECT DISTINCT user_id FROM chat_history")
            users = cursor.fetchall()
            print(f"Users: {[u[0] for u in users]}")
            
            cursor.execute("SELECT DISTINCT session_id FROM chat_history LIMIT 10")
            sessions = cursor.fetchall()
            print(f"Sample sessions: {[s[0] for s in sessions]}")
            
            cursor.execute("""
                SELECT user_id, session_id, COUNT(*) as msg_count 
                FROM chat_history 
                GROUP BY user_id, session_id 
                ORDER BY user_id, session_id 
                LIMIT 10
            """)
            user_sessions = cursor.fetchall()
            print(f"\nUser sessions:")
            for row in user_sessions:
                print(f"  User {row[0]} - Session {row[1]} - {row[2]} messages")
        
        conn.close()

if __name__ == "__main__":
    test_database()
