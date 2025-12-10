import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from api.routes import create_blueprints
from db.mongo import MongoDB

def create_app():
    db = None
    try:
        print("Tentando conectar ao banco...")
        db = MongoDB.connect()
        MongoDB.test()
        print("✅ Banco conectado com sucesso!")
    except Exception as e:
        print(f"⚠️ Banco OFF: {e}")

    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "version": "4.0 (EMERGENCY ACCESS)",
            "status": "online",
            "db_connected": db is not None
        })

    def do_login():
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200

        data = request.get_json(silent=True) or {}

        print(f"DEBUG COMPLETO DO JSON: {data}")

        req_password = data.get("password")

        CORRECT_PASS = "123456"

        if str(req_password) == CORRECT_PASS:
            print("LOGIN SUCESSO! Senha correta.")
            return jsonify({
                "token": "admin-token-emergency-access",
                "user": {
                    "id": "1",
                    "name": "Admin Apresentacao",
                    "email": "admin@teste.com",
                    "role": "admin"
                }
            }), 200

        print("LOGIN FALHA! Senha incorreta.")
        return jsonify({"error": "Senha incorreta"}), 401

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
