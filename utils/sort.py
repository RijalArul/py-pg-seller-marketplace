def sort_data(data, sort_by, sort_order):
    reverse = sort_order == 'desc'
    return sorted(data, key=lambda x: x.get(sort_by, 0), reverse=reverse)