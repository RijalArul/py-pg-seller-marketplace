from faker import Faker
import uuid
import random
from services.redis import RedisService
from services.offer import OfferService
from config.connect_db import connect_to_db

def generate_dummy_data_with_redis():
    fake = Faker()
    conn = connect_to_db()
    redis_service = RedisService() 
    offer_service = OfferService(redis_service)  
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

        offer_service.save_offers(offers, sellers)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()
