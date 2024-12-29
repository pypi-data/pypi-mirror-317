from requests import Response
from craws.utils import make_ua

from craws import Request, SelectorResponse


class AirSpider:
    def process_request(self, request: Request):
        """默认给请求头加上UA字段"""
        request.headers = request.headers or {}
        request.headers.setdefault("User-Agent", make_ua())

    def process_response(self, response: Response):
        """默认返回选择器响应，自带Xpath、CSS"""
        return SelectorResponse(response)

    def get(self, url: str, headers: dict = None, params: dict = None, proxies: dict = None, timeout=5, **kwargs):
        req = Request(url, method="GET", headers=headers, params=params, proxies=proxies, timeout=timeout, **kwargs)
        return self.perform(req)

    def post(self, url: str, headers: dict = None, params: dict = None, data: dict | str = None, json: dict = None, proxies: dict = None, timeout=5, **kwargs):
        req = Request(url, method="POST", headers=headers, params=params, data=data, json=json, proxies=proxies, timeout=timeout, **kwargs)
        return self.perform(req)

    def perform(self, request: Request):
        """处理请求，返回响应"""
        self.process_request(request)
        response = request.do()
        response = self.process_response(response)
        request.__dict__.update(response.request.__dict__)
        response.request = request
        return response
