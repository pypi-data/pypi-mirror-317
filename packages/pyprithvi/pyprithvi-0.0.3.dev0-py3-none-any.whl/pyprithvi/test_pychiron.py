import pyprithvi
import pytest

BACKEND_URL = 'BACKEND_URL'
DEFAULT_PROFILE = 'test-profile'
DEFAULT_PROJECT = 'test-project'


@pytest.fixture(name='init_client')
def test_client():
    pyprithvi.set_backend_url(BACKEND_URL)
    pyprithvi.healthcheck()
    pyprithvi.login(username='pychiron_unit_test', password='secret')
    pyprithvi.set_session_profile(DEFAULT_PROFILE)
    pyprithvi.set_session_project(DEFAULT_PROJECT)


def test_upload_model(init_client):
    model_path = 'pyprithvi/pyprithvi/tests/assets/gcn'
    model_address = pyprithvi.upload_model(model_path)
    assert model_address is not None
    assert model_address == f"chiron://{DEFAULT_PROFILE}/{DEFAULT_PROJECT}/gcn"
