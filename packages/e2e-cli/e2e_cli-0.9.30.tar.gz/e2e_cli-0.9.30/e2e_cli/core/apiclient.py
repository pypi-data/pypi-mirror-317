import requests
from colorama import Fore, init as init_colorama
from e2e_cli.core.constants import BASE_URL

init_colorama(autoreset=True)

class ApiClient:
    def __init__(self, api_key, auth_token, project_id, location):
        self.api_key = api_key
        self.auth_token = f"Bearer {auth_token}"
        self.project_id = project_id
        self.location = location
    
    def _get_headers(self):
        return {
            'Authorization': self.auth_token,
            'Content-Type': 'application/json',
            'User-Agent' : 'cli-e2e',
        }
    
    def _get_default_query_params(self):
        return {
            "apikey": self.api_key,
            "location": self.location,
            "project_id": self.project_id,
        }
    
    def get_response(self, url, method, payload=None, query_params={}):
        api_endpoint = f"{BASE_URL}{url}"
        headers = self._get_headers()
        query_params.update(self._get_default_query_params())
        try:
            response = requests.request(method=method, url=api_endpoint, headers=headers,
                                        params=query_params, json=payload)
            return response.json()
        except Exception as e:
            print(f"{Fore.RED}There is some exception occured. Kindly try after some time.")
            return None