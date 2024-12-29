#    ____   # -------------------------------------------------- #
#   | ^  |  # SimpleHttpClient for AUMC                          #
#   \  --   # o.m.vandermeer@amsterdamumc.nl                     #
# \_| ﬤ| ﬤ  # If you like this code, treat him to a coffee! ;)   #
#   |_)_)   # -------------------------------------------------- #

# SimpleHttpClient is needed to make HTTP requests to an API endpoint

from xml.dom.minidom import parseString
import requests


class SimpleHttpClient:
    def __init__(self, base_url=None, headers=None):
        self.base_url = base_url
        self.headers = headers if headers is not None else {}
        self.dino = "Mrauw!"

    def set_header(self, key, value):
        self.headers[key] = value

    def get(self, endpoint, params=None, extra_headers={}):
        url = self._build_url(endpoint)
        headers = {**self.headers, **extra_headers}
        response = requests.get(url, headers=headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json=None, extra_headers={}):
        url = self._build_url(endpoint)
        headers = {**self.headers, **extra_headers}
        response = requests.post(url, headers=headers, data=data, json=json)
        return self._handle_response(response)

    def put(self, endpoint, data=None, json=None, extra_headers={}):
        url = self._build_url(endpoint)
        headers = {**self.headers, **extra_headers}
        response = requests.put(url, headers=headers, data=data, json=json)
        return self._handle_response(response)

    def delete(self, endpoint, extra_headers={}):
        url = self._build_url(endpoint)
        headers = {**self.headers, **extra_headers}
        response = requests.delete(url, headers=headers)
        return self._handle_response(response)

    def patch(self, endpoint, data=None, json=None, extra_headers={}):
        url = self._build_url(endpoint)
        headers = {**self.headers, **extra_headers}
        response = requests.patch(url, headers=headers, data=data, json=json)
        return self._handle_response(response)

    def _build_url(self, endpoint):
        if self.base_url:
            return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return endpoint

    def _handle_response(self, response):
        try:
            response.raise_for_status()  # Raise an HTTPError on bad responses (4xx and 5xx)
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            print("Response Text:", response.text)
            return None
        content_type = response.headers.get("Content-Type", "")
        if "application/xml" in content_type or "text/xml" in content_type:
            return self._pretty_print_xml(response.text)
        try:
            return response.json()  # Try to return JSON if possible
        except ValueError:
            return response.text  # Fallback to text if no JSON

    def _pretty_print_xml(self, xml_str):
        dom = parseString(xml_str)
        return dom.toprettyxml()
