import requests
import json

class ApiRequest:

    def __init__(self, url, header, data="", json_flag=True):
        self.url = url
        self.header = header
        if json_flag:
            self.data = json.dumps(data)
        else:
            self.data = data

    def get(self):
        return requests.get(self.url, headers=self.header, data="")
    
    def post(self):
        return requests.post(self.url, headers=self.header, data=self.data)
    