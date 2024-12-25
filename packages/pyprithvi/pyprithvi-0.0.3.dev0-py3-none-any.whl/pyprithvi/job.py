from pyprithvi.engine import post_request


def terminate_job(job_id: str):
    """
    Terminate an AWS Batch Job.

    Parameters
    ----------
    job_id: str
      Job id associated with the job

    Example
    -------
    >>> pyprithvi.terminate_job(job_id='123456')
    """
    api_path = "job/terminate-job"
    params = {'job_id': job_id}
    response = post_request(api_path, params=params)
    if response:
        response = response.json()
        if response["terminated"]:
            print("Job successfully terminated")
        elif not response["terminated"]:
            print("Job termination failed")
    return None


def get_job_log(job_id: str) -> None:
    """Get AWS Batch Job.

    Parameters
    ----------
    job_id: str
      Job id associated with the job

    Example
    -------
    >>> pyprithvi.get_job_log(job_id='123456')
    """
    api_path = "job/get-job-log"
    params = {'job_id': job_id}
    response = post_request(api_path, params=params)
    if response:
        response = response.json()
        print(response['log'])
        return response['log']
    return None
