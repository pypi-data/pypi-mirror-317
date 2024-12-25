from pyprithvi.engine import delete_request


def delete_user():
    api_path = 'user/delete-user'
    response = delete_request(api_path)
    if response:
        response = response.json()
        print(response['detail'])
    return


def delete_org(org_name: str):
    api_path = 'user/delete-org'
    params = {'org_name': org_name}
    response = delete_request(api_path, params=params)
    if response:
        response = response.json()
        print(response['detail'])
    return


def delete_project(project_name: str):
    api_path = 'user/delete-project'
    params = {'project_name': project_name}
    response = delete_request(api_path, params=params)
    if response:
        response = response.json()
        print(response['detail'])
    return
