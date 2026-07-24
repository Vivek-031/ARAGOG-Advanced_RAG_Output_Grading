"""
MediRAG Backend - Flask API with Optimized Medical RAG Pipeline
Uses multi-domains-medical-final-rag-model.py as the core engine
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import sqlite3
from datetime import datetime
import os
import sys
import time

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Import the optimized Medical RAG pipeline
from typing import Optional
pipeline_instance: Optional[object] = None
pipeline_initialized = False

def initialize_rag_pipeline():
    """Initialize the memory-efficient RAG pipeline once"""
    global pipeline_instance, pipeline_initialized
    
    if pipeline_initialized:
        print("[OK] Medical RAG Pipeline already initialized")
        return True
    
    try:
        print("\n" + "="*80)
        print("*** INITIALIZING OPTIMIZED MEDICAL RAG PIPELINE ***")
        print("="*80)
        
        # Import pipeline components
        from multi_domains_medical_final_rag_model import (
            MemoryEfficientRAGPipeline, 
            config, 
            DOMAINS
        )
        
        # Initialize pipeline
        pipeline_instance = MemoryEfficientRAGPipeline(config, DOMAINS)
        pipeline_initialized = True
        
        print("\n" + "="*80)
        print("[OK] MEDICAL RAG PIPELINE READY!")
        print(f"Available Domains: {len(DOMAINS)}")
        print("Memory-optimized mode active")
        print("="*80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] ERROR INITIALIZING RAG PIPELINE:")
        print(f"   {str(e)}")
        print("   Backend will start but RAG queries will fail")
        print("="*80 + "\n")
        return False


app = Flask(__name__)
CORS(app)

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

def get_db_connection():
    """Get a fresh MySQL database connection for authentication"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="nikhil26@",
        database="user_auth",
        connection_timeout=30,
        autocommit=True
    )

def get_chat_db_connection():
    """Get SQLite database connection for chat history"""
    db_path = os.path.join(os.path.dirname(__file__), 'chat_history.db')
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize MySQL database connection for users
db = get_db_connection()
cursor = db.cursor(dictionary=True)

# Create users table if it doesn't exist
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

# Initialize SQLite database for chat history
chat_db = get_chat_db_connection()
chat_cursor = chat_db.cursor()

# Create chat_history table in SQLite
chat_cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_id TEXT,
    role TEXT,
    message TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
chat_db.commit()


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.route("/api/auth/signup", methods=["POST"])
def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not all([name, email, password]):
            return jsonify({"message": "All fields are required"}), 400

        # Get fresh database connection for this request
        req_db = get_db_connection()
        req_cursor = req_db.cursor(dictionary=True)
        
        # Check if user already exists
        req_cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = req_cursor.fetchone()
        
        if existing_user:
            req_cursor.close()
            req_db.close()
            return jsonify({"message": "Email already registered"}), 400

        # Hash password (simple implementation - use bcrypt in production)
        import hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert new user
        req_cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        req_db.commit()

        # Get the newly created user
        req_cursor.execute("SELECT id, name, email, avatar FROM users WHERE email = %s", (email,))
        user = req_cursor.fetchone()
        req_cursor.close()
        req_db.close()

        # Generate a simple token (use JWT in production)
        import secrets
        token = secrets.token_urlsafe(32)

        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "avatar": user["avatar"]
            },
            "token": token
        }), 201

    except Exception as e:
        print(f"❌ Signup error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"message": "Registration failed. Please try again."}), 500


@app.route("/api/auth/login", methods=["POST"])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not all([email, password]):
            return jsonify({"message": "Email and password are required"}), 400

        # Hash the provided password
        import hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Get fresh database connection for this request
        req_db = get_db_connection()
        req_cursor = req_db.cursor(dictionary=True)
        
        # Find user
        req_cursor.execute(
            "SELECT id, name, email, avatar, password FROM users WHERE email = %s",
            (email,)
        )
        user = req_cursor.fetchone()
        req_cursor.close()
        req_db.close()

        if not user or user["password"] != hashed_password:
            return jsonify({"message": "Invalid email or password"}), 401

        # Generate a simple token (use JWT in production)
        import secrets
        token = secrets.token_urlsafe(32)

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "avatar": user["avatar"]
            },
            "token": token
        }), 200

    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"message": "Login failed. Please try again."}), 500


# ============================================================================
# CHAT SESSION MANAGEMENT ENDPOINTS
# ============================================================================

