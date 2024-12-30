# ~/ClientFactory/src/clientfactory/clients/search/transformers.py
import urllib.parse, typing as t
from clientfactory.transformers.base import (
    Transform,
    TransformType,
    TransformOperation
)
from loguru import logger as log

class PayloadTransform(Transform):
    def __init__(self, key: str, valmap: dict, order: int = 0, nestkey: bool = False):
        super().__init__(
            type=TransformType.PAYLOAD,
            operation=TransformOperation.MERGE,
            target=key,
            order=order
        )
        self.key = key
        self.valmap = valmap
        self.nestkey = nestkey

    def apply(self, value: dict) -> dict:
        log.debug(f"PayloadTransform.apply | input: {value}")
        merged = self.valmap.copy()
        if self.key and self.nestkey:
            value = {self.key: value}
            log.debug(f"PayloadTransform.apply | nested key input: {value}")
        merged.update(value)
        result = {
            k:v for k,v in merged.items() if v is not None
        }
        log.debug(f"PayloadTransform.apply | output: {result}")
        return result


class URLTransform(Transform):
    def __init__(self, key:str, baseurl: str, order: int = 1):
        super().__init__(
            type=TransformType.URL,
            operation=TransformOperation.MAP,
            target=key,
            order=order
        )
        self.key = key
        self.baseurl = baseurl

    def apply(self, value: dict) -> dict:
        log.debug(f"URLTransform.apply | input: {value}")
        url = f"{self.baseurl}?{urllib.parse.urlencode(value)}"
        result = {"url": url}  # Return dict with URL instead of just URL
        log.debug(f"URLTransform.apply | output: {result}")
        return result


class ProxyTransform(Transform):
    """Transform for proxy-style APIs"""
    def __init__(
                self,
                apiurl: str,
                key: str = "proxy",
                valmap: dict = {"url": "url"},
                order: int = 2,
                **kwargs
            ):
        super().__init__(
            type=TransformType.PARAMS,
            operation=TransformOperation.MAP,
            target=key,
            order=order
        )
        self.apiurl = apiurl
        self.valmap = valmap
        self.kwargs = kwargs

    def apply(self, value: dict) -> dict:
        log.debug(f"ProxyTransform.apply | input: {value}")
        log.debug(f"ProxyTransform.apply | using apiurl: {self.apiurl}")
        log.debug(f"ProxyTransform.apply | using valmap: {self.valmap}")

        # Extract URL from previous transform
        url = value.get("url")
        if not url:
            raise ValueError("Missing URL from previous transform")

        # Create proxy params
        result = {
            outkey: url if inkey == "url" else self.kwargs.get(inkey)
            for outkey, inkey in self.valmap.items()
        }
        log.debug(f"ProxyTransform.apply | output: {result}")
        return result
