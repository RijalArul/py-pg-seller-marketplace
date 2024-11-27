from flask import Blueprint
from controllers.offer import get_offers_controller
from services.redis import RedisService

offer_routes = Blueprint('offers', __name__)

redis_service = RedisService()

@offer_routes.route('/api/offers', methods=['GET'])
def get_offers():
    return get_offers_controller(redis_service)
