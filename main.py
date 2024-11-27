from flask import Flask, jsonify, request
from constants.redis import redis_key_offers
from utils.filter import filter_data_by_target
from utils.function import apply_round_robin_offers
from utils.paginaton import paginate_data_with_redis
from utils.sort import sort_data
from services.redis import RedisService
from services.offer import OfferService


app = Flask(__name__)

@app.route('/api/offers', methods=['GET'])
def get_offers():
    redis_conn = RedisService()
    offer_service = OfferService(redis_conn)

    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    sort_by = request.args.get('sort_by', 'price')
    sort_order = request.args.get('sort_order', 'asc')
    category = request.args.get('category', None)

    offers, error = offer_service.fetch_offers()
    if error:
        return jsonify({"error": error}), 404 if "No offers" in error else 500
    
    offers = filter_data_by_target(offers, 'category', category)
    offers = sort_data(offers, sort_by, sort_order)
    offers = apply_round_robin_offers(offers)
    paginated_offers = paginate_data_with_redis(offers, page, limit)


    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(offers),
        "offers": paginated_offers
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)

