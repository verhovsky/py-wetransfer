#!/usr/bin/python
#
# Get the actual URL of WeTransfer files
#
# VERSION   : v1.2
# DATE      : 30th September 2021
# AUTHORS   : Alejandro Alonso
#           : Marcos Besteiro López
#           : Gary Watson <https://github.com/GaryWatsonUK>
#           : Boris Verkhovskiy <https://github.com/verhovsky>
# URL       : https://github.com/GaryWatsonUK/py-wetransfer
# DEPENDS   : pip install requests json5 beautifulsoup

import argparse
import sys

import requests
from bs4 import BeautifulSoup
import json5

from urllib.parse import urlparse

USAGE = "python wetransfer.py https://we.tl/XXXXXXXXXXXX"
DESC = """
You should have a We transfer address similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY or https://we.tl/XXXXXXXXXXXX
""".strip()

parser = argparse.ArgumentParser(
    usage=USAGE, description="download WeTransfer files", epilog=DESC
)
parser.add_argument("url", help="the url to download")
url = parser.parse_args().url

# Expand shortened we.tl URLs
redirect = requests.get(url, allow_redirects=False)
if not redirect.text and redirect.headers["location"]:
    url = redirect.headers["location"]

# TODO: alegedly, the URL might also look like this
# https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY/ZZZZZZZZ
# _, file_id, _, security_hash = urlparse(url).path.strip('/').split('/')
_, file_id, security_hash = urlparse(url).path.strip("/").split("/")

request_data = requests.get(url)
soup = BeautifulSoup(request_data.text, "html.parser")
for script_tag in soup.select('script[type="text/javascript"]'):
    if "__launch_darkly" in script_tag.string and "feature_flags" in script_tag.string:
        js_src = script_tag.string.strip()
        var_start = js_src.find("__launch_darkly")
        var_src_junk = js_src[var_start:]
        var_end = var_src_junk.find(";")
        var_src = var_src_junk[:var_end]
        obj_src = var_src[var_src.find("{"):].strip().strip(";")
        obj = json5.loads(obj_src)
        domain_user_id = obj["user"]["key"]
        break
else:
    raise ValueError("couldn't find __launch_darkly variable")

meta_tags = soup.select('meta[name="csrf-token"]')
if not meta_tags:
    raise ValueError('couldn\'t find any meta[name="csrf-token"]')
csrf_token = meta_tags[0]["content"]

# Call the API in order to retrieve the direct link
headers = {
    "authority": "msi.wetransfer.com",
    "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    "x-csrf-token": csrf_token,
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "accept": "application/json, text/plain, */*",
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua-platform": '"macOS"',
    "origin": "https://msi.wetransfer.com",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://msi.wetransfer.com/",
    "accept-language": "en-US,en;q=0.9",
}

data = {
    "security_hash": security_hash,
    "intent": "entire_transfer",
    "domain_user_id": domain_user_id,
}

result = requests.post(
    f"https://wetransfer.com/api/v4/transfers/{file_id}/download",
    headers=headers,
    json=data,
)
result.raise_for_status()
download_link = result.json()["direct_link"]

print(download_link)
