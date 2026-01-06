"""Basic import test for operations module."""


def test_operations_imports():
    """Test that the operations module can be imported successfully."""
    import file_sanitizer.core.operations as ops

    assert ops is not None
