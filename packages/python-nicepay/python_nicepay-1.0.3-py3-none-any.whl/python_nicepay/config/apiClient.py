import requests
import urllib.parse
import webbrowser


class apiClient:

    @staticmethod
    def send(host, header, request, endpoint):
        response = requests.post(url=host + endpoint, headers=header, json=request)
        return response.json()

    @staticmethod
    def sendDelete(host, header, request, endpoint):
        response = requests.delete(url=host + endpoint, headers=header, json=request)
        return response.json()

    @staticmethod
    def get(host, request, endpoint):
        data = urllib.parse.urlencode(request)
        webbrowser.open(f"{host}{endpoint}?{data}")

    @staticmethod
    def sendUrl(host, request, endpoint):
        response = requests.post(url=host + endpoint, data=request)
        return response.json()

    @staticmethod
    def redirect(host, tXid, endpoint):
        url = f"{host}{endpoint}?tXid={tXid}"
        webbrowser.open(url)
        return url


