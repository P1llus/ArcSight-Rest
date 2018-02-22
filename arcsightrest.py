#!/usr/bin/env python2

"""Test SDK for Arcsight Logger"""

import time
import warnings

import untangle
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning


class ArcsightLogger(object):
    """
    Main Class to interact with Arcsight Logger REST API
    """

    TARGET = 'https://TARGET:9000'

    def __init__(self, username, password, disable_insecure_warning=False):
        """
        Log in the user whose credentials are provided and
        store the access token to be used with all requests
        against Arcsight
        """

        action = 'ignore' if disable_insecure_warning else 'once'
        warnings.simplefilter(action, InsecureRequestWarning)
        r = self._post(
            '/core-service/rest/LoginService/login', data={
                'login': username,
                'password': password,
            }, is_json=False)
        r.raise_for_status()
        loginrequest = untangle.parse(r.text)
        self.token = loginrequest.ns3_loginResponse.ns3_return.cdata

    def _post(self, route, data, is_json=True,):
        """
        Post Call towards Arcsight Logger
        :param route: API endpoint to fetch
        :param is_json: Checks if post needs to be JSON
        :param data: Request Body
        :return: HTTP Response
        """

        if not data:
            return

        url = self.TARGET + route
        if is_json:
            return requests.post(url, json=data, verify=False)
        else:
            return requests.post(url, data, verify=False)

    def search(self, query, **kwargs):
        """
        Executes a searchquery, that is then stored and needs
        to be called again to get results, using the returned
        search_id.
        :param query: Query to be run with the search
        :return: Array of the current searchid, which is needed
                 for other functions, and the content of HTTP response.
        """
        search_id = int(round(time.time() * 1000))
        response = self._post(
            '/server/search', data=dict(
                    query=query,
                    search_session_id=search_id,
                    user_session_id=self.token,
                    **kwargs
            ))
        return search_id, response.json()

    def status(self, search_id):
        """
        Checks the current status of a search using the search_id
        :param search_id: The search_id that was generated
                          when a new search was called
        :return: status of the search as json
        """
        response = self._post(
            '/server/search/status', data=dict(
                search_session_id=search_id,
                user_session_id=self.token
                ))
        return response.json()

    def search_complete(self, search_id):
        """
        Checks the current status of a search using the search_id
        :param search_id: The search_id that was generated
                          when a new search was called
        :return: Whether or not the search finished already.
        """

        response = self._post(
            '/server/search/status', data=dict(
                search_session_id=search_id,
                user_session_id=self.token
            ))
        return response.json().get('status') == 'complete'

    def wait(self, search_id):
        """
        Blocks until the search represented by search_id completes
        :param search_id: The search_id that was generated
                          when a new search was called
        :return: The status of the search.
        """
        while not self.search_complete(search_id):
            time.sleep(5)
            print('still running')
        response = self._post(
            '/server/search/status', data=dict(
                search_session_id=search_id,
                user_session_id=self.token
            ))
        return response.json()

    def status(self, search_id):
        """
        Checks the current status of a search using the search_id
        :param search_id: The search_id that was generated
                        when a new search was called
        :return: Whether or not the search finished already.
        """

        response = self._post(
            '/server/search/status', data=dict(
                search_session_id=search_id,
                user_session_id=self.token
            ))
        return response.json()

    def events(self, search_id, custom_format=False, **kwargs):
        """
        Gathers events from a finished search
        :param search_id: The search_id that was generated
                          when a new search was called
        :param custom_format: Whether to return the response from
                              ArcSight unmodified or to pre-process it.
        :return: The events generated by a search.
        """

        response = self._post(
            '/server/search/events', data=dict(
                search_session_id=search_id,
                user_session_id=self.token,
                **kwargs
            ))
        events = response.json()
        if not events:
            return 'Search result was empty'
        if not custom_format:
            return events
        return [{
                    field['name']: result
                    for field, result in zip(events['fields'], results)
                    } for results in events['results']]

    def raw_events(self, search_id, row_ids):
        """
        Gathers events from a finished search
        :param search_id: The search_id that was generated
                          when a new search was called
        :return: The histogram generated by a search.
        """

        response = self._post(
            '/server/search/histogram', data=dict(
                search_session_id=search_id,
                user_session_id=self.token,
                row_ids=row_ids,
            ))
        return response.json()

    def histogram(self, search_id):
        """
        Gathers events from a finished search
        :param search_id: The search_id that was generated
                          when a new search was called
        :return: The histogram generated by a search.
        """

        response = self._post(
            '/server/search/histogram', data=dict(
                search_session_id=search_id,
                user_session_id=self.token
            ))
        return response.json()

    def drilldown(self, search_id, start_time, end_time):
        """
        Gathers events from a finished search
        :param search_id: The search_id that was generated
                          when a new search was called
        :return: The histogram generated by a search.
        """

        response = self._post(
            '/server/search/histogram', data=dict(
                search_session_id=search_id,
                user_session_id=self.token,
                start_time=start_time,
                end_time=end_time,
        ))
        return response.json()

    def chart_data(self, search_id, **kwargs):
        """
        Gathers events from a finished search
        :param search_id: The search_id that was generated
                          when a new search was called
        :return: The histogram generated by a search.
        """

        response = self._post(
            '/server/search/histogram', data=dict(
                search_session_id=search_id,
                user_session_id=self.token,
                **kwargs
        ))
        return response.json()

    def stop(self, search_id):
        """
        Stops the search operation but keeps the search
        session so that the search results can be narrowed
        down later.
        :param search_id: The search_id that was generated
                          when a new search was called
        :return: A message that the search has been stopped.
        """

        response = self._post(
            '/server/search/stop', data=dict(
                search_session_id=search_id,
                user_session_id=self.token
            ))
        return response

    def close(self, search_id):
        """
        Stops the execution of the search and clears
        the search session data from the server.
        :param search_id: The search_id that was generated
                          when a new search was called
        :return: A message that the search has been stopped.
        """
        response = self._post(
            '/server/search/close', data=dict(
                search_session_id=search_id,
                user_session_id=self.token
            ))
        return response
