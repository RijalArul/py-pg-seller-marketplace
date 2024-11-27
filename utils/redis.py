import redis
import json
from constants.redis import redis_key_offers

def connect_to_redis():
    return redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

def fetch_data_from_redis(redis_conn, redis_key):
    offers_string = redis_conn.get(redis_key)
    if not offers_string:
        return None, "No offers found in Redis"
    
    try:
        return json.loads(offers_string), None
    except json.JSONDecodeError:
        return None, "Error decoding offers data from Redis"

def save_offers_to_redis(redis_conn, offers, sellers):
    try:
        all_offers = []

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

            all_offers.append(offer_data)

        redis_conn.delete(redis_key_offers)
        redis_conn.set(redis_key_offers, json.dumps(all_offers))

        print("All offers have been saved to Redis under the key 'offers'.")
    except Exception as e:
        print(f"Error saving to Redis: {e}")
