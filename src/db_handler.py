import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Récupère les variables d'environnement
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "velib_db")

# URL de connexion PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class DatabaseHandler:
    """
    Classe pour gérer la connexion à PostgreSQL
    """
    
    def __init__(self):
        """
        Initialise la connexion à la base de données
        """
        try:
            self.engine = create_engine(DATABASE_URL)
            self.SessionLocal = sessionmaker(bind=self.engine)
            print(f"✅ Database connection established: {DB_NAME}")
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            self.engine = None
    
    def test_connection(self):
        """
        Teste la connexion à la base de données
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Database connection test: SUCCESS")
                return True
        except Exception as e:
            print(f"❌ Database connection test FAILED: {e}")
            return False
    
    def get_tables(self):
        """
        Récupère la liste des tables dans la base de données
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """))
                tables = [row[0] for row in result]
                print(f"✅ Tables in database: {tables}")
                return tables
        except Exception as e:
            print(f"❌ Error fetching tables: {e}")
            return []

if __name__ == "__main__":
    db = DatabaseHandler()
    db.test_connection()
    db.get_tables()
