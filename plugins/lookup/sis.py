import re
from typing import Iterable

import requests
from ansible.errors import AnsibleLookupError, AnsibleOptionsError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

DOCUMENTATION = r"""
name: sis
author: Petr Borňás <p@brns.cz>
description:
  - Get information about subjects taught at Charles University.
options:
  _terms:
    description: subject codes
    required: True
    type: string
"""

EXAMPLES = r"""
- name: Inspect NSWI126
  debug: msg="{{ lookup('sis', 'NSWI126') }}"
"""

RETURN = r"""
_list:
  description:
    - information published about the subjects
  type: list
  elements: dict
"""

display = Display()


class Subject:
    title_regex = re.compile(r"(.*) - [A-Z0-9]+")
    title_selector = "#content .form_div_title"
    detail_selector = "#content .tab2 tr"
    parser = "html.parser"
    url = "https://is.cuni.cz/studium/predmety/index.php"

    def __init__(self, code: str):
        self.code = code
        self.load()

    def get_title(self) -> str:
        if title := self.soup.css.select_one(self.title_selector):
            if match := self.title_regex.match(title.get_text()):
                return match.group(1)

        raise ValueError("Could not extract subject title")

    def get_details(self) -> Iterable[tuple[str, str]]:
        for row in self.soup.css.iselect(self.detail_selector):
            if key := row.find("th").get_text():
                value = row.find("td").get_text(", ", strip=True)
                yield key.rstrip(":").lower(), value

    def to_dict(self) -> dict[str, str]:
        ret = {key: value for key, value in self.get_details()}
        ret["název"] = self.get_title()
        ret["kód"] = self.code

        return ret

    def load(self):
        try:
            r = requests.get(
                self.url,
                {
                    "do": "predmet",
                    "kod": self.code,
                },
            )
        except RequestException as e:
            raise AnsibleLookupError("Failed to retrieve data", orig_exc=e)

        if r.status_code == 404:
            raise AnsibleOptionsError("Subject not found")
        elif not r.ok:
            raise AnsibleLookupError(
                f"Server responded with HTTP status code {r.status_code}"
            )

        display.debug("Successfully requested web page '{}'".format(r.url))
        self.soup = BeautifulSoup(r.content, self.parser)


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        return [Subject(term).to_dict() for term in terms]
