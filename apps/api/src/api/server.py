import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from api.routes import create_blueprints
from db.mongo import MongoDB
from dev import print_routes

def create_app():
    db = None
    try:
        print("Tentando conectar ao banco...")
        db = MongoDB.connect()
        MongoDB.test()
        print("✅ Banco conectado com sucesso!")
    except Exception as e:
        print(f"⚠️ Banco OFF (Rodando em modo limitado): {e}")

    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "version": "2.1 (Login Corrigido)",
            "status": "online",
            "db_connected": db is not None
        })

    def do_login():
        data = request.get_json(silent=True) or {}

        env_email = os.getenv("ADMIN_EMAIL", "admin@teste.com")
        env_pass = os.getenv("ADMIN_PASS", "123456")

        req_email = data.get("email") or data.get("username")
        req_password = data.get("password")

        print(f"Tentativa de login recebida -> User: {req_email} | Senha: {req_password}")

        if req_email and req_email == env_email and req_password == env_pass:
            return jsonify({
                "token": "admin-token-super-seguro-123",
                "user": {
                    "id": "1",
                    "name": "Admin",
                    "email": env_email,
                    "role": "admin"
                }
            }), 200

        return jsonify({"error": "Usuário ou senha incorretos"}), 401

    app.add_url_rule('/login', view_func=do_login, methods=['POST', 'OPTIONS'])
    app.add_url_rule('/auth/login', view_func=do_login, methods=['POST', 'OPTIONS'])

    if db is not None:
        try:
            for blueprint in create_blueprints(db):
                app.register_blueprint(blueprint)
        except Exception as e:
            print(f"Erro ao registrar blueprints: {e}")

    return app

def run():
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
