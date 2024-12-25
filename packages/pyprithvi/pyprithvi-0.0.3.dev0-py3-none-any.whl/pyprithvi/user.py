import json
import requests
from typing import Optional, Union, Dict
from pyprithvi.engine import _get_user_session, set_user_session, get_backend_url
from pyprithvi.engine import get_request, post_request, delete_request, patch_request


def set_session_profile(profile_name: str):
    """Set session profile

    Parameters
    ----------
    profile_name: str
        Sets session profile

    Example
    -------
    >>> pyprithvi.set_session_profile(profile_name='profile')

    Returns
    -------
    None
    """
    api_path = "user/set-session-profile"
    params = {'profile_name': profile_name}
    response = post_request(api_path, params=params)
    if response is not None:
        print(f"{profile_name} is set as your current session profile")

        # gets information on current billing organization
        get_billing_organizations()
    return


def get_session_profile() -> Union[str, None]:
    """Gets profile in current user session

    Example
    -------
    >>> pyprithvi.get_session_profile()
    """
    session = _get_user_session()
    if session is None:
        print("login to start a session")
        return None
    try:
        profile_name = session.cookies['profile_name']
        return profile_name
    except KeyError:
        print('profile name not set')
    return None


def set_session_project(project_name: str):
    """Set session project

    Parameters
    ----------
    project_name: str
        Sets session project

    Example
    -------
    >>> pyprithvi.set_session_project(project_name='project')

    Returns
    -------
    None
    """
    api_path = "user/set-session-project"
    params = {'project_name': project_name}
    response = post_request(api_path, params=params)
    if response is not None:
        print(f"{project_name} is set as your current session project")
    return


def set_billing_organization(billing_org_name: str) -> None:
    """
    Set billing organization
    (To get the list of available billing organizations, use `pyprithvi.list_user_profiles()`)

    Parameters
    ----------
    billing_org_name: str
        billing organization name

    Returns
    -------
    None

    Example
    -------
    >>> pyprithvi.set_billing_organization(billing_org_name='profile')
    """
    api_path = "user/billing-organization"
    json = {'profile_name': billing_org_name}
    response = patch_request(api_path, json=json)
    if response is not None:
        data = response.json()['data']
        print(
            f"{data['name']} is set as your billing organization.\nCurrent balance: {data['balance']}"
        )
    return


def get_session_project() -> Union[str, None]:
    """Gets project in current user session

    Example
    -------
    >>> pyprithvi.get_session_project()
    """
    session = _get_user_session()
    if session is None:
        print("login to start a session")
        return None
    try:
        project_name = session.cookies['project_name']
        return project_name
    except KeyError:
        print('project name not set')
    return None


def list_user_profiles():
    """List all profiles of the users

    Example
    -------
    >>> pyprithvi.list_user_profiles()
    """
    api_path = "user/list-user-profiles"
    response = get_request(api_path)
    if response:
        print(response.json())
    return


def list_all_projects():
    """List all projects of the users

    Example
    -------
    >>> pyprithvi.list_all_projects()
    """
    api_path = "user/list-user-all-projects"
    response = get_request(api_path)
    if response:
        print(response.json())
    return


def get_billing_organizations() -> Optional[Dict]:
    """
    Returns name and balance information of current billing organization

    Returns
    -------
    data: Optional[Dict]
        Dictionary of the type: {'name': 'billing_org_name', 'balance': 100}

    Example
    -------
    >>> pyprithvi.get_billing_organizations()
    """
    api_path = "user/billing-organization"
    response = get_request(api_path)
    if response:
        data = response.json()['data']
        if data is not None:
            print(
                f"{data['name']} is your current billing organization.\nCurrent balance: {data['balance']}"
            )
            return data
    print(
        "No billing organization found. (Current profile will be used as billing organization.)"
    )
    return None


def list_users_in_profile():
    """List users in profile.

    The method allows users to view other collaborators

    Example
    -------
    >>> pyprithvi.list_users_in_profile()
    """
    api_path = "user/list-users-in-profile"
    response = get_request(api_path)
    if response:
        print(response.json())
    return


def add_user_to_org_profile(username: str) -> None:
    """Add user to an organization

    Parameters
    ----------
    username: str
        Username of the user to add to the organization

    Example
    -------
    >>> pyprithvi.add_user_to_org_profile(username='joe')
    """
    params = {'username': username}
    api_path = "user/add-user-to-org-profile"
    response = post_request(api_path, params=params)
    if response:
        response = response.json()
        print(response['detail'])
    return None


def remove_user_from_org_profile(username: str) -> None:
    """Remove user from an organization

    Parameters
    ----------
    username: str
        Username of the user to remove the organization

    Example
    -------
    >>> pyprithvi.add_user_to_org_profile(username='joe')
    """
    params = {'username': username}
    api_path = "user/remove-user-from-org-profile"
    response = delete_request(api_path, params=params)
    if response:
        response = response.json()
        print(response['detail'])
    return None


