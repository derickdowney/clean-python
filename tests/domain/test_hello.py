from clean_python.domain.hello import hello


def test_hello():
    assert hello() == "hello!"
