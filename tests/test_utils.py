from classification import utils
import pytest
import flexmock
from requests import HTTPError


@pytest.mark.parametrize(
    ['code', 'body', 'expected_code', 'result'],
    [(204, None, 204, None),
     (200, {}, 200, None),
     (200, {'my': 'data'}, 200, {'my': 'data'}),
     (201, {'error': 'message'}, 201, None)]
)
def test_get_body_or_raise_error_positive(code, body, expected_code, result):
    def body_or_exception():
        if body is not None and 'error' in body:
            raise ValueError
        else:
            return body

    resp = flexmock(status_code=code,
                    json=body_or_exception)
    assert utils.get_body_or_raise_error(resp, expected_code) == result


def test_get_body_or_raise_error_error():
    def raise_error():
        raise HTTPError

    resp = flexmock(status_code=401,
                    raise_for_status=raise_error)

    with pytest.raises(HTTPError):
        utils.get_body_or_raise_error(resp, 200)


@pytest.fixture
def body_dict():
    return {'my': {'complex': 'dict', 'with': 'data'}}


def test_make_dict_body_from_dict(body_dict):
    assert utils.make_dict_body(body_dict) == body_dict


def test_make_dict_body_from_object(body_dict):
    object = flexmock(to_dict=lambda: body_dict)
    assert utils.make_dict_body(object) == body_dict


def test_remove_none_entries():
    dict_without_nones = {'k1': 'v1', 'k2': 'v2'}

    dict_with_nones = dict(dict_without_nones)
    dict_with_nones['k3'] = None
    dict_with_nones['k4'] = None

    assert dict_with_nones != dict_without_nones

    utils.remove_none_entries(dict_with_nones)

    assert dict_with_nones == dict_without_nones
