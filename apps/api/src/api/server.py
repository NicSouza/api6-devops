import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from api.routes import create_blueprints
from db.mongo import MongoDB

def create_app():
    # Tenta conectar no banco
    db = None
    try:
        print("Tentando conectar ao banco...")
        db = MongoDB.connect()
        MongoDB.test()
        print("✅ Banco conectado com sucesso!")
    except Exception as e:
        print(f"⚠️ Banco OFF: {e}")

    app = Flask(__name__)

    # CORS TOTAL
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "version": "3.0 (DEBUG MODE)",
            "status": "online",
            "db_connected": db is not None
        })

    # --- LOGIN DE DEBUG ---
    def do_login():
        # 1. Responde OPTIONS na hora (Correção CORS)
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200

        data = request.get_json(silent=True) or {}

        # 2. DEFINA A SENHA AQUI (Sem variáveis de ambiente para não ter erro)
        CORRECT_EMAIL = "admin@teste.com"
        CORRECT_PASS = "123456"

        # 3. Pega o que veio do site
        req_user = data.get("email") or data.get("username")
        req_pass = data.get("password")

        # 4. IMPRIME NO LOG DO RENDER (Para a gente ver o erro)
        print(f"--- TENTATIVA DE LOGIN ---")
        print(f"Recebido User: '{req_user}'")
        print(f"Recebido Pass: '{req_pass}'")
        print(f"Esperado User: '{CORRECT_EMAIL}'")
        print(f"Esperado Pass: '{CORRECT_PASS}'")
        print(f"--------------------------")

        # 5. Comparação direta
        if req_user == CORRECT_EMAIL and req_pass == CORRECT_PASS:
            return jsonify({
                "token": "admin-token-final-presentation",
                "user": {
                    "id": "1",
                    "name": "Admin",
                    "email": CORRECT_EMAIL,
                    "role": "admin"
                }
            }), 200

        return jsonify({"error": "Credenciais invalidas"}), 401

    app.add_url_rule('/login', view_func=do_login, methods=['POST', 'OPTIONS'])
    app.add_url_rule('/auth/login', view_func=do_login, methods=['POST', 'OPTIONS'])

    if db is not None:
        try:
            for blueprint in create_blueprints(db):
                app.register_blueprint(bp)
        except:
            pass

    return app

def run():
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
