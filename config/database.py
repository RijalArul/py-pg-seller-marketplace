import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error while creating database: {e}")

# Eksekusi fungsi
if __name__ == "__main__":
    create_or_replace_database()
