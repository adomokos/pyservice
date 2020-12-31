from pyservice import __version__


def test_verifies_the_package_version() -> None:
    assert __version__ == "0.0.3"
