# shared/api_client.py

from typing import Optional, Dict, Any
import requests
import logging
import http.client as http_client
import certifi

# Enable verbose logging for SSL connections
http_client.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class APIClient:

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Token {self.api_key}',
        }

    ## CLASSICAL JSON API'S 
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self._build_url(endpoint)
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self._build_url(endpoint)
        response = requests.post(url, headers=self.headers, json=data, params=params)
        return self._handle_response(response)

    def put(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self._build_url(endpoint)
        response = requests.put(url, headers=self.headers, json=data, params=params)
        return self._handle_response(response)

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self._build_url(endpoint)
        response = requests.delete(url, headers=self.headers, params=params)
        return self._handle_response(response)
    
    ## AUDIO 
    def postAudio(self, endpoint: str, audioData: bytes, params: Optional[Dict[str, Any]] = None, ) -> Dict[str, Any]:
        url = self._build_url(endpoint)
        headers = self.headers.copy()
        headers["Content-Type"] = "audio/*"
        response = requests.post(url, headers=headers, data=audioData, params=params, verify=certifi.where())
        return self._handle_response(response)

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint}"

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code == 200:
            json_response = response.json()
            # Extract the "results" object
            if "results" in json_response:
                return json_response["results"]
            else:
                raise KeyError("The 'results' key was not found in the response.")
        else:
            response.raise_for_status()


