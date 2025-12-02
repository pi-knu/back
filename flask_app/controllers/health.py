from flask import Blueprint, jsonify
from sqlalchemy import text
from database import get_session

bp = Blueprint("health", __name__)


@bp.route("/flask/health", methods=["GET"])
def aggregate_health():
    """Check health of all modules + DB"""
    results = {
        "status": "ok",
        "modules": {}
    }
    overall_healthy = True
    
    # Check database
    try:
        with get_session() as s:
            s.execute(text("SELECT 1"))
        results["modules"]["database"] = "ok"
    except Exception as e:
        results["modules"]["database"] = f"error: {str(e)}"
        overall_healthy = False
    
    # Check users module
    try:
        from controllers.users import bp as users_bp
        results["modules"]["users"] = "ok"
    except Exception as e:
        results["modules"]["users"] = f"error: {str(e)}"
        overall_healthy = False
    
    # Check lots module
    try:
        from controllers.lots import bp as lots_bp
        results["modules"]["lots"] = "ok"
    except Exception as e:
        results["modules"]["lots"] = f"error: {str(e)}"
        overall_healthy = False
    
    if not overall_healthy:
        results["status"] = "degraded"
        return jsonify(results), 503
    
    return jsonify(results), 200