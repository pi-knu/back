import uuid
from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy import text

from models import User, UserData
from database import get_session

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get("/health")
def health():
    try:
        with get_session() as s:
            s.execute(text("SELECT 1"))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500

@bp.get("/<user_id>")
def get_user(user_id):
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
                "phone": u.data.phone,
            }

        return jsonify({"id": str(u.id), "email": u.email, "data": data}), 200


@bp.route("/<user_id>", methods=["PATCH"])
def update_user(user_id):
    try:
        uid = uuid.UUID(user_id)
    except Exception:
        return jsonify({"error": "invalid uuid"}), 400

    payload = request.get_json() or {}

    with get_session() as s:
        u = s.query(User).filter(User.id == uid).first()
        if not u:
            return jsonify({"error": "not found"}), 404

        if "email" in payload:
            u.email = payload["email"]
        if "password" in payload:
            u.password = payload["password"]

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
