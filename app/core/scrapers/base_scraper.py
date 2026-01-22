import requests
from app.core.config import logger


class BaseScraper:
    def __init__(self):
        self.url = ""
        self.source = "BaseScraper"

    async def call(self):
        res = requests.get(
            self.url, params=self.build_params(), headers=self.build_header()
        )

        if res.status_code == 200:
            await self.parse_response(res)
        else:
            self.log_error(f"Error getting data - response code: {res.status_code}")

    def build_params(self):
        pass

    def build_header(self):
        pass

    def parse_response(self, res):
        pass

    def log_info(self, msg):
        logger.info(f"[{self.source}] {msg}")

    def log_error(self, msg):
        logger.error(f"[{self.source}] {msg}")
