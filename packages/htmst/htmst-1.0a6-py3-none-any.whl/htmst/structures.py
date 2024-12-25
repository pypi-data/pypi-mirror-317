from copy import copy


class Pos:
    __slots__ = ("row", "col")

    def __init__(self, row: int, col: int):
        self.row: int = copy(row)
        self.col: int = copy(col)

    def to_json(self):
        return {"row": self.row, "col": self.col}

    def __eq__(self, other: "Pos"):
        return self.row == other.row and self.col == other.col

    def __str__(self) -> str:
        return f"[{self.row}:{self.col}]"

    def __repr__(self):
        return f"Pos({self.row}:{self.col})"


class TextNode:
    __slots__ = ("text", "parent", "start", "end")

    def __init__(self, text: str, parent: "DoubleTagNode", start: Pos, end: Pos):
        self.text: str = text
        self.start: Pos = start
        self.end: Pos = end
        self.parent: DoubleTagNode = parent

    def __repr__(self):
        return f"TextNode(...){self.start}-{self.end}"


class AttrNode:
    __slots__ = ("name", "value", "start", "end")

    def __init__(
        self,
        name: str,
        value: str | None,
        start: Pos,
        end: Pos,
    ):
        self.name: str = name
        self.value: str | None = value
        self.start: Pos = start
        self.end: Pos = end

    def __repr__(self):
        return f"AttrNode(@{self.name}){self.start}-{self.end}"


class DoubleTagNode:
    __slots__ = ("tag", "attrs", "children", "parent", "start", "end")

    def __init__(
        self,
        tag: str,
        attrs: list[AttrNode],
        parent: "DoubleTagNode | None",
        start: Pos,
        end: Pos,
    ):
        self.tag: str = tag
        self.attrs: list[AttrNode] = attrs
        self.children: list[
            DoubleTagNode | SingleTagNode | TextNode | CommentNode | DoctypeNode
        ] = []
        self.parent: DoubleTagNode | None = parent
        self.start: Pos = start
        self.end: Pos = end

    def __repr__(self):
        return f"DoubleNode(<{self.tag}>){self.start}-{self.end}"


class SingleTagNode:
    __slots__ = ("tag", "attrs", "parent", "start", "end")

    def __init__(
        self,
        tag: str,
        attrs: list[AttrNode],
        parent: DoubleTagNode,
        start: Pos,
        end: Pos,
    ):
        self.tag: str = tag
        self.attrs: list[AttrNode] = attrs
        self.parent: DoubleTagNode = parent
        self.start: Pos = start
        self.end: Pos = end

    def __repr__(self):
        return f"SingleNode(<{self.tag}/>){self.start}-{self.end}"


class CommentNode:
    def __init__(
        self,
        text: str,
        parent: DoubleTagNode,
        start: Pos,
        end: Pos,
    ):
        self.text: str = text
        self.parent: DoubleTagNode = parent
        self.start: Pos = start
        self.end: Pos = end

    def __repr__(self):
        return f"CommentNode(...){self.start}-{self.end}"


class DoctypeNode:
    def __init__(
        self,
        text: str,
        parent: DoubleTagNode,
        start: Pos,
        end: Pos,
    ):
        self.text: str = text
        self.parent: DoubleTagNode = parent
        self.start: Pos = start
        self.end: Pos = end

    def __repr__(self):
        return f"DoctypeNode({self.text}){self.start}-{self.end}"