def update_password(old_password: str, new_password: str):
    """
    Update password

    Parameters
    ----------
    old_password: str
      Old password of user
    new_password: str
      New password of user

    Example
    -------
    >>> pyprithvi.update_password(old_password='oldsecret', new_password='newsecret')
    """
    confirm_old_password = input(
        "Are you sure to update password? If yes, type old password again else type no "
    )
    if confirm_old_password == old_password:
        session = _get_user_session()
        if session is None:
            print("Not signed in")
            return
        response = session.post(get_backend_url() + "user/update/password",
                                data={
                                    'old_password': old_password,
                                    'new_password': new_password
                                })
        return response.json()
    elif confirm_old_password.lower() == 'no':
        print("password update cancelled")
        return None


def get_current_user():
    """Returns information about current logged in user.

    Example
    -------
    >>> pyprithvi.get_current_user()
    {'username': 'test_user', 'email': 'email@example.com', 'namespace': 'test_company', 'full_name': 'John Doe'}
    """
    session = _get_user_session()
    if session is None:
        print("Not signed in")
        return
    current_user = session.get(get_backend_url() + "user/me").content
    return json.loads(current_user)


def create_org(org_name: str,
               aws_bucket: str = 'dfs-chiron-datastore',
               aws_region: str = 'us-east-2') -> None:
    """Create an organization

    Parameters
    ----------
    org_name: str
        Organization name
    aws_bucket: str, default: `dfs-chiron-datastore`
        AWS S3 bucket to use for the organization.
    aws_region: str, default: `us-east-2`
        AWS region to use for the organization.

    Returns
    -------
    None

    Example
    -------
    >>> pyprithvi.create_org(org_name='dfs', aws_bucket='dfs-bucket', aws_region='us-east-2')
    """
    params = {
        'name': org_name,
        'aws_bucket': aws_bucket,
        'aws_region': aws_region
    }
    api_path = 'user/create-org'
    response = post_request(api_path, json=params)
    if response:
        response = response.json()
        print(response['detail'])
    return


def create_project(project_name: str) -> None:
    """Create a project

    Parameters
    ----------
    project_name: str
        Project name

    Returns
    -------
    None

    Example
    -------
    >>> pyprithvi.create_project(project_name='project')
    """
    params = {'project_name': project_name}
    api_path = 'user/create-project'
    response = post_request(api_path, params=params)
    if response:
        response = response.json()
        print(response['detail'])
    return


def get_user_balance() -> None:
    """Get prithvi budget balance of the user in the current profile.

    Example
    -------
    >>> pyprithvi.get_user_balance()
    """
    api_path = 'user/get-chiron-balance'
    response = get_request(api_path)
    if response:
        response = response.json()
        balance = response['balance']
        print(f'user balance is {balance}')
    return


def update_user_balance(difference: str, username: str) -> None:
    """Update prithvi user balance.

    Parameters
    ----------
    username: str
        The username to update
    difference: str
        The amount by which to increase/decrease balance

    Example
    -------
    >>> pyprithvi.update_user_balance(difference=100, username='joe')
    """
    # FIXME Ideally, this should make a request to payment gateway
    api_path = "user/update-chiron-balance"
    params = {'difference': difference, 'username': username}
    response = post_request(api_path, params=params)
    if response:
        response = response.json()
        balance = response['new_balance']
        print(f'user new balance is {balance}')
    return


def get_job_status(job_id: str):
    """
    Getting job status of a Prithvi Job

    Parameters
    ----------
    job_id: str
      Job id associated with the job

    Returns
    -------
    job_status: str
      Status of the job. One among 'STARTING', 'RUNNING', 'SUCCEEDED', 'TERMINATED', 'FAILED'

    Example
    -------
    >>> pyprithvi.get_job_status(job_id='123456')
    """
    session = _get_user_session()
    if session is None:
        print("Not signed in")
        return
    url = get_backend_url() + "user/get-job-status/" + job_id
    response = session.get(url)
    if response.status_code == 200:
        response = response.json()
        set_user_session(session)
        return response["job_status"]
    else:
        return requests.status_codes._codes[response.status_code]


def get_jobs(n_days: Optional[int] = 7,
             offset: Optional[int] = 0,
             limit: Optional[int] = 20):
    """
    Get submitted jobs history

    Parameters
    ----------
    n_days: int, optional, default: 7
      Retrieves jobs created in the last `n_days`
    offset: int, optional, default: 0
      offset used in retrieving job logs
    limit: int, optional, default: 20
      maximum number of job logs to retrieve

    Example
    -------
    >>> pyprithvi.get_jobs()
    """
    session = _get_user_session()
    if session is None:
        print("Not signed in")
        return
    json_params = {'n_days': n_days, 'offset': offset, 'limit': limit}
    response = session.get(get_backend_url() + "user/jobs", params=json_params)
    response = response.json()
    set_user_session(session)
    return response
