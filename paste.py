import json
import requests


class PasteEEClient():
    def __init__(self, access_token):
        self.access_token = access_token

    def getLatestPasteContent(self):
        headers = {
            "X-Auth-Token": self.access_token
        }

        params = {
            "perpage": 1
        }

        try:
            return requests.get("https://api.paste.ee/v1/pastes/" + requests.get("https://api.paste.ee/v1/pastes", headers=headers, params=params).json()['data'][0]['id'], headers=headers).json()['paste']['sections'][0]['contents']
        except:
            return ""
