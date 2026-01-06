"""Tests for sanitize helpers."""

from file_sanitizer.core.sanitize import sanitize_name


def test_sanitize_basic():
    """Test basic file name sanitization."""
    assert sanitize_name("My File.txt") == "my-file.txt"
    assert sanitize_name("Résumé.md") == "resume.md"
    assert sanitize_name("  Leading  ") == "leading"
