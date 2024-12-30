from htmst import HtmlAst
from htmst.structures import (
    CommentNode,
    DoctypeNode,
    DoubleTagNode,
    Pos,
    SingleTagNode,
    TextNode,
)


def test_text():
    html = """hi"""
    ast = HtmlAst(html)
    node = ast.root.children[0]
    assert isinstance(node, TextNode)
    assert node.text == "hi"


def test_double():
    html = """<div>hi</div>"""
    ast = HtmlAst(html)
    node = ast.root.children[0]
    assert isinstance(node, DoubleTagNode)
    assert node.tag == "div"
    assert hasattr(node, "children")
    assert node.start == Pos(0, 0)
    assert node.end == Pos(0, len(html))


def test_single():
    html = """<input type="text" />"""
    ast = HtmlAst(html)
    node = ast.root.children[0]
    assert isinstance(node, SingleTagNode)
    assert node.tag == "input"
    assert not hasattr(node, "children")
    assert node.start == Pos(0, 0)
    assert node.end == Pos(0, len(html))


def test_attrs():
    html = """<div class="foo" id="bar" @click="alert()">hi</div>"""
    ast = HtmlAst(html)
    node = ast.root.children[0]
    assert isinstance(node, DoubleTagNode)
    assert node.tag == "div"
    assert node.attrs[0].name == "class"
    assert node.attrs[0].value == "foo"
    assert node.attrs[1].name == "id"
    assert node.attrs[1].value == "bar"
    assert node.attrs[2].name == "@click"
    assert node.attrs[2].value == "alert()"
    assert node.start == Pos(0, 0)
    assert node.end == Pos(0, len(html))


def test_double_quote():
    html = """<div class="foo \\" bar">hi</div>"""
    ast = HtmlAst(html)
    node = ast.root.children[0]
    assert isinstance(node, DoubleTagNode)
    assert node.tag == "div"
    assert node.attrs[0].value == 'foo \\" bar'
    assert node.start == Pos(0, 0)
    assert node.end == Pos(0, len(html))


def test_single_quote():
    html = """<div class='foo \\' bar'>hi</div>"""
    ast = HtmlAst(html)
    node = ast.root.children[0]
    assert isinstance(node, DoubleTagNode)
    assert node.tag == "div"
    assert node.attrs[0].value == "foo \\' bar"
    assert node.start == Pos(0, 0)
    assert node.end == Pos(0, len(html))


def test_comment():
    html = """<!-- comment -->"""
    ast = HtmlAst(html)
    node = ast.root.children[0]
    assert isinstance(node, CommentNode)
    assert node.text == " comment "
    assert node.start == Pos(0, 0)
    assert node.end == Pos(0, len(html))


def test_doctype():
    html = """<!DOCTYPE html>"""
    ast = HtmlAst(html)
    node = ast.root.children[0]
    assert isinstance(node, DoctypeNode)
    assert node.text == "html"
    assert node.start == Pos(0, 0)
    assert node.end == Pos(0, len(html))


class TestSource:
    def test_first_bracket(self):
        source = "foo(</script>)"
        html = f"""<script>{source}</script>"""
        ast = HtmlAst(html)
        node = ast.root.children[0]
        assert isinstance(node, DoubleTagNode)
        assert node.tag == "script"
        assert node.start == Pos(0, 0)
        assert node.end == Pos(0, len(html))
        assert node.children[0].text == source

    def test_second_bracket(self):
        source = "function foo(){ </script>; }"
        html = f"""<script>{source}</script>"""
        ast = HtmlAst(html)
        node = ast.root.children[0]
        assert isinstance(node, DoubleTagNode)
        assert node.tag == "script"
        assert node.start == Pos(0, 0)
        assert node.end == Pos(0, len(html))
        assert node.children[0].text == source

    def test_third_bracket(self):
        source = "function foo(){ bar[</script>]; }"
        html = f"""<script>{source}</script>"""
        ast = HtmlAst(html)
        node = ast.root.children[0]
        assert isinstance(node, DoubleTagNode)
        assert node.tag == "script"
        assert node.start == Pos(0, 0)
        assert node.end == Pos(0, len(html))
        assert node.children[0].text == source

    def test_signle_quote(self):
        source = "function foo(){ bar['</script>']; }"
        html = f"""<script>{source}</script>"""
        ast = HtmlAst(html)
        node = ast.root.children[0]
        assert isinstance(node, DoubleTagNode)
        assert node.tag == "script"
        assert node.start == Pos(0, 0)
        assert node.end == Pos(0, len(html))
        assert node.children[0].text == source

    def test_double_quote(self):
        source = 'function foo(){ bar["</script>"]; }'
        html = f"""<script>{source}</script>"""
        ast = HtmlAst(html)
        node = ast.root.children[0]
        assert isinstance(node, DoubleTagNode)
        assert node.tag == "script"
        assert node.start == Pos(0, 0)
        assert node.end == Pos(0, len(html))
        assert node.children[0].text == source


def test_lf():
    html = """<div>\n  hi\n</div>"""
    ast = HtmlAst(html)
    node = ast.root.children[0]
    assert isinstance(node, DoubleTagNode)
    assert node.tag == "div"
    assert node.start == Pos(0, 0)
    assert node.end == Pos(2, 6)


def test_crlf():
    html = """<div>\r\n  hi\r\n</div>"""
    ast = HtmlAst(html)
    node = ast.root.children[0]
    assert isinstance(node, DoubleTagNode)
    assert node.tag == "div"
    assert node.start == Pos(0, 0)
    assert node.end == Pos(2, 6)
