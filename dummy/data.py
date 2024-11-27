import psycopg2
import redis
from faker import Faker
import random
import uuid

# Koneksi ke PostgreSQL
def connect_to_db():
    return psycopg2.connect(
        dbname="g2g_offer_management",
        user="postgres",
        password="postgres",
        host="localhost"
    )

# Koneksi ke Redis
def connect_to_redis():
    return redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def save_offers_to_redis(redis_conn, offers, sellers):
    try:
        pipeline = redis_conn.pipeline()

        seller_map = {seller[0]: {"name": seller[1], "level": seller[2]} for seller in sellers}

        for offer in offers:
            offer_id, seller_id, category, title, price = offer

            seller_name = seller_map[seller_id]["name"]
            seller_level = seller_map[seller_id]["level"]

            offer_data = {
                "offer_id": offer_id,
                "seller_id": seller_id,
                "title": title,
                "seller_name": seller_name,
                "seller_level": seller_level,
                "price": f"{price:.2f} MYR",
                "category": category,
                "duration": "10 mins",  
                "min_qty": "Min. 1"    
            }

            pipeline.hmset(f"offer:{offer_id}", offer_data)

        pipeline.execute()
        print("Offers already saved to Redis within seller_id and offer_id!")
    except Exception as e:
        print(f"Error save to Redis: {e}")

def generate_dummy_data_with_redis():
    fake = Faker()
    conn = connect_to_db()
    redis_conn = connect_to_redis()
    cursor = conn.cursor()

    try:
        sellers = []
        for _ in range(20):  
            seller_id = str(uuid.uuid4())
            seller_name = fake.name()
            seller_level = f"Level {random.randint(100, 200)}" 
            sellers.append((seller_id, seller_name, seller_level))

        cursor.executemany("""
            INSERT INTO seller (id, name, email)
            VALUES (%s, %s, %s);
        """, [(seller[0], seller[1], fake.email()) for seller in sellers])

        print(f"Inserted {len(sellers)} sellers into the database.")

        offers = []
        categories = ['Games', 'Tools', 'Accounts', 'Premium Content']
        for _ in range(200): 
            offer_id = str(uuid.uuid4())
            seller_id = random.choice(sellers)[0]
            category = random.choice(categories)
            title = f"No.{random.randint(5000, 6000)}: {category} - Heroes {random.randint(60, 99)}%"
            price = round(random.uniform(100, 1500), 2)
            offers.append((offer_id, seller_id, category, title, price))

        cursor.executemany("""
            INSERT INTO offer (id, seller_id, category, title, price)
            VALUES (%s, %s, %s, %s, %s);
        """, offers)

        print(f"Inserted {len(offers)} offers into the database.")

        save_offers_to_redis(redis_conn, offers, sellers)

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_dummy_data_with_redis()
