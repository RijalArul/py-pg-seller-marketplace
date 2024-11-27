import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from utils.redis import connect_to_redis
from constants.redis import redis_key_offers

def create_or_replace_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",  
            user="postgres",
            password="postgres",
            host="localhost",
            port=5432  
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
        cursor = conn.cursor()

        cursor.execute("DROP DATABASE IF EXISTS \"g2g_offer_management\";")
        print("Existing database 'g2g_offer_management' dropped (if it existed).")

        cursor.execute("CREATE DATABASE \"g2g_offer_management\";")
        print("Database 'g2g_offer_management' created successfully!")

        redis_conn = connect_to_redis()

        if redis_conn.exists(redis_key_offers):
            redis_conn.delete(redis_key_offers)
            print("Redis key 'offers' has been deleted.")


        cursor.close()
        conn.close()
        

    except Exception as e:
        print(f"Error while creating database: {e}")

if __name__ == "__main__":
    create_or_replace_database()
