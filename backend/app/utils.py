def flatten(obj):
    if isinstance(obj, list):
        for item in obj:
            yield from flatten(item)
    else:
        yield obj
