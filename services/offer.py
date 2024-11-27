from constants.redis import redis_key_offers
class OfferService:

    def __init__(self, redis_service):
        self.redis_service = redis_service

    def save_offers(self, offers, sellers):
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

            self.redis_service.delete_data(redis_key_offers)
            self.redis_service.save_data(redis_key_offers, all_offers)

        except Exception as e:
            print(f"Error saving offers to Redis: {e}")

    def fetch_offers(self):
        return self.redis_service.fetch_data(redis_key_offers)