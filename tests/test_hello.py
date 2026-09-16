from codescape.parse.hello import hello


def test_hello() -> None:
    assert hello("world") == "Hello, world!"
