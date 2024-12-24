# htmst

![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/htmst)
[![PyPI - Version](https://img.shields.io/pypi/v/htmst)](https://pypi.org/project/htmst)
![GitHub](https://img.shields.io/github/license/picomet/htmst)

htmst is a python library for parsing html into AST with positions.

## Installation

```bash
uv add htmst
```

or

```bash
pip install htmst
```

## Usage

```python
from htmst import HtmlAst

html = """<span foo="bar">hi</span>"""
ast = HtmlAst(html)

print(ast.root.children[0].tag) # span

print(ast.root.children[0].start.row) # 0
print(ast.root.children[0].start.col) # 0

print(ast.root.children[0].end.row) # 0
print(ast.root.children[0].end.col) # 25

print(ast.root.children[0].attrs[0].name) # foo
print(ast.root.children[0].attrs[0].value) # bar

print(ast.root.children[0].attrs[0].start.row) # 0
print(ast.root.children[0].attrs[0].start.col) # 6

print(ast.root.children[0].attrs[0].end.row) # 0
print(ast.root.children[0].attrs[0].end.col) # 15
```

### Nodes

-   `DoubleTagNode`: represents double tags
-   `SingleTagNode`: represents single tags
-   `AttrNode`: represents attributes
-   `TextNode`: represents texts
-   `CommentNode`: represents comments
-   `DoctypeNode`: represents doctypes

Each node has a `start` and `end` position.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the [MIT License](LICENSE).
