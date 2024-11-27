import psycopg2
def connect_to_db():
    return psycopg2.connect(
        dbname="g2g_offer_management",
        user="postgres",
        password="postgres",
        host="localhost"
    )