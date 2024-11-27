def paginate_data_with_redis(data, page, limit):
    start = (page - 1) * limit
    end = start + limit
    return data[start:end]