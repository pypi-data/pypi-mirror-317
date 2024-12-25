import os
import requests
import json as Json
import numpy as np
from http import HTTPStatus
from typing import Optional, List, Dict

# TODO Ideally, this should be the public IP which the user
# connects to (the IP of EC2 instance)
_BACKEND_URL = "http://localhost:8000/"
_SESSION = None

# Parameters to fetch recent jobs and update the status if required
N_DAYS = 7
OFFSET = 0
LIMIT = 2000

__all__ = ['set_backend_url', 'healthcheck', 'login', 'login_access_token']


def set_backend_url(url: str):
    """
    Set address of Prithvi server.

    .. note::

        The backend URL of the production server is
        ``BACKEND_URL``.

    Parameters
    ----------
    url: str
        Address of Prithvi server.

    Example
    -------
    >>> import pyprithvi
    >>> pyprithvi.set_backend_url("http://localhost:8000/")
    """
    global _BACKEND_URL
    _BACKEND_URL = url


def get_backend_url() -> str:
    """Get address of Prithvi server.

    PyPrithvi sends commands to a running pyprithvi server. This
    function returns the address for the current server.
    """
    global _BACKEND_URL
    return _BACKEND_URL


def set_user_session(session: requests.Session):
    global _SESSION
    _SESSION = session


def _get_user_session() -> Optional[requests.Session]:
    global _SESSION
    return _SESSION


def post_request(api_path,
                 *,
                 params: Dict = None,
                 json: Dict = None,
                 data: Dict = None):
    if params is None:
        params = dict()
    if json is None:
        json = dict()
    if data is None:
        data = dict()
    backend_url = get_backend_url()
    api_endpoint = backend_url + api_path
    session = _get_user_session()
    if not session:
        session = requests.Session()
    try:
        response = session.post(api_endpoint,
                                params=params,
                                data=data,
                                json=json)
    except requests.exceptions.ConnectionError:
        print("backend not available")
        return None
    set_user_session(session)
    if response.status_code == HTTPStatus.OK.value:
        return response
    elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value:
        print("Internal server error")
        return None
    elif response.status_code >= 400:
        detail = response.json()
        if 'detail' in detail.keys():
            print(detail['detail'])
        elif 'status' in detail.keys():
            print(detail['status'])
        return None


def patch_request(api_path,
                  *,
                  params: Dict = None,
                  json: Dict = None,
                  data: Dict = None):
    if params is None:
        params = dict()
    if json is None:
        json = dict()
    if data is None:
        data = dict()
    backend_url = get_backend_url()
    api_endpoint = backend_url + api_path
    session = _get_user_session()
    if not session:
        session = requests.Session()
    try:
        response = session.patch(api_endpoint,
                                 params=params,
                                 data=data,
                                 json=json)
    except requests.exceptions.ConnectionError:
        print("backend not available")
        return None
    set_user_session(session)
    if response.status_code == HTTPStatus.OK.value:
        return response
    elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value:
        print("Internal server error")
        return None
    elif response.status_code >= 400:
        detail = response.json()
        if 'detail' in detail.keys():
            print(detail['detail'])
        elif 'status' in detail.keys():
            print(detail['status'])
        return None


def get_request(api_path,
                *,
                params: Dict = None,
                json: Dict = None,
                data: Dict = None):
    if params is None:
        params = dict()
    if json is None:
        json = dict()
    if data is None:
        data = dict()
    backend_url = get_backend_url()
    api_endpoint = backend_url + api_path
    session = _get_user_session()
    if not session:
        session = requests.Session()
    try:
        response = session.get(api_endpoint,
                               params=params,
                               data=data,
                               json=json)
    except requests.exceptions.ConnectionError:
        print("backend not available")
        return None
    set_user_session(session)
    if response.status_code == 200:
        return response
    elif response.status_code == 500:
        print("Internal server error")
        return None
    elif response.status_code >= 400:
        detail = response.json()
        if 'detail' in detail.keys():
            print(detail['detail'])
        elif 'status' in detail.keys():
            print(detail['status'])
        return None


