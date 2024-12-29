import time

import requests
from loguru import logger

from craws.errs import RequestMethodError


class Request:
    """请求对象"""

    def __init__(self, url: str, method="GET", headers: dict = None, params: dict | str = None, data: dict = None, json: dict = None, proxies: dict = None, timeout=5, retry=2, rest=1, **kwargs):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.json = json
        self.proxies = proxies
        self.timeout = timeout

        self.retry = retry
        self.rest = rest

        self.kwargs = kwargs

    @staticmethod
    def elog(url: str, e: Exception, times: int):
        logger.error(
            """
            URL         {}
            ERROR       {}
            TIMES       {}
            """.format(url, e, times)
        )

    def sleep(self):
        time.sleep(self.rest)

    def do(self):
        if self.method not in ["GET", "POST"]:
            raise RequestMethodError("Method must be GET or POST")

        same = dict(headers=self.headers, params=self.params, proxies=self.proxies, timeout=self.timeout, **self.kwargs)
        for i in range(self.retry + 1):
            try:
                if self.method == "GET":
                    response = requests.get(self.url, **same)
                else:
                    response = requests.post(self.url, data=self.data, json=self.json, **same)
            except Exception as e:
                self.elog(self.url, e, i + 1)
                self.sleep()
                if i == self.retry:
                    raise e
            else:
                return response
