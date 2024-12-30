import re
from copy import deepcopy

from htmst.structures import (
    AttrNode,
    CommentNode,
    DoctypeNode,
    DoubleTagNode,
    Pos,
    SingleTagNode,
    TextNode,
)

SOURCES: list[str] = ["script", "style"]

CLOSINGS: dict[str, tuple[str, str | None, list[str]]] = {
    "(": [")", None, ["(", "{", "[", '"', "'", "`"]],
    "{": ["}", None, ["(", "{", "[", '"', "'", "`"]],
    "[": ["]", None, ["(", "{", "[", '"', "'", "`"]],
    '"': ['"', "\\", []],
    "'": ["'", "\\", []],
    "`": ["`", "\\", []],
}

TAG_NAME = r"[a-zA-Z0-9.-]"
ATTR_NAME = r"[a-zA-Z0-9@:_.-]"


class HtmlAst:
    __slots__ = ("html", "root", "current_node", "current_index", "current_pos")

    def __init__(self, html: str):
        self.html: str = html
        self.root = DoubleTagNode("", [], None, Pos(0, 0), Pos(0, 0))
        self.current_node = self.root
        self.current_index = 0
        self.current_pos = Pos(0, 0)
        self.__parse()
        self.root.end = deepcopy(self.current_pos)

    def __parse(self):
        while self.current_index < len(self.html):
            char = self.html[self.current_index]
            if char == "<":
                if self.if_next([r"!", r"-", r"-"]):
                    self.handle_comment()
                elif self.if_next(
                    [r"!", r"(d|D)", r"(o|O)", r"(c|C)", r"(t|T)", r"(y|Y)"],
                ):
                    self.handle_doctype()
                elif self.if_finds(r"/"):
                    self.handle_tag_end()
                else:
                    self.handle_tag_start()
            else:
                self.handle_text()

    def if_next(self, chars: list[str]) -> bool:
        """
        Check if the next list of chars is the given chars.

        Args:
            chars (list[str]): the chars to check.

        Returns:
            True if the next list of chars is the given chars, False otherwise.
        """
        i = self.current_index + 1
        for char in chars:
            if i < len(self.html):
                if not re.match(char, self.html[i]):
                    return False
                i += 1
            else:
                return False
        return True

    def if_finds(self, char: str) -> bool:
        """
        Check if the next non-whitespace char is the given char.

        Args:
            char (str): the char to check.

        Returns:
            True if the next non-whitespace char is the given char, False otherwise.
        """
        i = self.current_index + 1
        while i < len(self.html):
            if re.match(r"(\s|\t|\n|\r)", self.html[i]):
                i += 1
                continue
            elif re.match(char, self.html[i]):
                return True
            return False
        return False

    def skip_char(self, num: int = 1) -> None:
        """
        Skip the next char(s) by incrementing the current index by given num,
        and incrementing the current position column by given num.

        Args:
            num (int, optional): the number of char(s) to skip. Defaults to 1.
        """
        self.current_index += num
        self.current_pos.col += num

    def skip_eol(self) -> None:
        """
        Skip the next end of line by incrementing the current index.
        And setting the postion to the start of the next line.
        """
        self.current_index += 1
        self.current_pos = Pos(self.current_pos.row + 1, 0)

    def skip_any(self) -> None:
        """
        Skip the next char or end of line.
        """
        char = self.html[self.current_index]
        if char == "\r":
            self.skip_char()
            self.skip_eol()
        elif char == "\n":
            self.skip_eol()
        else:
            self.skip_char()

    def skip_whitespaces(self) -> None:
        """
        Skip all whitespace characters.
        """
        while self.current_index < len(self.html):
            char = self.html[self.current_index]
            if re.match(r"(\s|\t|\r)", char):
                self.skip_char()
            elif char == "\n":
                self.skip_eol()
            else:
                break

    def match_char(self, regex: str) -> str | None:
        """
        Optionally match a char and skip it.

        Args:
            regex (str): the regex to match.

        Returns:
            str | None: the matched char or None if no match.
        """
        char = self.html[self.current_index]
        if re.match(regex, char):
            self.skip_any()
            return char
        return None

    def match_chars(self, regex: str) -> str | None:
        """
        Match and skip a sequence of chars one by one.

        Args:
            regex (str): the regex to match.

        Returns:
            str | None: the matched char(s) or None if no match.
        """
        string = ""
        while self.current_index < len(self.html):
            char = self.html[self.current_index]
            if re.match(regex, char):
                string += char
                self.skip_any()
            elif string:
                return string
            else:
                return None

    def handle_until(self, start: str) -> str:
        text = ""
        while self.current_index < len(self.html):
            char = self.html[self.current_index]
            if char in CLOSINGS[start][2]:
                text += char
                self.skip_any()
                text += self.handle_until(char)
                text += self.html[self.current_index]
                self.skip_char()
            elif re.match(f"[^{CLOSINGS[start][0]}]", char):
                text += char
                self.skip_any()
            else:
                escape = CLOSINGS[start][1]
                if escape and self.html[self.current_index - 1] == escape:
                    text += char
                    self.skip_any()
                    continue
                break
        return text

    def handle_text(self):
        start_pos = deepcopy(self.current_pos)
        text = ""
        while self.current_index < len(self.html):
            char = self.html[self.current_index]
            if self.current_node.tag in SOURCES:
                if char in CLOSINGS:
                    text += char
                    self.skip_char()

                    text += self.handle_until(char)

                    text += self.html[self.current_index]
                    self.skip_char()
                elif char == "<":
                    break
                else:
                    text += char
                    self.skip_any()
            elif char == "<":
                break
            else:
                text += char
                self.skip_any()

        node = TextNode(
            text,
            self.current_node,
            start_pos,
            deepcopy(self.current_pos),
        )
        self.current_node.children.append(node)

    def handle_tag_start(self):
        tag_start = deepcopy(self.current_pos)
        self.skip_char()  # <
        self.skip_whitespaces()
        tag = self.match_chars(TAG_NAME)  # tag
        self.skip_whitespaces()

        attrs: list[AttrNode] = []
        while self.current_index < len(self.html):
            attr_start = deepcopy(self.current_pos)
            name = self.match_chars(ATTR_NAME)
            if not name:
                break
            self.skip_whitespaces()
            equal = self.match_char("=")
            if equal:
                self.skip_whitespaces()
                quote_start = self.match_char(r"('|\")")
                if quote_start == "'":
                    value = self.handle_until("'")
                    self.skip_char()  # '
                elif quote_start == '"':
                    value = self.handle_until('"')
                    self.skip_char()  # "
                else:
                    break
            else:
                value = None

            attrs.append(
                AttrNode(
                    name,
                    value,
                    attr_start,
                    deepcopy(self.current_pos),
                )
            )
            self.skip_whitespaces()

        while self.current_index < len(self.html):
            char = self.html[self.current_index]
            if char == ">":
                self.skip_char()
                node = DoubleTagNode(
                    tag, attrs, self.current_node, tag_start, Pos(0, 0)
                )
                self.current_node.children.append(node)
                self.current_node = node
                break
            elif char == "/":
                self.skip_char()
                self.skip_whitespaces()
                while self.current_index < len(self.html):
                    char = self.html[self.current_index]
                    if char == ">":
                        self.skip_char()
                        node = SingleTagNode(
                            tag,
                            attrs,
                            self.current_node,
                            tag_start,
                            deepcopy(self.current_pos),
                        )
                        self.current_node.children.append(node)
                        return
                    else:
                        self.skip_any()
            else:
                self.skip_any()

    def handle_tag_end(self):
        self.skip_char()  # <
        self.skip_whitespaces()
        self.skip_char()  # /
        self.match_chars(TAG_NAME)  # tag
        self.skip_whitespaces()
        while self.current_index < len(self.html):
            char = self.html[self.current_index]
            if char == ">":
                self.skip_char()
                break
            self.skip_any()
        self.current_node.end = deepcopy(self.current_pos)
        self.current_node = self.current_node.parent

    def handle_comment(self):
        start = deepcopy(self.current_pos)
        self.skip_char(4)  # <!--

        text = ""
        while self.current_index < len(self.html):
            char = self.html[self.current_index]
            text += char
            self.skip_any()

            if text.endswith("-->"):
                text = text[:-3]
                break

        node = CommentNode(
            text,
            self.current_node,
            start,
            deepcopy(self.current_pos),
        )
        self.current_node.children.append(node)

    def handle_doctype(self):
        start = deepcopy(self.current_pos)
        self.skip_char(9)  # <!doctype | <!DOCTYPE
        self.skip_whitespaces()

        typ = self.match_chars(r"[a-zA-Z0-9]")
        self.skip_whitespaces()

        self.match_char(">")

        self.current_node.children.append(
            DoctypeNode(
                typ,
                self.current_node,
                start,
                deepcopy(self.current_pos),
            )
        )
