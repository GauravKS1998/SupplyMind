def apply_filter(query, model, **filters):

    for field, value in filters.items():

        if value is None:
            continue

        column = getattr(model, field, None)

        if column is not None:
            query = query.filter(column == value)

    return query
