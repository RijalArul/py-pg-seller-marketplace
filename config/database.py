import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from services.redis import RedisService
from constants.redis import redis_key_offers
from config.load_env import Config

def create_or_replace_database():
    try:
        connection = psycopg2.connect(
            dbname=Config.POSTGRES_DBNAME,
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD,
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
        cursor = connection.cursor()

        cursor.execute("DROP DATABASE IF EXISTS \"g2g_offer_management\";")
        print("Existing database 'g2g_offer_management' dropped (if it existed).")

        cursor.execute("CREATE DATABASE \"g2g_offer_management\";")
        print("Database 'g2g_offer_management' created successfully!")

        redis_service = RedisService()

        if redis_service.exists(redis_key_offers):
            redis_service.delete(redis_key_offers)
            print("Redis key 'offers' has been deleted.")


        cursor.close()
        connection.close()
        

    except Exception as e:
        print(f"Error while creating database: {e}")

if __name__ == "__main__":
    create_or_replace_database()
