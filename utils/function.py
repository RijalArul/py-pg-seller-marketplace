from collections import defaultdict
from itertools import cycle

def apply_round_robin_offers(offers):
    grouped_offers = defaultdict(list)
    for offer in offers:
        seller_id = offer.get("seller_id")
        grouped_offers[seller_id].append(offer)
    
    round_robin_result = []
    sellers_cycle = cycle(grouped_offers.keys())
    while len(round_robin_result) < len(offers):
        seller_id = next(sellers_cycle)
        if grouped_offers[seller_id]:
            round_robin_result.append(grouped_offers[seller_id].pop(0))
    
    return round_robin_result