# app.py
import os
import uuid
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from sqlalchemy import create_engine, Column, String, Date, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session

# Load DB config from env (these vars come from compose env_file)
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres-dev")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "main")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()

# Models (copied/adapted from your models.py)
class User(Base):
    __tablename__ = "users"
    id = Column(PGUUID(as_uuid=True), primary_key=True,
                server_default=text("gen_random_uuid()"))
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    data = relationship("UserData", back_populates="user", uselist=False,
                        cascade="all, delete-orphan")

class UserData(Base):
    __tablename__ = "user_data"
    id = Column(PGUUID(as_uuid=True), primary_key=True,
                server_default=text("gen_random_uuid()"))
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False)
    name = Column(String(40))
    birth_date = Column(Date)
    phone = Column(String(30))

    user = relationship("User", back_populates="data")


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

app = Flask(__name__)
# open CORS for all (allows all origins, methods, headers)
CORS(app, resources={r"/*": {"origins": "*"}})

# Basic health endpoint used by docker/nginx
@app.route("/users/health", methods=["GET"])
def health():
    # Try a very cheap DB check
    try:
        with get_session() as s:
            s.execute(text("SELECT 1"))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500

# Create new user (basic)
@app.route("/users", methods=["POST"])
def create_user():
    payload = request.get_json() or {}
    email = payload.get("email")
    password = payload.get("password")
    data_payload = payload.get("data")

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    try:
        with get_session() as s:
            # Перевірка унікальності email (необов'язково, IntegrityError теж спрацює)
            existing = s.query(User).filter(User.email == email).first()
            if existing:
                return jsonify({"error": "email already exists"}), 409

            # 1) створюємо User без UserData — тригер у БД автоматично створить user_data
            user = User(email=email, password=password)
            s.add(user)

            # flush() відправляє INSERT в БД, тригер виконається вже зараз
            s.flush()

            # 2) після flush() шукаємо user_data (тригер мав створити рядок)
            ud = s.query(UserData).filter(UserData.user_id == user.id).one_or_none()

            # 3) Якщо client передав data у payload — оновлюємо (або створюємо, якщо тригер не створив)
            if data_payload:
                name = data_payload.get("name")
                phone = data_payload.get("phone")
                birth_date_raw = data_payload.get("birth_date")

                birth_date = None
                if birth_date_raw:
                    try:
                        birth_date = datetime.strptime(birth_date_raw, "%Y-%m-%d").date()
                    except ValueError:
                        return jsonify({"error": "birth_date must be YYYY-MM-DD"}), 400

                if ud:
                    # оновлюємо поля
                    if name is not None:
                        ud.name = name
                    if phone is not None:
                        ud.phone = phone
                    if birth_date_raw is not None:
                        ud.birth_date = birth_date

            # commit відбудеться у get_session context manager
            return jsonify({"id": str(user.id), "email": user.email}), 201

    except IntegrityError as ie:
        return jsonify({"error": "integrity error", "detail": str(ie.orig)}), 409
    except Exception as e:
        return jsonify({"error": "internal error", "detail": str(e)}), 500

@app.route("/users/<user_id>", methods=["GET"])
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
                "phone": u.data.phone
            }
        return jsonify({
            "id": str(u.id),
            "email": u.email,
            "data": data
        }), 200

@app.route("/users/<user_id>", methods=["PUT", "PATCH"])
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5011)))
