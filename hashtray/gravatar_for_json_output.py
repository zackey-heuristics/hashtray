import hashlib
import re
import sys

import httpx

from hashtray.gravatar import Gravatar


class GravatarForJson(Gravatar):
    def __init__(self, email=None, ghash: str = None, account: str = None):
        super().__init__(email, ghash, account)
    
    def get_json(self) -> dict:
        try:
            res = httpx.get(self.account_url + ".json")
            res.raise_for_status() ## Raise an exception for non-200 status codes
            return res.json()
        except httpx.HTTPError as e:
            if e.response.status_code == 404:
                print("Profile not found (404 error)", file=sys.stderr)
            else:
                print("HTTP error occurred", file=sys.stderr)
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)

        return {}