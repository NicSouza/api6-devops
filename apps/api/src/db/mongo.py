import os
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING

class MongoDB:
    _client = None

    @classmethod
    def connect(cls):
        """Connect to MongoDB using environment variables."""
        if cls._client is not None:
            return cls._client

        load_dotenv()

        # --- CORREÇÃO DEVOPS ---
        # 1. Tenta pegar a string de conexão completa (Produção / Atlas)
        mongo_uri = os.getenv("MONGO_URI")

        if mongo_uri:
            # Se existir a variável MONGO_URI (no Render), usa ela direto.
            # Isso suporta o protocolo 'mongodb+srv://' do Atlas.
            print(f"Tentando conectar via MONGO_URI...")
            client = MongoClient(mongo_uri)

            # Pega o nome do banco da variável ou usa o padrão
            db_name = os.getenv("DB_MONGO_NAME", "api6_mongo")
            cls._client = client[db_name]

        else:
            # 2. Se não tiver MONGO_URI, usa o método antigo (Localhost)
            print(f"Tentando conectar via variáveis locais (localhost)...")
            mongo_user = os.getenv("DB_MONGO_USER", "mongo")
            mongo_password = os.getenv("DB_MONGO_PASS", "secret")
            mongo_host = os.getenv("DB_MONGO_HOST", "localhost")
            mongo_port = os.getenv("DB_MONGO_PORT", "27017")
            mongo_db = os.getenv("DB_MONGO_NAME", "api6_mongo")

            mongo_url = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin"
            cls._client = MongoClient(mongo_url)[mongo_db]

        return cls._client

    @classmethod
    def test(cls):
        """Test the connection to MongoDB."""
        try:
            db = cls.connect()
            db.command("ping")
            print("✅ Conexão com MongoDB estabelecida com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar no MongoDB: {e}")
            raise e

# Uso:
# from db.mongo import MongoDB
# db = MongoDB.connect()


def create_species_collection(db):
    species_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "scientific_name",
                "common_name",
            ],
            "properties": {
                "scientific_name": {
                    "bsonType": "string",
                    "description": "Nome científico da espécie",
                },
                "common_name": {
                    "bsonType": "string",
                    "description": "Nome popular da espécie",
                },
            },
        }
    }
    try:
        # Verifica se a coleção existe antes de criar (evita erro em alguns drivers)
        if "species_collection" not in db.list_collection_names():
            db.create_collection("species_collection", validator=species_validator)
            print("Coleção 'species' criada com validador.")
        else:
            # Opcional: Atualizar validador se necessário
            pass
    except Exception as e:
        print(f"Aviso ao criar coleção 'species': {e}")


def create_plots_collection(db):
    plots_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["area", "state", "country"],
            "properties": {
                "area": {
                    "bsonType": "double",
                    "description": "Área da propriedade",
                },
                "state": {"bsonType": "string", "description": "Estado da área"},
                "country": {"bsonType": "string", "description": "País da área"},
            },
        }
    }
    try:
        if "plots_collection" not in db.list_collection_names():
            db.create_collection("plots_collection", validator=plots_validator)
            print("Coleção 'plots' criada com validador.")
    except Exception as e:
        print(f"Aviso ao criar coleção 'plots': {e}")


def create_yield_collection(db):
    yield_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "crop",
                "crop_year",
                "season",
                "state",
                "area",
                "production",
                "annual_rainfall",
                "fertilizer",
                "pesticide",
                "yield",
            ],
            "properties": {
                "crop": {
                    "bsonType": "string",
                    "description": "Nome da cultura cultivada",
                },
                "crop_year": {
                    "bsonType": "int",
                    "description": "Ano em que a safra foi cultivada",
                },
                "season": {
                    "bsonType": "string",
                    "enum": ["Whole Year", "Spring", "Autumn", "Summer", "Winter"],
                    "description": "Estação do ano",
                },
                "state": {"bsonType": "string", "description": "Estado"},
                "area": {
                    "bsonType": "double",
                    "description": "A área total de terra (em hectares) cultivada para a cultura específica",
                },
                "production": {
                    "bsonType": "number",
                    "description": "Quantidade de cultura produzida",
                },
                "annual_rainfall": {
                    "bsonType": "double",
                    "description": "A precipitação anual recebida na região de cultivo (em mm)",
                },
                "fertilizer": {
                    "bsonType": "double",
                    "description": "A quantidade total de fertilizante usada na cultura (em quilogramas)",
                },
                "pesticide": {
                    "bsonType": "double",
                    "description": "A quantidade total de pesticida usado na cultura (em quilogramas)",
                },
                "yield": {
                    "bsonType": "double",
                    "description": "The calculated crop yield (production per unit area)",
                },
            },
        }
    }
    try:
        if "yield_collection" not in db.list_collection_names():
            db.create_collection("yield_collection", validator=yield_validator)
            print("Coleção 'yield' criada com validador.")
    except Exception as e:
        print(f"Aviso ao criar coleção 'yield': {e}")

