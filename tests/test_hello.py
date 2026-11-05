from clean_python.domain.entities.hello import hello


def test_hello():
    assert hello() == "hello!"
