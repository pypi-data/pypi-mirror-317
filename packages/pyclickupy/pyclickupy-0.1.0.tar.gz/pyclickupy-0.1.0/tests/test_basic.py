from pyclickupy import hello

def test_import():
    """Test that the package can be imported."""
    import pyclickupy
    assert pyclickupy.__name__ == "pyclickupy"

def test_hello():
    """Test the hello function returns the expected greeting."""
    result = hello()
    assert isinstance(result, str)
    assert result == "Hello from pyclickupy!" 