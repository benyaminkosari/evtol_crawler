import requests as req

class Request:
    def __init__(self, url):
        self.url = url
        self.headers = self.get_headers()

    def send_request(self):
        print("sending request to (", self.url, ") ...")
        res = req.get(self.url, self.headers)
        return res

    @staticmethod
    def get_headers():
        headers = dict()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
        return headers
