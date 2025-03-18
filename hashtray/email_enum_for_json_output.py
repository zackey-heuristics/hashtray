import itertools
import sys

import httpx

from hashtray.gravatar import Gravatar
from hashtray.email_enum import EmailEnum


class EmailEnumForJson(EmailEnum):
    def __init__(self, target: str, domain_list: str = "full"):
        super().__init__(target, domain_list=domain_list)

    def create_elements(self) -> list:
        # Get Gravatar info with account or with account hash
        if self.check_mailhash(self.account_hash):
            self.g = Gravatar(ghash=self.account_hash)
        else:
            self.g = Gravatar(account=self.account_hash)

        self.is_exists = self.g.is_exists()
        if not self.is_exists:
            # print(f"Account {self.account_hash} not found on Gravatar.com", file=sys.stderr)
            # don't exit in case of removed gravatar profile
            self.hashed = self.account_hash
        else:
            # Get elements with custom arguments or from the Gravatar profile
            self.hashed = self.g.info().get("hash", self.account_hash)

        if self.elements:
            elements = self.get_custom_elements()
        else:
            if not self.is_exists:
                elements = []
            else:
                elements = self.get_elements_from_gravatar()
        return elements
    
    def combinator(self) -> str:
        elements = self.dedup_chunks(self.create_elements())
        self.n_combs = self.get_combination_count(len(elements))
        # Generate all permutations/combinations of elements
        # Per chunk
        for r in range(1, len(elements) + 1):
            # Per chunk permutation
            for permutation in itertools.permutations(elements, r):
                # Per domain
                for domain in self.domains:
                    # No need of separator for single chunks
                    if len(permutation) == 1:
                        email_local_part = permutation[0]
                        yield f"{email_local_part}@{domain}"
                    else:
                        # Crazy mode: per separator, any kind of separator in each combination at any place
                        if self.crazy:
                            for separators in itertools.product(
                                self.separators, repeat=r - 1
                            ):
                                email_local_part = "".join(
                                    f"{e}{s}"
                                    for e, s in itertools.zip_longest(
                                        permutation, separators, fillvalue=""
                                    )
                                )
                                yield f"{email_local_part}@{domain}"
                        else:
                            # Normal mode: per separator, unique separator in each combination at any place
                            for separator in self.separators:
                                email_local_part = separator.join(permutation)
                                yield f"{email_local_part}@{domain}"
    
    def hashes(self) -> str:
        for email in self.combinator():
            hashd = self.hash_email(email)
            # Return if found
            if self.hashed == hashd:
                return email
    
    def get_json(self) -> dict:
        result = self.hashes()
        try:
            res = httpx.get(self.g.account_url + ".json")
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
    