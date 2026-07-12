def get_or_raise(entity, exception):

    if entity is None:
        raise exception

    return entity


def ensure_active(entity, exception):
    if not entity.is_active:
        raise exception
