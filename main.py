from flask import Flask, jsonify, request
from utils.redis import connect_to_redis
import json
from collections import defaultdict
from itertools import cycle
from constants.redis import redis_key_offers

app = Flask(__name__)

@app.route('/api/offers', methods=['GET'])
def get_offers():
    redis_conn = connect_to_redis()

    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    sort_by = request.args.get('sort_by', 'price')
    sort_order = request.args.get('sort_order', 'asc')
    category_filter = request.args.get('category', None) 

    offers_key = redis_key_offers

    offers_string = redis_conn.get(offers_key)

    if not offers_string:
        return jsonify({"error": "No offers found in Redis"}), 404

    try:
        all_offers = json.loads(offers_string)
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding offers data from Redis"}), 500

    if category_filter:
        all_offers = [offer for offer in all_offers if offer.get("category") == category_filter]

    if sort_by == 'price':
        if sort_order == 'asc':
            all_offers = sorted(all_offers, key=lambda x: x.get('price', 0))
        elif sort_order == 'desc':
            all_offers = sorted(all_offers, key=lambda x: x.get('price', 0), reverse=True)

    grouped_offers = defaultdict(list)
    for offer in all_offers:
        seller_id = offer.get("seller_id")
        grouped_offers[seller_id].append(offer)

    round_robin_result = []
    sellers_cycle = cycle(grouped_offers.keys())
    while len(round_robin_result) < len(all_offers):
        seller_id = next(sellers_cycle)
        if grouped_offers[seller_id]:
            round_robin_result.append(grouped_offers[seller_id].pop(0))

    start = (page - 1) * limit
    end = start + limit
    paginated_offers = round_robin_result[start:end]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(all_offers), 
        redis_key_offers: paginated_offers
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)
