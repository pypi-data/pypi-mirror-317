import requests

class Util():
    def assign_enum_val(enum_class, value):
        try:
            return enum_class(value)
        except ValueError:
            return None
    
    def assign_enum_name(enum_class, name):
        try:
            return enum_class[name]
        except ValueError:
            return None

class RestAPIProxy:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None, headers=None):
        response = requests.get(f"{self.base_url}/{endpoint}", params=params, headers=headers)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json=None, headers=None):
        response = requests.post(f"{self.base_url}/{endpoint}", data=data, json=json, headers=headers)
        return self._handle_response(response)

    def put(self, endpoint, data=None, json=None, headers=None):
        response = requests.put(f"{self.base_url}/{endpoint}", data=data, json=json, headers=headers)
        return self._handle_response(response)

    def delete(self, endpoint, headers=None):
        response = requests.delete(f"{self.base_url}/{endpoint}", headers=headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()