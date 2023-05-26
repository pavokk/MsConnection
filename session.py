from urllib.parse import urljoin
import requests
import exceptions


class Requestor:
    def __init__(self, session: requests.Session, store: str):
        self.session = session
        self.base_url = f"https://api.mystore.no/shops/{store}/"

    def _request(self, method: str, path: str, vnd: bool = True, data: str | None = None):

        if not vnd:
            self.session.headers['Accept'] = 'application/json'

        url = urljoin(self.base_url, path) if path[0] != "h" else path

        try:
            response = self.session.request(
                method,
                url,
                headers=self.session.headers,
                data=data,
            )

        except requests.RequestException as e:
            raise exceptions.ApiError(e)
        if not response.ok:
            raise exceptions.ResponseError(response)

        return response

    def get(self, path: str, vnd: bool = True):
        return self._request('GET', path, vnd=vnd)

    def post(self, path: str, data: str, vnd: bool = True):
        return self._request('POST', path, vnd=vnd, data=data)

    def patch(self, path: str, data: str, vnd: bool = True):
        return self._request('PATCH', path, vnd=vnd, data=data)

    def delete(self, path: str, vnd: bool = True):
        return self._request('DELETE', path, vnd=vnd)

    def get_paginated(self, endpoint: str):
        next_page: str | int = endpoint
        output = list()

        while type(next_page) == str:  # If theres no next page in the response we set next_page to int 0
            response = self.get(next_page).json()

            for data in response["data"]:
                output.append(data)

            if "next" in response["links"]:
                next_page = response["links"]["next"]
            else:
                next_page = 0

        return output


class TokenSession(requests.Session):
    def __init__(self, token: str, agent: str):
        super().__init__()
        self.headers['User-Agent'] = agent
        self.headers['Content-Type'] = 'application/vnd.api+json'
        self.headers['Accept'] = 'application/vnd.api+json'
        self.headers['Authorization'] = f"Bearer {token}"
