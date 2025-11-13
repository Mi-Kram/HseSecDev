import html
import re
from pathlib import Path
from typing import Any, List


class InputValidationError(ValueError):
    """Custom exception for input validation errors"""

    pass


def validate_text_content(text: str, field_name: str, max_length: int = 1000) -> str:
    """Validate and sanitize text content"""
    if not isinstance(text, str):
        raise InputValidationError(f"{field_name} must be a string")

    if len(text.strip()) == 0:
        raise InputValidationError(f"{field_name} cannot be empty")

    if len(text) > max_length:
        raise InputValidationError(
            f"{field_name} exceeds maximum length of {max_length} characters"
        )

    # Check for SQL injection patterns
    sql_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"(--|\#|\/\*|\*\/)",
    ]

    for pattern in sql_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            raise InputValidationError(f"{field_name} contains potentially malicious content")

    # HTML sanitization
    sanitized = html.escape(text.strip())

    return sanitized


def validate_numeric_range(
    value: Any, field_name: str, min_val: float = 0, max_val: float = 999999
) -> float:
    """Validate numeric values within specified range"""
    try:
        num_value = float(value)
    except (ValueError, TypeError):
        raise InputValidationError(f"{field_name} must be a valid number")

    if num_value < min_val or num_value > max_val:
        raise InputValidationError(f"{field_name} must be between {min_val} and {max_val}")

    return num_value


def validate_file_path(file_path: str, allowed_extensions: List[str] = None) -> str:
    """Validate file path against path traversal attacks"""
    if not isinstance(file_path, str):
        raise InputValidationError("File path must be a string")

    # Check for path traversal patterns in the input string
    if ".." in file_path or file_path.startswith("/"):
        raise InputValidationError("Invalid file path: path traversal detected")

    # Normalize path
    path = Path(file_path).resolve()

    # Check file extension
    if allowed_extensions:
        if not any(str(path).lower().endswith(ext.lower()) for ext in allowed_extensions):
            raise InputValidationError(f"File extension not allowed. Allowed: {allowed_extensions}")

    return file_path  # Return original filename, not resolved path


def validate_email(email: str) -> str:
    """Validate email format"""
    if not isinstance(email, str):
        raise InputValidationError("Email must be a string")

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        raise InputValidationError("Invalid email format")

    return email.lower().strip()


def validate_url(url: str) -> str:
    """Validate URL format"""
    if not isinstance(url, str):
        raise InputValidationError("URL must be a string")

    url_pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
    if not re.match(url_pattern, url):
        raise InputValidationError("Invalid URL format")

    return url.strip()


def sanitize_html_content(html_content: str) -> str:
    """Sanitize HTML content by removing potentially dangerous tags"""
    # Remove script tags and their content
    html_content = re.sub(
        r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>", "", html_content, flags=re.IGNORECASE
    )

    # Remove javascript: protocols
    html_content = re.sub(r"javascript:", "", html_content, flags=re.IGNORECASE)

    # Remove on* event handlers
    html_content = re.sub(r'\son\w+\s*=\s*["\'][^"\']*["\']', "", html_content, flags=re.IGNORECASE)

    return html_content
