import os
import time
from urllib.parse import urljoin
import requests
import logging
import copy

from .MsExceptions import MsExceptions
# from .exceptions import ApiError, ResponseError


class Queue:
    """
    1. Add jobs to the system. First thought is to have these as tuples with necessary info
    2. Add some tracker that monitors amount of requests over time
    3. Make sure requests dont go above the rate limit

    note: AS long as you have less than 120 requests to send per minute you don't actually have to limit. You could
    send all over 10 seconds, but you will have to wait 50 seconds before sending anything new.

    """
    def __init__(self, rate: int = 120):
        self.rate = rate
        self.queue = []

    def add(
            self,
            endpoint: str,
            method: str,
            data: str, request_type: str = "request",
            additional_info: str | None = None
    ):
        request = (endpoint, method, data)
        if additional_info is not None:
            request += additional_info
        self.queue.append(request)

    def process(self):
        """
        Sends all requests.
        :return:
        """
        pass


class Requestor:
    def __init__(self, session: requests.Session, store: str):
        self.session = session
        self.base_url = f"https://api.mystore.no/shops/{store}/"

    def _get_headers(self, vnd: bool, content_type: str | None):
        session_headers = copy.copy(self.session.headers)
        if not vnd:
            session_headers["Accept"] = "application/json"
            session_headers["Content-Type"] = "application/json"
        if content_type is not None:
            session_headers["Content-Type"] = content_type
        return session_headers

    def _request(
            self,
            method: str,
            path: str,
            vnd: bool = True,
            data: str | None = None,
            content_type: str | None = None,
            files: dict | None = None
    ):

        url = urljoin(self.base_url, path) if not path.startswith("http") else path
        logging.debug(url)

        try:
            response = self.session.request(
                method,
                url,
                headers=self._get_headers(vnd, content_type),
                data=data,
                files=files
            )

        except requests.RequestException as e:
            raise MsExceptions.ApiError(e)
        if not response.ok:
            raise MsExceptions.ResponseError(response)

        return response

    def get(self, path: str, vnd: bool = True):
        return self._request('GET', path, vnd=vnd)

    def post(self, path: str, data: str | dict, vnd: bool = True):
        return self._request('POST', path, vnd=vnd, data=data)

    def patch(self, path: str, data: str | dict, vnd: bool = True):
        return self._request('PATCH', path, vnd=vnd, data=data)

    def delete(self, path: str, vnd: bool = True):
        return self._request('DELETE', path, vnd=vnd)

    def get_paginated(self, endpoint: str):
        next_page: str | int = endpoint
        output = list()

        while type(next_page) is str:  # If theres no next page in the response we set next_page to int 0
            response = self.get(next_page).json()
            for data in response["data"]:
                output.append(data)

            if "next" in response["links"]:
                next_page = response["links"]["next"]
            else:
                next_page = 0

            time.sleep(0.5)

        return output


class TokenSession(requests.Session):

    """
    A Requests session with some custom headers made specifically for the Client class in MsConnection.py
    Requires an API token from auth.mystore.no and User-Agent.
    """

    def __init__(self, token: str, agent: str):
        super().__init__()
        self.headers['User-Agent'] = agent
        self.headers['Content-Type'] = 'application/vnd.api+json'
        self.headers['Accept'] = 'application/vnd.api+json'
        self.headers['Authorization'] = f"Bearer {token}"
