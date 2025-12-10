import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from api.routes import create_blueprints
from db.mongo import MongoDB
from dev import print_routes

def create_app():
    # Tenta conexão com banco de dados
    try:
        db = MongoDB.connect()
        MongoDB.test()
        print("✅ Banco de Dados conectado!")
    except Exception as e:
        print(f"⚠️ Aviso: Conexão com banco falhou ({e})")
        db = None

    app = Flask(__name__)

    # Configuração de CORS (Permite acesso da Vercel)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route("/")
    def home():
        return jsonify({
            "status": "online",
            "service": "api-backend",
            "database": "connected" if db is not None else "disconnected"
        })

    # --- ROTA DE AUTENTICAÇÃO (BOOTSTRAP ADMIN) ---
    # Valida credenciais baseadas em variáveis de ambiente seguras.
    @app.route("/auth/login", methods=["POST"])
    def login():
        data = request.get_json()

        # Pega credenciais seguras do ambiente (ou usa padrão para teste local)
        env_email = os.getenv("ADMIN_EMAIL", "admin@teste.com")
        env_pass = os.getenv("ADMIN_PASS", "123456")

        req_email = data.get("email")
        req_password = data.get("password")

        if req_email == env_email and req_password == env_pass:
            return jsonify({
                "token": "session-valid-admin-token",
                "user": {
                    "id": "admin-01",
                    "name": "Administrator",
                    "email": env_email,
                    "role": "admin"
                }
            }), 200

        return jsonify({"error": "Credenciais inválidas"}), 401
    # --------------------------------------------------

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
