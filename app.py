from flask import Flask, render_template, request, jsonify
import sqlite3
import re

app = Flask(__name__)

# Configuración de la base de datos para la agenda
DB_NAME = "contacts.db"

def init_db():
    """Crea la tabla de contactos si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()
def get_db_connection():
   
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

#===== PAGINA PRINCIPAL =====
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/agenda')
def agenda():
    return render_template("agenda.html")
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    search = request.args.get('q', '')
    conn = get_db_connection()
    if search:
        query = "SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?"
        contacts = conn.execute(query, (f'%{search}%', f'%{search}%')).fetchall()
    else:
        contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in contacts])

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    new_data = request.json
    name = new_data.get('name')
    phone = new_data.get('phone')
    email = new_data.get('email')
    if not name or not phone:
        return jsonify({"error": "Faltan datos"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", 
                   (name, phone, email))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": new_id, "message": "Creado"}), 201

@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.json
    conn = get_db_connection()
    conn.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",
                 (data.get('name'), data.get('phone'), data.get('email'), id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Actualizado"})

@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Eliminado"})


#===== PAGINA VALIDADOR =====
@app.route('/validador')
def validador():
    return render_template("validador.html")

#==== ENDPOINT VALIDAR PASSWORD =====
@app.route('/validar', methods=['POST'])
def validar_password():
    data = request.get_json()
    password = data.get("password", "")

    errores = []

    if len(password) < 8:
        errores.append("Mínimo 8 caracteres")

    if not re.search(r"[A-Z]", password):
        errores.append("Debe tener mayúscula")

    if not re.search(r"[0-9]", password):
        errores.append("Debe tener número")

    if not re.search(r"[!@#$%^&*]", password):
        errores.append("Debe tener símbolo")

    nivel = "Débil"

    if len(errores) == 0:
        nivel = "Fuerte"
    elif len(errores) <= 2:
        nivel = "Media"

    return jsonify({
        "nivel": nivel,
        "errores": errores
    })

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)