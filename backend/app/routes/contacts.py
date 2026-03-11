from flask import Blueprint, request, jsonify
import psycopg2.extras

from app.database import get_db

contacts_bp = Blueprint("contacts", __name__, url_prefix="/api")


@contacts_bp.route("/contacts", methods=["GET"])
def get_contacts():
    """Lista todos los contactos o filtra por nombre/teléfono."""
    search = request.args.get("q", "")
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        if search:
            cur.execute(
                "SELECT * FROM contacts WHERE name ILIKE %s OR phone ILIKE %s",
                (f"%{search}%", f"%{search}%"),
            )
        else:
            cur.execute("SELECT * FROM contacts ORDER BY id")
        rows = cur.fetchall()
    return jsonify(rows)


@contacts_bp.route("/contacts", methods=["POST"])
def add_contact():
    """Crea un nuevo contacto."""
    data = request.get_json()
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email")

    if not name or not phone:
        return jsonify({"error": "Faltan datos obligatorios (name, phone)"}), 400

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s) RETURNING id",
            (name, phone, email),
        )
        new_id = cur.fetchone()[0]

    return jsonify({"id": new_id, "message": "Contacto creado"}), 201


@contacts_bp.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    """Actualiza un contacto existente."""
    data = request.get_json()
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "UPDATE contacts SET name = %s, phone = %s, email = %s WHERE id = %s",
            (data.get("name"), data.get("phone"), data.get("email"), contact_id),
        )
    return jsonify({"message": "Contacto actualizado"})


@contacts_bp.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    """Elimina un contacto."""
    db = get_db()
    with db.cursor() as cur:
        cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
    return jsonify({"message": "Contacto eliminado"})
