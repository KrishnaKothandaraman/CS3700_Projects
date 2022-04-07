from enum import Enum, auto
from html.parser import HTMLParser
from urllib.parse import urlparse
from typing import List, Tuple, Optional, Dict

AttributeResult = Tuple[str, Optional[str]]


class TargetType(Enum):
    """This class is an enumeration of various target types for the Parser. Passing a different target type will result
    in different Parser behavior"""
    CSRF_TOKEN_FINDER = auto()
    FLAG_FINDER = auto()
    LINK_FINDER = auto()


class Parser(HTMLParser):
    target_type: TargetType
    results = Dict
    save_next_data: bool

    def __init__(self, target_type: TargetType):
        super().__init__()
        self.target_type = target_type
        self.results = {}
        self.save_next_data = False

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, AttributeResult]]) -> None:
        """Called when a start tag is encountered by the parser"""

        if self.target_type == TargetType.CSRF_TOKEN_FINDER and tag == "input":
            attr_dict = dict(attrs)
            if "name" in attr_dict and attr_dict["name"] == "csrfmiddlewaretoken":
                self.results["csrfmiddlewaretoken"] = attr_dict["value"]
            if "name" in attr_dict and attr_dict["name"] == "next":
                self.results["next"] = attr_dict["value"]

        if self.target_type == TargetType.FLAG_FINDER and tag == "h3":
            attr_dict = dict(attrs)
            if "class" in attr_dict and attr_dict["class"] == "secret_flag":
                self.save_next_data = True

        if self.target_type == TargetType.LINK_FINDER and tag == "a":
            attr_dict = dict(attrs)
            if "href" not in attr_dict:
                return
            if "href" in self.results:
                self.results["href"].append(attr_dict["href"])
            else:
                self.results["href"] = [attr_dict["href"]]

    def handle_data(self, data: str) -> None:
        """Called when data is encountered by the parser"""

        if self.save_next_data:
            self.results["flag"] = data
            self.save_next_data = False

    def get_token(self) -> str:
        """Returns the CSRF in the HTML after processing"""
        if self.target_type != TargetType.CSRF_TOKEN_FINDER or "csrfmiddlewaretoken" not in self.results:
            return ""

        return self.results["csrfmiddlewaretoken"]

    def get_next(self) -> str:
        """Returns the next link in the HTML"""
        if self.target_type != TargetType.CSRF_TOKEN_FINDER or "next" not in self.results:
            return ""

        return self.results["next"]


if __name__ == "__main__":
    htmlparser = Parser(TargetType.FLAG_FINDER)
    login_html = open("login_html", mode='r')
    content = login_html.read()
    htmlparser.feed(content)
    print(f"Result is: {htmlparser.results}")
    login_html.close()
