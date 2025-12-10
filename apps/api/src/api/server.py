from flask import Flask, jsonify, request
from flask_cors import CORS
from api.routes import create_blueprints
from db.mongo import MongoDB
from dev import print_routes

def create_app():
    try:
        db = MongoDB.connect()
        MongoDB.test()
        print("✅ Banco de Dados conectado!")
    except Exception as e:
        print(f"⚠️ Aviso: Banco não conectado ({e}). Rodando em modo limitado.")
        db = None

    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route("/")
    def home():
        status_banco = "Online" if db is not None else "Offline (Modo Mock)"
        return jsonify({
            "message": "API Online! 🚀",
            "database_status": status_banco
        })

    @app.route("/auth/login", methods=["POST", "OPTIONS"])
    def fake_login():
        return jsonify({
            "token": "token-login",
            "user": {
                "id": "1",
                "name": "Admin DevOps",
                "email": "admin@teste.com"
            }
        }), 200

    if db is not None:
        try:
            for blueprint in create_blueprints(db):
                app.register_blueprint(blueprint)
        except Exception as e:
            print(f"Erro ao registrar rotas: {e}")

    return app

def run():
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
