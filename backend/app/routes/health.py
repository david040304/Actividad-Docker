from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Endpoint de salud para Docker / orquestadores."""
    return jsonify({"status": "ok"})
