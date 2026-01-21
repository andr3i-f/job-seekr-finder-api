import requests

class BaseScraper:
    def __init__(self):
        self.url = ''
        self.source = 'BaseScraper'

    async def call(self):
        res = requests.get(self.url, params=self.build_params(), headers=self.build_header())

        if (res.status_code == 200):
            await self.parse_response(res)
        else:
            # TODO: Log this in a better method :P
            print(f"{self.source} | ERROR GETTING DATA | RESPONSE CODE: {res.status_code}")

    def build_params(self):
        pass

    def build_header(self):
        pass

    def parse_response(self, res):
        pass