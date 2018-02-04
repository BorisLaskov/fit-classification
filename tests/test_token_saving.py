from classification import sessionutils
from tempfile import gettempdir
import os
import uuid
import flexmock


def test_token_saving():
    path = os.path.join(gettempdir(), f'myfolder-{uuid.uuid4()}',
                        'my-other-folder', 'file.txt')
    mocked_utils = flexmock(sessionutils)
    mocked_utils.TOKEN_FILE_PATH = path

    assert not os.path.isfile(path)

    token = {'token': 'Bearer qwerty', 'expires_in': 3600}
    sessionutils.save_token(token)

    assert os.path.isfile(path)
    read_token = sessionutils.load_token()
    assert read_token == token
