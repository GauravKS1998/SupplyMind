from sqlalchemy import asc, desc


def apply_sorting(query, model, sort_by, direction):

    if not sort_by:
        return query

    column = getattr(model, sort_by, None)

    if column is None:
        return query

    if direction.lower() == "desc":
        return query.order_by(desc(column))

    return query.order_by(asc(column))
