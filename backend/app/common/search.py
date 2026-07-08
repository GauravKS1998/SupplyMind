from sqlalchemy import or_


def apply_search(query, columns, search):

    if not search:
        return query

    conditions = []

    for column in columns:
        conditions.append(column.ilike(f"%{search}%"))

    return query.filter(or_(*conditions))
