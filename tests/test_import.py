import aadrkit

def test_package_imports():
    """The package installs and exposes a version number."""
    assert aadrkit.__version__ == "0.1.0"