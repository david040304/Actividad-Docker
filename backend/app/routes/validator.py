import re

from flask import Blueprint, request, jsonify

validator_bp = Blueprint("validator", __name__, url_prefix="/api")


@validator_bp.route("/validar", methods=["POST"])
def validate_password():
    """Valida la fortaleza de una contraseña."""
    data = request.get_json()
    password = data.get("password", "")

    errors = []

    if len(password) < 8:
        errors.append("Mínimo 8 caracteres")
    if not re.search(r"[A-Z]", password):
        errors.append("Debe tener al menos una mayúscula")
    if not re.search(r"[0-9]", password):
        errors.append("Debe tener al menos un número")
    if not re.search(r"[!@#$%^&*]", password):
        errors.append("Debe tener al menos un símbolo (!@#$%^&*)")

    if len(errors) == 0:
        level = "Fuerte"
    elif len(errors) <= 2:
        level = "Media"
    else:
        level = "Débil"

    return jsonify({"nivel": level, "errores": errors})