def delete_request(api_path,
                   *,
                   params: Dict = None,
                   json: Dict = None,
                   data: Dict = None):
    if params is None:
        params = dict()
    if json is None:
        json = dict()
    if data is None:
        data = dict()
    backend_url = get_backend_url()
    api_endpoint = backend_url + api_path
    session = _get_user_session()
    if not session:
        session = requests.Session()
    try:
        response = session.delete(api_endpoint,
                                  params=params,
                                  data=data,
                                  json=json)
    except requests.exceptions.ConnectionError:
        print("backend not available")
        return None
    set_user_session(session)
    if response.status_code == 200:
        return response
    elif response.status_code == 500:
        print("Internal server error")
        return None
    elif response.status_code >= 400:
        detail = response.json()
        # TODO We have to standardize return data in app
        if 'detail' in detail.keys():
            print(detail['detail'])
        elif 'status' in detail.keys():
            print(detail['status'])
        return None


def healthcheck():
    """Performs a basic healthcheck that server is up and running.

    Example
    -------
    >>> pyprithvi.healthcheck()
    """
    api_path = "healthcheck"
    response = get_request(api_path)
    if response:
        print(response.json())
    return None


def login(username: str, password: str):
    """Logs in to server with provided username and password.

    Parameters
    ----------
    username: str
      Username to login as
    password: str
      Password to login with.

    Example
    -------
    >>> pyprithvi.login(username='test_user', password='secret123')
    """
    login_data = {'username': username, 'password': password}
    api_path = "login"
    response = post_request(api_path, data=login_data)
    if response:
        response = response.json()
        session = _get_user_session()
        session.headers.update(
            {"Authorization": 'Bearer ' + response['access_token']})
        set_user_session(session)
        print("Logged in successfully")
        json_params = {'n_days': N_DAYS, 'offset': OFFSET, 'limit': LIMIT}
        try:
            jobs_response = session.get(get_backend_url() + "user/jobs",
                                        params=json_params)
            jobs_response = jobs_response.json()
            print(
                f"{len(jobs_response)} job(s) checked (submitted in last {N_DAYS} days)"
            )
        except Exception:
            print("Failed to fetch recently submited jobs")
    return None


def login_access_token(token: str):
    """
    Logs in to server with provided token.
    This login session is for a short duration and expires quickly.

    Parameters
    ----------
    token: str
      token for temporary access
    """
    api_path = "login-access-token"
    response = post_request(api_path, params={'token': token})
    if response:
        response = response.json()
        session = _get_user_session()
        session.headers.update(
            {"Authorization": 'Bearer ' + response['access_token']})
        set_user_session(session)
        print("Logged in successfully")
        return True
    return False


def logout():
    """Logs out the user.

    Example
    -------
    >>> pyprithvi.logout()
    """
    session = _get_user_session()
    if session is not None:
        session.headers.pop('Authorization')
        set_user_session(session)
        print("Logged out successfully")
    return None


def visualize(dataset_address, kind, x, y, output_dir="cache"):
    request = get_backend_url(
    ) + f"build_visualization?dataset_id={dataset_address}&kind={kind}&x={x}&y={y}"
    response = requests.post(request)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, "visualization.png"), "wb+") as f:
        f.write(response.content)
    return response.content


def build_molecular_property_prediction_model(
        model_address: str,
        dataset_address: str,
        model_type: str,
        description: Optional[str] = None,
        foundation_address: Optional[str] = None):
    if foundation_address is None:
        request = get_backend_url(
        ) + f"build_mpm?model_address={model_address}&dataset_address={dataset_address}&model_type={model_type}&description={description}"
    else:
        request = get_backend_url(
        ) + f"build_mpm?model_address={model_address}&dataset_address={dataset_address}&model_type={model_type}&description={description}&foundation_address={foundation_address}"

    response = requests.post(request)
    response_content = Json.loads(response.content.decode('utf-8'))
    return response_content["model_address"]


def query_model(model_address: str, query: str):
    request = get_backend_url(
    ) + f"query_model?model_address={model_address}&query={query}"
    response = requests.post(request)
    response_content = Json.loads(response.content.decode('utf-8'))
    return response_content["prediction"]


def screen_library(model_address: str, dataset_address: str):
    request = get_backend_url(
    ) + f"screen_library?model_address={model_address}&dataset_address={dataset_address}"
    response = requests.post(request)
    response_content = Json.loads(response.content.decode('utf-8'))
    # TODO: Using eval is dangerous. Find a better way
    return np.array(eval(response_content["result"]))


def multiobjective_optimization(dataset_address: str,
                                model_addresses: List[str]):
    # TODO: How do we pass multiple model addresses in POST?
    request = get_backend_url(
    ) + f"multiobjective_optimization?dataset_address={dataset_address}"
    response = requests.post(request)
    response_content = Json.loads(response.content.decode('utf-8'))
    return response_content["prediction"]
