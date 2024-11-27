from flask import Flask, jsonify, request
from utils.redis import connect_to_redis
import json

app = Flask(__name__)

@app.route('/api/offers', methods=['GET'])
def get_offers():
    redis_conn = connect_to_redis()

    page = int(request.args.get('page', 1))  
    limit = int(request.args.get('limit', 10))  
    sort_by = request.args.get('sort_by', 'price') 
    sort_order = request.args.get('sort_order', 'asc')  
    category_filter = request.args.get('category', None)  

    offers_key = "offers"

    offers_string = redis_conn.get(offers_key)

    if not offers_string:
        return jsonify({"error": "No offers found in Redis"}), 404

    try:
        all_offers = json.loads(offers_string)
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding offers data from Redis"}), 500

    if category_filter:
        all_offers = [offer for offer in all_offers if offer.get("category") == category_filter]

    if sort_by and sort_order:
        all_offers = sorted(all_offers, key=lambda x: x.get(sort_by, 0), reverse=(sort_order == 'desc'))

    start = (page - 1) * limit
    end = start + limit
    paginated_offers = all_offers[start:end]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(all_offers), 
        "offers": paginated_offers
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)
