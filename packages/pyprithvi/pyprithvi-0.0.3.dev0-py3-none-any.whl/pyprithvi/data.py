"""
"""
import os
import tempfile
from http import HTTPStatus
import pandas as pd
import json
import logging
import urllib.request as req
from typing import Optional, Any, Union
from pyprithvi.utils import serialization
from pyprithvi.user import get_session_profile, get_session_project

from pyprithvi.engine import _get_user_session, set_user_session, get_backend_url
from pyprithvi.engine import get_request, delete_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_data():
    """List datastore data visible to this user.

    Example
    -------
    >>> pyprithvi.list_data()
    """
    api_path = "data/listdata"
    response = get_request(api_path)
    if response.status_code == 200:
        response = response.json()
        print(response["contents"])
    return


def list_data_v2(address: Optional[str] = None, n_pages: int = 1) -> None:
    """
    List datastore files and folders from a specific directory address (format: Prithvi address)
    in the form of pages of 100 items each. If no address is given as input, the files and folders
    from the project level are fetched.

    Parameters
    ----------
    address: Optional[str]
        Prithvi address of the directory to retrieve files and folders from.
    n_pages: int
        Number of pages to fetch. Each page contains 100 items.

    Example
    -------
    >>> pyprithvi.list_data_v2(address="chiron://profile/project/folder/", n_pages=3)
    """
    api_path: str = "data/listdata-pagination"
    if address is None:
        address = f"chiron://{get_session_profile()}/{get_session_project()}/"
    continuation_token: Optional[str] = ""
    page: int = 1
    while page <= n_pages and continuation_token is not None:
        params = {
            'address': address,
            'limit': 100,
            'continuation_token': continuation_token
        }
        response = get_request(api_path, params=params)
        if response.status_code == 200:
            response = response.json()
            print("page ", page)
            print(response["contents"])
            continuation_token = response['nextContinuationToken']
            page += 1
            print()
        else:
            print(
                "Error occured while fetching the data from the given address.")
            break
    return


def upload_file(datastore_filename: str,
                filename: str,
                description: Optional[str] = '') -> str:
    """Upload file to the datastore.

    Parameters
    ----------
    datastore_filename: str
      The file identifier (filename) in the datastore
    filename: str
      The local file on disk which is to be uploaded to the datastore
    description: str
      A description about the data

    Returns
    -------
    datastore_address: str
      The datastore address of the uploaded dataset

    Example
    -------
    >>> pyprithvi.upload_file(datastore_filename='temp.csv', filename='path/to/file/on/disk.csv', description='a description of dataset')
    chiron://namespace/username/working_dir/temp.csv
    """
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    sess = _get_user_session()
    m = MultipartEncoder(
        fields={
            'filename': datastore_filename,
            'file': (filename, open(filename, 'rb'), 'text/plain'),
            'description': description
        })
    response = sess.post(get_backend_url() + "data/uploaddata",
                         data=m,
                         headers={'Content-Type': m.content_type})
    set_user_session(sess)
    if response.status_code == HTTPStatus.OK.value:
        response = response.json()
        return response['dataset_address']
    elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value:
        print("Internal server error")
        return None
    elif response.status_code >= 400:
        detail = response.json()
        print(detail['detail'])
        return None
    return None


def upload_model(path: str) -> Union[str, None]:
    """
    Upload a model to the datastore
    The model should be a directory containing the model files
    and a ``config.yaml`` file with the model configuration.

    Parameters
    ----------
    path: str
      Path to the model directory on disk

    Returns
    -------
    model_address: str
      The datastore address of the uploaded model
    """
    sess = _get_user_session()
    model_name = os.path.basename(path)

    # get absolute path of the model directory
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    if not os.path.exists(path):
        print(f"Model path: <{path}> does not exist")
        return None

    # check if the model path contains any subdirectories
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            print("Model path should not contain any subdirectories")
            return None
    files_names = [
        f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
    ]
    files = [('files', open(os.path.join(path, f), 'rb')) for f in files_names]
    response = sess.post(get_backend_url() + "data/uploadmodel",
                         files=files,
                         data={
                             'filenames': files_names,
                             'model_name': model_name
                         })
    if response.status_code == HTTPStatus.OK.value:
        response = response.json()
        return response['model_address']
    elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value:
        print("Internal server error")
        return None
    elif response.status_code >= 400:
        detail = response.json()
        print(detail['detail'])
        return None
    return None