def create_terms_of_use_collection(db):
    terms_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["text", "status", "topics"],
            "properties": {
                "text": {
                    "bsonType": "string",
                    "description": "Texto completo dos termos de uso",
                },
                "status": {
                    "bsonType": "string",
                    "enum": ["ativo", "inativo"],
                    "description": "Status do termo de uso",
                },
                "version": {
                    "bsonType": "string",
                    "description": "Versão do termo de uso",
                },
                "topics": {
                    "bsonType": "array",
                    "description": "Lista de tópicos incluídos nos termos",
                    "items": {
                        "bsonType": "object",
                        "required": ["description", "status", "required"],
                        "properties": {
                            "description": {
                                "bsonType": "string",
                                "description": "Descrição do tópico",
                            },
                            "status": {
                                "bsonType": "string",
                                "enum": ["ativo", "inativo"],
                                "description": "Status do tópico",
                            },
                            "required": {
                                "bsonType": "bool",
                                "description": "Se o tópico é obrigatório",
                            },
                        },
                    },
                },
            },
        }
    }
    try:
        if "terms_of_use_collection" not in db.list_collection_names():
            db.create_collection("terms_of_use_collection", validator=terms_validator)
            print("Coleção 'terms_of_use_collection' criada com validador.")
    except Exception as e:
        print(f"Aviso ao criar coleção 'terms_of_use': {e}")

def create_user_acceptance_collection(db):
    acceptance_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "topics"],
            "properties": {
                "user_id": {
                    "bsonType": "string",
                    "description": "Identificador do usuário",
                },
                "topics": {
                    "bsonType": "array",
                    "description": "Lista de tópicos aceitos pelo usuário",
                    "items": {
                        "bsonType": "object",
                        "required": ["description", "status", "accepted"],
                        "properties": {
                            "description": {
                                "bsonType": "string",
                                "description": "Descrição do tópico",
                            },
                            "status": {
                                "bsonType": "string",
                                "enum": ["ativo", "inativo"],
                                "description": "Status do tópico",
                            },
                            "accepted": {
                                "bsonType": "bool",
                                "description": "Se o usuário aceitou o tópico",
                            },
                        },
                    },
                },
            },
        }
    }
    try:
        if "user_acceptance_collection" not in db.list_collection_names():
            db.create_collection("user_acceptance_collection", validator=acceptance_validator)
            print("Coleção 'user_acceptance_collection' criada com validador.")
    except Exception as e:
        print(f"Aviso ao criar coleção 'user_acceptance': {e}")


def create_indexes(db):
    try:
        # Cria índices apenas se não existirem (o ensure_index é deprecated, create_index é idempotente na maioria dos casos)
        db.species_collection.create_index(
            [("scientific_name", ASCENDING)], unique=True
        )
        db.plots_collection.create_index([("area", ASCENDING)])
        db.yield_collection.create_index([("production", ASCENDING)])
        print("📌 Índices verificados/criados com sucesso!")
    except Exception as e:
        print(f"Aviso ao criar índices: {e}")


def restart_collections(db):
    try:
        db.species_collection.drop()
        db.plots_collection.drop()
        db.yield_collection.drop()
        create_species_collection(db)
        create_plots_collection(db)
        create_yield_collection(db)
        create_indexes(db)
    except Exception as e:
        print(f"Erro ao reiniciar coleções: {e}")


def initialize_mongo_database():
    try:
        # Usa o método connect da classe para garantir a conexão correta
        db = MongoDB.connect()
        if db is None:
            print("Erro crítico: Banco de dados não conectado.")
            return

        create_species_collection(db)
        create_plots_collection(db)
        create_yield_collection(db)
        create_terms_of_use_collection(db)
        create_user_acceptance_collection(db)
        create_indexes(db)
    except Exception as e:
        print(f"Erro na inicialização do banco: {e}")
