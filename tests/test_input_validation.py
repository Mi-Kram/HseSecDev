import pytest

from src.presentation.validators.input_validators import (
    InputValidationError,
    sanitize_html_content,
    validate_email,
    validate_file_path,
    validate_numeric_range,
    validate_text_content,
    validate_url,
)


def test_validate_text_content_success():
    """Test successful text validation"""
    result = validate_text_content("Hello World", "test_field", max_length=100)
    assert result == "Hello World"


def test_validate_text_content_empty():
    """Test validation rejects empty text"""
    with pytest.raises(InputValidationError, match="cannot be empty"):
        validate_text_content("", "test_field")


def test_validate_text_content_too_long():
    """Test validation rejects text that's too long"""
    long_text = "x" * 1001
    with pytest.raises(InputValidationError, match="exceeds maximum length"):
        validate_text_content(long_text, "test_field", max_length=1000)


def test_validate_text_content_sql_injection():
    """Test validation rejects SQL injection attempts"""
    with pytest.raises(InputValidationError, match="potentially malicious content"):
        validate_text_content("'; DROP TABLE users; --", "test_field")

    with pytest.raises(InputValidationError, match="potentially malicious content"):
        validate_text_content("1 OR 1=1", "test_field")


def test_validate_text_content_html_escaping():
    """Test that HTML is properly escaped"""
    result = validate_text_content("<script>alert('xss')</script>", "test_field")
    assert result == "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"


def test_validate_numeric_range_success():
    """Test successful numeric validation"""
    result = validate_numeric_range(50, "test_field", min_val=0, max_val=100)
    assert result == 50.0


def test_validate_numeric_range_out_of_bounds():
    """Test validation rejects numbers out of range"""
    with pytest.raises(InputValidationError, match="must be between 0 and 100"):
        validate_numeric_range(150, "test_field", min_val=0, max_val=100)

    with pytest.raises(InputValidationError, match="must be between 0 and 100"):
        validate_numeric_range(-10, "test_field", min_val=0, max_val=100)


def test_validate_numeric_range_invalid_type():
    """Test validation rejects non-numeric values"""
    with pytest.raises(InputValidationError, match="must be a valid number"):
        validate_numeric_range("not_a_number", "test_field")


def test_validate_file_path_success():
    """Test successful file path validation"""
    result = validate_file_path("test.txt", [".txt", ".pdf"])
    assert result == "test.txt"


def test_validate_file_path_traversal():
    """Test validation rejects path traversal attempts"""
    with pytest.raises(InputValidationError, match="path traversal detected"):
        validate_file_path("../../../etc/passwd")

    with pytest.raises(InputValidationError, match="path traversal detected"):
        validate_file_path("/etc/passwd")


def test_validate_file_path_invalid_extension():
    """Test validation rejects invalid file extensions"""
    with pytest.raises(InputValidationError, match="File extension not allowed"):
        validate_file_path("test.exe", [".txt", ".pdf"])


def test_validate_email_success():
    """Test successful email validation"""
    result = validate_email("test@example.com")
    assert result == "test@example.com"


def test_validate_email_invalid():
    """Test validation rejects invalid email formats"""
    with pytest.raises(InputValidationError, match="Invalid email format"):
        validate_email("invalid-email")

    with pytest.raises(InputValidationError, match="Invalid email format"):
        validate_email("@example.com")


def test_validate_url_success():
    """Test successful URL validation"""
    result = validate_url("http://example.com")
    assert result == "http://example.com"


def test_validate_url_invalid():
    """Test validation rejects invalid URL formats"""
    with pytest.raises(InputValidationError, match="Invalid URL format"):
        validate_url("not-a-url")

    with pytest.raises(InputValidationError, match="Invalid URL format"):
        validate_url("ftp://example.com")


def test_sanitize_html_content():
    """Test HTML content sanitization"""
    malicious_html = '<script>alert("xss")</script><p>Safe content</p>'
    result = sanitize_html_content(malicious_html)
    assert "<script>" not in result
    assert "<p>Safe content</p>" in result

    # Test javascript: protocol removal
    malicious_html = '<a href="javascript:alert(1)">Click me</a>'
    result = sanitize_html_content(malicious_html)
    assert "javascript:" not in result

    # Test event handler removal
    malicious_html = '<div onclick="alert(1)">Click me</div>'
    result = sanitize_html_content(malicious_html)
    assert "onclick=" not in result