@app.route("/api/chat/sessions/<int:user_id>", methods=["GET"])
def get_sessions(user_id):
    """Fetch all chat sessions for a user"""
    try:
        conn = get_chat_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                session_id,
                MIN(created_at) as created_at,
                COUNT(*) as message_count,
                (SELECT message FROM chat_history 
                 WHERE user_id = ? AND session_id = ch.session_id 
                 AND role = 'user' 
                 ORDER BY created_at ASC LIMIT 1) as title
            FROM chat_history ch
            WHERE user_id = ?
            GROUP BY session_id
            ORDER BY created_at DESC
        """, (user_id, user_id))
        sessions = cur.fetchall()
        
        formatted_sessions = []
        for session in sessions:
            formatted_sessions.append({
                "session_id": session["session_id"],
                "created_at": session["created_at"],
                "message_count": session["message_count"],
                "title": session["title"] if session["title"] else "New Chat"
            })
        
        conn.close()
        return jsonify(formatted_sessions)
    except Exception as e:
        print(f"❌ Error fetching sessions: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat/sessions/<session_id>/messages", methods=["GET"])
def get_session_messages(session_id):
    """Fetch messages for a specific session"""
    try:
        conn = get_chat_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT * FROM chat_history WHERE session_id = ? ORDER BY created_at ASC",
            (session_id,)
        )
        messages = cur.fetchall()
        
        # Convert Row objects to dictionaries
        result = [dict(row) for row in messages]
        conn.close()
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error fetching session messages: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat/new", methods=["POST"])
def create_new_session():
    """Create a new chat session"""
    data = request.get_json()
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    
    import random
    session_id = f"session_{int(time.time())}_{random.randint(1000, 9999)}"
    
    return jsonify({
        "status": "success",
        "session_id": session_id
    }), 200


@app.route("/api/chat/sessions/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    """Delete a chat session"""
    try:
        conn = get_chat_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "DELETE FROM chat_history WHERE session_id = ?",
            (session_id,)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Session deleted"}), 200
    except Exception as e:
        print(f"❌ Error deleting session: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat/<int:user_id>", methods=["GET"])
def get_chat(user_id):
    """Fetch chat history (legacy endpoint)"""
    try:
        conn = get_chat_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT * FROM chat_history WHERE user_id = ? ORDER BY created_at ASC",
            (user_id,)
        )
        chats = cur.fetchall()
        
        # Convert Row objects to dictionaries
        result = [dict(row) for row in chats]
        conn.close()
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error fetching chat history: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat/save", methods=["POST"])
def save_chat():
    """Save a chat message"""
    data = request.get_json()
    
    user_id = data.get("user_id")
    session_id = data.get("session_id")
    role = data.get("role")
    message = data.get("message", "")
    image_url = data.get("image_url")

    if not all([user_id, session_id, role]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_chat_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO chat_history (user_id, session_id, role, message, image_url)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, session_id, role, message, image_url))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"❌ Database error: {e}")
        return jsonify({"error": str(e)}), 500


# ============================================================================
# NEW OPTIMIZED RAG ENDPOINTS
# ============================================================================

def generate_general_response(query: str) -> str:
    """
    Generate a general-purpose response for non-medical queries using the generator model
    """
    try:
        from multi_domains_medical_final_rag_model import AutoTokenizer, AutoModelForSeq2SeqLM
        import torch
        
        # Use the same generator model that's already loaded in pipeline
        if pipeline_instance and hasattr(pipeline_instance, 'generator_model'):
            tokenizer = pipeline_instance.generator_tokenizer
            model = pipeline_instance.generator_model
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            # Fallback: load a small model
            tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
            model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model = model.to(device)
        
        # Create a clear, general prompt
        prompt = f"Answer the following question clearly and accurately:\n\nQuestion: {query}\n\nAnswer:"
        
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.7,
                top_p=0.9,
                num_beams=4,
                do_sample=False,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        
        # If answer is too short or empty, provide a helpful fallback
        if len(answer.split()) < 5:
            return "I can help with that. Could you provide more context or rephrase your question?"
        
        return answer
        
    except Exception as e:
        print(f"❌ Error generating general response: {e}")
        return "I can help you with that. Could you please provide more details or rephrase your question?"


@app.route("/api/ask", methods=["POST"])
def ask():
    """
    Main query endpoint with dual-mode support:
    - Medical queries: Use specialized RAG pipeline
    - General queries: Use general-purpose response generation
    """
    global pipeline_instance, pipeline_initialized

    # Ensure pipeline is ready
    if not pipeline_initialized or pipeline_instance is None:
        print("⚙️ Initializing Medical RAG pipeline...")
        initialize_rag_pipeline()

    data = request.get_json()
    query = data.get("query", "").strip()
    user_id = data.get("user_id", None)
    session_id = data.get("session_id", None)

    if not query:
        return jsonify({"error": "Query is required"}), 400

    print(f"\n{'='*80}")
    print(f"📩 Query Received: {query}")
    print(f"{'='*80}")

    try:
        start = time.time()

        # ✅ Call the RAG pipeline to determine mode
        result = None
        if hasattr(pipeline_instance, "run_query"):
            result = pipeline_instance.run_query(query)
        elif hasattr(pipeline_instance, "query"):
            result = pipeline_instance.query(query)

        elapsed = round(time.time() - start, 2)

        if not result:
            print("❌ Empty result from pipeline.")
            return jsonify({
                "query": query,
                "answer": "The AI was unable to generate a response. Please retry.",
                "confidence": 0.0,
                "processing_time": elapsed
            }), 500

        # ✅ Check query type and handle accordingly
        query_type = result.get("query_type", "general")
        
        # Handle irrelevant queries
        if query_type == "irrelevant":
            return jsonify({
                "query": query,
                "answer": result.get("answer", "Please ask a question related to medicine, healthcare, biology, or medical history."),
                "domains": [],
                "confidence": 0.0,
                "processing_time": round(time.time() - start, 2),
                "sources": [],
                "is_emergency": False,
                "is_medical": False,
                "mode": "irrelevant"
            }), 200
        
        # Handle general queries
        if result.get("requires_general_response", False):
            print(f"🤖 Generating general response for: {query}")
            general_answer = generate_general_response(query)
            
            return jsonify({
                "query": query,
                "answer": general_answer,
                "domains": [],
                "confidence": 1.0,
                "processing_time": round(time.time() - start, 2),
                "sources": [],
                "is_emergency": False,
                "is_medical": False,
                "mode": "general"
            }), 200

        # ✅ Medical query - return RAG result
        if not result.get("answer", "").strip():
            print("❌ Empty medical answer from pipeline.")
            return jsonify({
                "query": query,
                "answer": "The medical AI was unable to generate a response. Please retry.",
                "confidence": 0.0,
                "processing_time": elapsed
            }), 500

        # ✅ Normalize keys for medical response
        response = {
            "query": result.get("query", query),
            "answer": result.get("answer", "No answer generated."),
            "domains": result.get("domains", []),
            "confidence": result.get("metrics", {}).get("composite", 0.0),
            "processing_time": result.get("processing_time", elapsed),
            "sources": result.get("sources", []),
            "is_emergency": result.get("is_emergency", False),
            "is_medical": True,
            "mode": "medical"
        }

        print(f"✅ Medical answer ready in {elapsed}s (confidence: {response['confidence']:.2f})")
        print(f"{'='*80}\n")

        return jsonify(response), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Error in /api/ask: {e}")

        return jsonify({
            "query": query,
            "answer": f"An internal error occurred while processing your question: {e}",
            "confidence": 0.0
        }), 500


@app.route("/api/rag/query", methods=["POST"])
def rag_query():
    """
    Legacy RAG endpoint - redirects to /api/ask for compatibility
    """
    return ask()


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Health check endpoint
    Returns system status and available domains
    """
    global pipeline_initialized
    
    try:
        from multi_domains_medical_final_rag_model import DOMAINS
        
        return jsonify({
            "status": "healthy",
            "pipeline_initialized": pipeline_initialized,
            "available_domains": len(DOMAINS) if pipeline_initialized else 0,
            "domain_names": [d.name for d in DOMAINS] if pipeline_initialized else [],
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route("/api/domains", methods=["GET"])
def get_domains():
    """
    Get all available medical domains
    
    Response:
    {
        "domains": [
            {"name": "Cancer", "dataset": "Cancer Medical QA"},
            ...
        ]
    }
    """
    try:
        from multi_domains_medical_final_rag_model import DOMAINS
        
        domains_list = [
            {
                "name": d.name,
                "dataset": d.dataset_name,
                "has_index": os.path.exists(d.index_path)
            }
            for d in DOMAINS
        ]
        
        return jsonify({
            "domains": domains_list,
            "total": len(domains_list)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("*** STARTING MEDIRAG BACKEND SERVER ***")
    print("="*80 + "\n")
    
    # Initialize Medical RAG Pipeline on startup
    initialize_rag_pipeline()
    
    print("\n" + "="*80)
    print("Server Configuration:")
    print("   Host: 0.0.0.0")
    print("   Port: 5000")
    print("   Debug: True")
    print("="*80 + "\n")
    
    print("Available Endpoints:")
    print("   POST /api/auth/login       - User login")
    print("   POST /api/auth/signup      - User registration")
    print("   POST /api/ask              - Main RAG query endpoint")
    print("   POST /api/rag/query        - Legacy RAG endpoint")
    print("   GET  /api/health           - Health check")
    print("   GET  /api/domains          - Get available domains")
    print("   GET  /api/chat/sessions/<user_id>")
    print("   POST /api/chat/save")
    print("="*80 + "\n")
    
    # ✅ Disable debug mode to avoid reloader issues
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
