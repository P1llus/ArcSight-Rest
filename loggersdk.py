#!/usr/bin/env python

"""Unofficial Python SDK for Arcsight Logger."""

import json
import time
import requests


def post(host, url, data, verify=False, disable_warning=True):
    """Request implementation, to simplify error handling.

    Args:
        host (string): Hostname of Logger
        url (string): URL for the API Endpoint
        data (array): Payload of the body
        verify (bool, optional): SSL Verification
        disable_warning (bool, optional): Disable SSL warnings

    Returns:
        json: An array upon success, or empty if HTTP 204.
        If an error is caught the error will be printed
        and the application will exit.

    """
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    if disable_warning:
        requests.packages.urllib3.disable_warnings()
    try:
        response = requests.post(
            'https://' + host + url, json=data, headers=headers, verify=verify)
        response.raise_for_status()
        if response.status_code == 200:
            if response.text:
                response = json.loads(response.text)
        else:
            response = response.text
    except requests.exceptions.HTTPError as err:
        print(response.text)
        print(err)
        exit(1)
    return response


def login(host, username, password):
    """Authenticate with the ArcSight Logger.

    Args:
        host (string): Hostname of Logger
        username (string): Username to authenticate with
        password (string): Password related to the user account

    Returns:
        json: On successful login it will return the related authtoken

    """
    url = '/core-service/rest/LoginService/login'
    payload = {
        "log.login": {
            "log.login": username,
            "log.password": password
        }
    }
    response = post(host, url, data=payload)
    return response


def logout(host, authtoken):
    """Close the provided authtoken.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session

    Returns:
        Null: Returns an empty HTTP 204 upon success

    """
    url = '/core-service/rest/LoginService/logout'
    payload = {
        "log.logout": {
            "log.authToken": authtoken,
        }
    }
    response = post(host, url, data=payload)
    return response


def search(host, authtoken, query, search_id, **kwargs):
    """Start a background search job.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session
        query (string): Which query to run
        search_id (int): The search_id to be generated for the search
        **kwargs: All arguments marked as optional in documentation

    Returns:
        json: If successful returns a sessionId, this ID is only
        related if you want to find the running search
        on the ArcSight Logger web interface. This is not related
        to the search_id provided by the user.

    """
    url = '/server/search'
    payload = {
        'search_session_id': search_id,
        'user_session_id': authtoken,
        'query': query,
        **kwargs
    }
    response = post(host, url, data=payload)
    return response


def status(host, authtoken, search_id):
    """Retrieve status of an existing search.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session
        search_id (int): The search_id for the search to take action on

    Returns:
        json: An array showing the current status of a search

    """
    url = '/server/search/status'
    payload = {
        'search_session_id': search_id,
        'user_session_id': authtoken,
    }
    response = post(host, url, data=payload)
    return response


def wait(host, authtoken, search_id):
    """Wait until a search is finalized, checking every 5 seconds.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session
        search_id (int): The search_id for the search to take action on

    Returns:
        json: An array showing the current status of a search

    """
    response = status(host, authtoken, search_id)
    while response['status'] != 'complete' and response['status'] != "error":
        response = status(host, authtoken, search_id)
        if response['status'] != 'complete' and response['status'] != "error":
            time.sleep(5.0)
    return response


def events(host, authtoken, search_id, **kwargs):
    """Retrieve events related to a running or finalized search.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session
        search_id (int): The search_id for the search to take action on
        **kwargs: All arguments marked as optional in documentation

    Returns:
        json: Array including the events for the related search_id

    """
    url = '/server/search/events'
    payload = {
        'search_session_id': search_id,
        'user_session_id': authtoken,
        **kwargs
    }
    response = post(host, url, data=payload)
    return response


def raw_events(host, authtoken, search_id, row_ids):
    """Retrieve the raw CEF formatted events from search_id.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session
        search_id (int): The search_id for the search to take action on
        row_ids (array): An array of IDs which raw events should be retrieved from

    Returns:
        json: An array of CEF formatted raw events related to the row_ids

    """
    url = '/server/search/raw_events'
    payload = {
        'search_session_id': search_id,
        'user_session_id': authtoken,
        'row_ids': [row_ids]
    }
    response = post(host, url, data=payload)
    return response


def histogram(host, authtoken, search_id):
    """Retrieve data from a related search_id in a histogram format.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session
        search_id (int): The search_id for the search to take action on

    Returns:
        json: An array with bucket counts, width
        and the relevant count for each bucket

    """
    url = '/server/search/histogram'
    payload = {
        'search_session_id': search_id,
        'user_session_id': authtoken,
    }
    response = post(host, url, data=payload)
    return response


def drilldown(host, authtoken, search_id, start_time, end_time):
    """Drill down a finalized search, to retrieve events from a smaller time.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session
        search_id (int): The search_id for the search to take action on
        start_time (string): The starttime for the drilldown
        end_time (string): The endtime for the drilldown

    Returns:
        Null: Returns an empty HTTP 204 response upon success

    """
    url = '/server/search/drilldown'
    payload = {
        'search_session_id': search_id,
        'user_session_id': authtoken,
        'start_time': start_time,
        'end_time': end_time,
    }
    response = post(host, url, data=payload)
    return response


def chart_data(host, authtoken, search_id, **kwargs):
    """Return results to be used in charts or statistics.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session
        search_id (int): The search_id for the search to take action on
        **kwargs: All arguments marked as optional in documentation

    Returns:
        json: An array of aggregated data based on the specific search_id

    """
    url = '/server/search/chart_data'
    payload = {
        'search_session_id': search_id,
        'user_session_id': authtoken,
        **kwargs
    }
    response = post(host, url, data=payload)
    return response


def stop(host, authtoken, search_id):
    """Halts an ongoing search while keeping the currently found results.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session
        search_id (int): The search_id for the search to take action on

    Returns:
        null: An empty HTTP 204 response upon success

    """
    url = '/server/search/stop'
    payload = {
        'search_session_id': search_id,
        'user_session_id': authtoken,
    }
    response = post(host, url, data=payload)
    return response


def close(host, authtoken, search_id):
    """Close down an ongoing or finished search, and delete it's current results.

    Args:
        host (string): Hostname of Logger
        authtoken (string): Token for the current session
        search_id (int): The search_id for the search to take action on

    Returns:
        null: An empty HTTP 204 response upon success

    """
    url = '/server/search/close'
    payload = {
        'search_session_id': search_id,
        'user_session_id': authtoken,
    }
    response = post(host, url, data=payload)
    return response
