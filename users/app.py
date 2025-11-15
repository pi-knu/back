import os
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from flask import Flask, jsonify, request
from flask_cors import CORS

# Import database configuration and models
from database import get_session
from models import User, UserData

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/users/health", methods=["GET"])
def health():
    """Health check endpoint with database connectivity test."""
    try:
        with get_session() as s:
            s.execute(text("SELECT 1"))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500

# Get user endpoint
@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get user by ID with profile data."""
    try:
        uid = uuid.UUID(user_id)
    except Exception:
        return jsonify({"error": "invalid uuid"}), 400

    with get_session() as s:
        u = s.query(User).filter(User.id == uid).first()
        if not u:
            return jsonify({"error": "not found"}), 404

        data = None
        if u.data:
            data = {
                "name": u.data.name,
                "birth_date": u.data.birth_date.isoformat() if u.data.birth_date else None,
                "phone": u.data.phone
            }
        
        return jsonify({
            "id": str(u.id),
            "email": u.email,
            "data": data
        }), 200

# Update user info endpoint
@app.route("/users/<user_id>", methods=["PUT", "PATCH"])
def update_user(user_id):
    """Update user account and/or profile data."""
    try:
        uid = uuid.UUID(user_id)
    except Exception:
        return jsonify({"error": "invalid uuid"}), 400

    payload = request.get_json() or {}
    
    with get_session() as s:
        u = s.query(User).filter(User.id == uid).first()
        if not u:
            return jsonify({"error": "not found"}), 404

        # Update user fields
        if "email" in payload:
            u.email = payload["email"]
        if "password" in payload:
            u.password = payload["password"]

        # Update user data
        data = payload.get("data")
        if data is not None:
            if not u.data:
                u.data = UserData(user_id=u.id)
            
            if "name" in data:
                u.data.name = data["name"]
            if "phone" in data:
                u.data.phone = data["phone"]
            if "birth_date" in data:
                bd = data["birth_date"]
                if bd:
                    try:
                        u.data.birth_date = datetime.strptime(bd, "%Y-%m-%d").date()
                    except ValueError:
                        return jsonify({"error": "birth_date must be YYYY-MM-DD"}), 400
                else:
                    u.data.birth_date = None

        return jsonify({"id": str(u.id), "email": u.email}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT")))