from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# ===== PAGINA PRINCIPAL =====
@app.route('/')
def home():
    return render_template("index.html")

# ===== PAGINA VALIDADOR =====
@app.route('/validador')
def validador():
    return render_template("validador.html")

# ===== ENDPOINT VALIDAR PASSWORD =====
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
    app.run(host="0.0.0.0", port=5000, debug=True)