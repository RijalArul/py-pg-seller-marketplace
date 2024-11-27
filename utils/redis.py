import redis
import json

def connect_to_redis():
    return redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

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

        redis_conn.delete("offers")
        redis_conn.set("offers", json.dumps(all_offers))

        print("All offers have been saved to Redis under the key 'offers'.")
    except Exception as e:
        print(f"Error saving to Redis: {e}")
