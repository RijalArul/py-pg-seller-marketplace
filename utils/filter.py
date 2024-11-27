def filter_data_by_target(offers, target_key, target_value):
    if not target_key:
        return offers
    return [offer for offer in offers if offer.get(target_key) == target_value]