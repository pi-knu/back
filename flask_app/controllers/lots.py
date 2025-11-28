import uuid
from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from database import get_session
from models import Lot
from models import LotPhoto

bp = Blueprint("lots", __name__, url_prefix="/lots")


@bp.route("/health", methods=["GET"])
def health():
    """
    Simple health check for the lots module.
    Also tests DB connectivity.
    """
    try:
        with get_session() as s:
            s.execute(text("SELECT 1"))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500


@bp.route("", methods=["POST"])
def create_lot():
    """
    Create a new lot with optional photos.

    Expected JSON body:
    {
        "user_id": "<uuid>",
        "name": "string",
        "description": "string or null",
        "min_price": 100.0,
        "min_step": 5.0,
        "current_price": 100.0,       # optional
        "photos": ["url1", "url2"]    # optional array of photo URLs
    }
    """
    payload = request.get_json() or {}

    user_id_raw = payload.get("user_id")
    name = payload.get("name")
    description = payload.get("description")
    min_price_raw = payload.get("min_price")
    min_step_raw = payload.get("min_step")
    current_price_raw = payload.get("current_price")
    photos_payload = payload.get("photos") or []

    # Basic required fields validation
    if not user_id_raw or not name or min_price_raw is None or min_step_raw is None:
        return jsonify({"error": "user_id, name, min_price and min_step are required"}), 400

    # Parse UUID
    try:
        user_id = uuid.UUID(user_id_raw)
    except Exception:
        return jsonify({"error": "user_id must be a valid UUID"}), 400

    # Parse numeric values using Decimal for precision
    try:
        min_price = Decimal(str(min_price_raw))
        min_step = Decimal(str(min_step_raw))
        current_price = (
            Decimal(str(current_price_raw)) if current_price_raw is not None else None
        )
    except (InvalidOperation, TypeError):
        return jsonify({"error": "min_price, min_step and current_price must be numeric"}), 400

    # Additional business validation (duplicated DB CHECK constraints)
    if min_price < 1:
        return jsonify({"error": "min_price must be >= 1"}), 400
    if min_step <= 1:
        return jsonify({"error": "min_step must be > 1"}), 400

    # Validate photos payload
    if not isinstance(photos_payload, list):
        return jsonify({"error": "photos must be an array of URLs"}), 400

    for url in photos_payload:
        if not isinstance(url, str) or not url:
            return jsonify({"error": "each photo url must be a non-empty string"}), 400

    try:
        with get_session() as s:
            # Create lot entity
            # is_deleted та is_finished =False 
            lot = Lot(
                user_id=user_id,
                name=name,
                description=description,
                min_price=min_price,
                min_step=min_step,
                current_price=current_price,
            )
            s.add(lot)
            s.flush()  # obtain generated lot.id

            # Create photos if provided
            for url in photos_payload:
                photo = LotPhoto(lot_id=lot.id, url=url)
                s.add(photo)

            # Build response
            return jsonify(
                {
                    "id": str(lot.id),
                    "user_id": str(lot.user_id),
                    "name": lot.name,
                    "description": lot.description,
                    "min_price": float(lot.min_price),
                    "min_step": float(lot.min_step),
                    "current_price": float(lot.current_price)
                    if lot.current_price is not None
                    else None,
                    "is_deleted": lot.is_deleted,
                    "is_finished": lot.is_finished,
                    "photos": photos_payload,
                }
            ), 201

    except IntegrityError as ie:
        return jsonify({"error": "integrity error", "detail": str(ie.orig)}), 409
    except Exception as e:
        return jsonify({"error": "internal error", "detail": str(e)}), 500


@bp.route("/<lot_id>", methods=["GET"])
def get_lot(lot_id: str):
    """
    Get lot details by ID, including attached photos.
    """
    try:
        lid = uuid.UUID(lot_id)
    except Exception:
        return jsonify({"error": "invalid uuid"}), 400

    with get_session() as s:
        lot = s.query(Lot).filter(Lot.id == lid).first()
        if not lot:
            return jsonify({"error": "not found"}), 404

        # Load photos explicitly to control output format
        photos = (
            s.query(LotPhoto.url)
            .filter(LotPhoto.lot_id == lot.id)
            .all()
        )
        photo_urls = [row[0] for row in photos]

        return jsonify(
            {
                "id": str(lot.id),
                "user_id": str(lot.user_id),
                "name": lot.name,
                "description": lot.description,
                "min_price": float(lot.min_price),
                "min_step": float(lot.min_step),
                "current_price": float(lot.current_price)
                if lot.current_price is not None
                else None,
                "is_deleted": lot.is_deleted,
                "is_finished": lot.is_finished,
                "photos": photo_urls,
            }
        ), 200

@bp.route("/<lot_id>", methods=["PATCH"])
def update_lot(lot_id):
    try:
        lid = uuid.UUID(lot_id)
    except ValueError:
        return jsonify({"error": "invalid uuid"}), 400

    payload = request.get_json() or {}

    with get_session() as s:
        lot = s.query(Lot).filter(Lot.id == lid).first()
        if not lot:
            return jsonify({"error": "not found"}), 404

        # scalar fields 
        if "name" in payload:
            lot.name = payload["name"]
        if "description" in payload:
            lot.description = payload["description"]
        if "min_price" in payload:
            if payload["min_price"] is not None and payload["min_price"] < 1:
                return jsonify({"error": "min_price must be >= 1"}), 400
            lot.min_price = payload["min_price"]
        if "min_step" in payload:
            if payload["min_step"] is not None and payload["min_step"] <= 1:
                return jsonify({"error": "min_step must be > 1"}), 400
            lot.min_step = payload["min_step"]
        if "current_price" in payload:
            lot.current_price = payload["current_price"]
        
        if "is_finished" in payload:
            lot.is_finished = bool(payload["is_finished"])
        if "is_deleted" in payload:
            lot.is_deleted = bool(payload["is_deleted"])

        if "photos" in payload and payload["photos"] is not None:
            new_urls = payload["photos"]
            if not isinstance(new_urls, list):
                return jsonify({"error": "photos must be a list of URLs"}), 400

            existing_urls = {p.url for p in lot.photos}
            for url in new_urls:
                if url not in existing_urls:
                    lot.photos.append(LotPhoto(lot_id=lot.id, url=url))

        return jsonify(
            {
                "id": str(lot.id),
                "user_id": str(lot.user_id),
                "name": lot.name,
                "description": lot.description,
                "min_price": float(lot.min_price) if lot.min_price is not None else None,
                "min_step": float(lot.min_step) if lot.min_step is not None else None,
                "current_price": float(lot.current_price) if lot.current_price is not None else None,
                "is_deleted": lot.is_deleted,
                "is_finished": lot.is_finished,
                "photos": [p.url for p in lot.photos],
            }
        ), 200

@bp.route("/<lot_id>", methods=["DELETE"])
def delete_lot(lot_id: str):
    """
    Delete a lot by ID.
    Sets is_deleted = True instead of removing from DB.
    """
    try:
        lid = uuid.UUID(lot_id)
    except Exception:
        return jsonify({"error": "invalid uuid"}), 400

    with get_session() as s:
        lot = s.query(Lot).filter(Lot.id == lid).first()
        if not lot:
            return jsonify({"error": "not found"}), 404

        lot.is_deleted = True
        
        # To hard delete uncomment
        # s.delete(lot)

        return "", 204