import json
import psycopg2

from urllib.error import HTTPError

import vulners as vulners


class LoadFromVulners:

    def __init__(self):
        self.key = "1FP2EXX7Q262T5M823WTVBRB82TPLZ6ND9AE2DJ2D2FPIRILW4IZHJKM3ZRY5SHT"

    def load(self):
        try:
            vulners_api = vulners.Vulners(api_key=self.key)
            nesus = vulners_api.archive("nessus")  # we get list of dictionaries.
            return nesus
        except HTTPError as e:
            print('problem with site loading: ', e.code)
