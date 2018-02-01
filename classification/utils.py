def remove_none_entries(dictionary):
    keys = [k for k in dictionary]
    for k in keys:
        del dictionary[k]


def get_body_or_empty_dict(object):
    return object.body if object is not None else dict()


def get_body_or_raise_error(resp, exp_code):
    if resp.status_code == exp_code and exp_code == 204:
        return None  # Since 204 is for 'No Content'

    if resp.status_code == exp_code:
        try:
            body = resp.json()
            if len(body) == 0:
                return None
            else:
                return body

        except ValueError:
            # For the requests with 'optional' body
            # that can return 201, for example
            return None

    resp.raise_for_status()
