import betamax
import pytest
import os
from requests import HTTPError
from classification import classification


TOKEN = 'dummy'


with betamax.Betamax.configure() as beta_config:
    client_id = os.environ.get('PYTEST_CLIENT_ID')
    client_secret = os.environ.get('PYTEST_CLIENT_SECRET')
    if client_id is not None and client_secret is not None:
        c = classification.Classification(client_id, client_secret)
        TOKEN = c.session.token.get('access_token')
        beta_config.default_cassette_options['record_mode'] = 'all'

    else:
        beta_config.default_cassette_options['record_mode'] = 'none'

    beta_config.cassette_library_dir = 'tests/fixtures/cassettes'
    beta_config.define_cassette_placeholder('<TOKEN>', TOKEN)

    first_name = os.environ.get('PYTEST_FIRST_NAME', 'dummy')
    last_name = os.environ.get('PYTEST_LAST_NAME', 'dummy')
    email = os.environ.get('PYTEST_EMAIL', 'dummy')
    beta_config.define_cassette_placeholder('<FIRST_NAME>', first_name)
    beta_config.define_cassette_placeholder('<LAST_NAME>', last_name)
    beta_config.define_cassette_placeholder('<EMAIL>', email)


@pytest.fixture
def session(betamax_session):
    betamax_session.headers.update({'Accept-Encoding': 'identity',
                                    'Authorization': 'Bearer ' + TOKEN})
    return betamax_session


@pytest.fixture
def client(session):
    c = classification.Classification('dummy', 'dummy', session=session)
    c.API_URL.replace('classification-dev', 'classification')
    return c


def test_demo_success(client):
    resp = client.find_student_classification('MI-PYT', 'laskobor')

    tasks = resp['studentClassificationFullDtos']
    value = None

    for task in tasks:
        if task['identifier'] == 'total':
            value = int(task['value'])

    assert value is not None
    assert value == 51


def test_demo_fail_401(client):
    with pytest.raises(HTTPError):
        client.find_student_group_classifications('MI-PYT', group_code='ALL')
