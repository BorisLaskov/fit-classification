def remove_none_entries(dictionary):
    keys = [k for k in dictionary]
    for k in keys:
        del dictionary[k]


def get_body_or_empty_dict(object):
    return object.body if object is not None else dict()
