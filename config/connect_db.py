import psycopg2
from config.load_env import Config

def connect_db():
    try:
        connection = psycopg2.connect(
            dbname=Config.POSTGRES_DB,
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD,
        )
        print("Connected to PostgreSQL")
        return connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
