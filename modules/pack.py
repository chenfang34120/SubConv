"""
This module is to general a complete config for Clash
"""


from modules import parse
import re
from . import config
import yaml
import random

from urllib.parse import urlparse, urlencode

async def pack(url: list, urlstandalone: list, urlstandby:list, urlstandbystandalone: list, content: str, interval: str, domain: str, short: str, notproxyrule: str, base_url: str):
    providerProxyNames = await parse.mkListProxyNames(content)
    result = {}

    if short is None:
        # head of config
        result.update(config.configInstance.HEAD)

    # proxies
    proxies = {
        "proxies": []
    }
    proxiesName = []
    proxiesStandbyName = []

    if urlstandalone or urlstandbystandalone:
        if urlstandalone:
            for i in urlstandalone:
                proxies["proxies"].append(
                    i
                )
                proxiesName.append(i["name"])
                proxiesStandbyName.append(i["name"])
        if urlstandbystandalone:
            for i in urlstandbystandalone:
                proxies["proxies"].append(
                    i
                )
                proxiesStandbyName.append(i["name"])
    if len(proxies["proxies"]) == 0:
        proxies = None
    if len(proxiesName) == 0:
        proxiesName = None
    if len(proxiesStandbyName) == 0:
        proxiesStandbyName = None
    if proxies:
        result.update(proxies)


    # proxy providers
    providers = {
        "proxy-providers": {}
    }
    if url or urlstandby:
        if url:
            for u in range(len(url)):
                providers["proxy-providers"].update({
                    "subscription{}".format(u): {
                        "type": "http",
                        "url": url[u],
                        "interval": int(interval),
                        "path": "./sub/subscription{}.yaml".format(u),
                        "health-check": {
                            "enable": True,
                            "interval": 60,
                            # "lazy": True,
                            "url": config.configInstance.TEST_URL
                        }
                    }
                })
        if urlstandby:
            for u in range(len(urlstandby)):
                providers["proxy-providers"].update({
                    "subscription{}".format("sub"+str(u)): {
                        "type": "http",
                        "url": urlstandby[u],
                        "interval": int(interval),
                        "path": "./sub/subscription{}.yaml".format("sub"+str(u)),
                        "health-check": {
                            "enable": True,
                            "interval": 60,
                            # "lazy": True,
                             "url": config.configInstance.TEST_URL
                        }
                    }
                })
    if len(providers["proxy-providers"]) == 0:
        providers = None
    if providers:
        result.update(providers)

    yaml.SafeDumper.ignore_aliases = lambda *args : True
    
    return yaml.safe_dump(result, allow_unicode=True, sort_keys=False)