# FIXME Should we call this as address or filename?
def delete_file(address: str) -> None:
    """Delete a file in datastore

    Parameters
    ----------
    address: str
      Address of the object to delete

    Example
    -------
    >>> pyprithvi.delete_file(address='zinc5k.csv')
    """
    api_path = "data/delete"
    params = {'fileName': address}
    response = delete_request(api_path, params=params)
    if response and response.status_code == HTTPStatus.OK.value:
        response = response.json()
        print(response['detail'])
        return True
    return False


def upload_data_from_memory(data: Any,
                            datastore_filename: str,
                            description: Optional[str] = '') -> Optional[str]:
    # TODO A dataset in memory should be be converted to a suitable format
    # and then exported. Do we need this?
    """Uploads dataset in in-memory

    Parameters
    ----------
    data: Any
      An inmemory data object like pandas.DataFrame
    datastore_filename: str
      The file identifier (filename) in the datastore
    description: str
      A description about the file

    Note
    ----
    Supported data types are pandas.DataFrame, deepchem.data.Dataset, deepchem.model.Model

    Example
    -------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'a': [1, 2, 3, 4, 5]})
    >>> pyprithvi.upload_data_from_memory(data=df, datastore_filename='a.csv', description='a dummy dataframe')
    chiron://namespace/username/working_dir/a.csv
    """
    with tempfile.TemporaryDirectory() as tempdir:
        if isinstance(data, pd.DataFrame):
            temp_path = os.path.join(tempdir, 'temp.csv')
            data.to_csv(temp_path, index=False)
            return upload_file(datastore_filename, temp_path, description)
        else:
            raise ValueError("Other data types not supported")
            return None


def get(address: str, fetch_sample: bool = False) -> Any:
    """Fetches data from the datastore.

    Parameters
    ----------
    address: str
      Chiron address of object to retrieve from the dataset

    Example
    -------
    >>> pyprithvi.get('chiron://namespace/username/working_dir/file.extension')
    """
    sess = _get_user_session()
    response = sess.get(get_backend_url() + "data/get",
                        params={
                            'filename': address,
                            'fetch_sample': fetch_sample
                        })
    if response.status_code == 404:
        print("Object not found")
        return
    elif response.status_code == 400:
        response = response.json()
        print(response['detail'])
        return
    set_user_session(sess)

    if address.endswith('.csv'):
        content = response.json()['contents']
        df = serialization.csv_bytes_to_dataframe(content.encode('utf-8'))
        return df
    elif address.endswith('.cdc') or address.endswith('.cmc'):
        card = response.json()['contents']
        card = {k: v for k, v in card.items() if v is not None}
        return card
    elif address.endswith('.json'):
        return response.json()['contents']
    return


def download_file(address: str, filename: str):
    """Download file from datastore

    Parameters
    ----------
    address: str
      Prithvi address of object to retrieve from the dataset
    filename: str
      Filename to write the downloaded object

    Returns
    -------
    bytes: bytes of object data

    Example
    -------
    >>> pyprithvi.download('chiron://namespace/profile/project/working_dir/file.extension')
    """
    api_path = "data/get-presigned-url-download"
    response = get_request(api_path, params={'filename': address})
    if response and response.status_code == 200:
        download_url = json.loads(response.content)['presigned_url']
        for i in range(1, 5):
            try:
                with req.urlopen(download_url,
                                 timeout=20) as d, open(filename,
                                                        "wb") as opfile:
                    data = d.read()
                    opfile.write(data)
                    opfile.close()
            except ConnectionResetError:
                logger.info(f"Download failed, retrying {i}/4")
                continue
            except Exception:
                break
            logger.info("File download successful!")
            return True
    logger.info("File download failed")
    return False


def download_model(address: str, filename: str):
    """Download model from datastore as a zip file

    Parameters
    ----------
    address: str
      Prithvi address of object to retrieve from the dataset
    filename: str
      Filename to write the downloaded object

    Returns
    -------
    bytes: bytes of object data

    Example
    -------
    >>> pyprithvi.download_model('chiron://profile/project/model_name')
    """
    return download_file(address, filename)
