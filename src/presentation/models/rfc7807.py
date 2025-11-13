from typing import Any, Dict, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ProblemDetail(BaseModel):
    """RFC 7807 Problem Details for HTTP APIs"""

    type: str = Field(
        default="about:blank", description="A URI reference that identifies the problem type"
    )
    title: str = Field(description="A short, human-readable summary of the problem type")
    status: int = Field(description="The HTTP status code")
    detail: str = Field(
        description="A human-readable explanation specific to this occurrence of the problem"
    )
    correlation_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="A unique identifier for tracing this specific error",
    )
    instance: Optional[str] = Field(
        default=None,
        description="A URI reference that identifies the specific occurrence of the problem",
    )
    extensions: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional problem-specific information"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "https://example.com/problems/validation-error",
                "title": "Validation Error",
                "status": 400,
                "detail": "The request contains invalid data",
                "correlation_id": "123e4567-e89b-12d3-a456-426614174000",
                "instance": "/wishes/123",
            }
        }
    )


class SecurityProblemDetail(ProblemDetail):
    """Security-focused problem detail that masks internal information in production"""

    def __init__(self, **data):
        super().__init__(**data)

        # In production, mask internal details
        import os

        if os.getenv("ENVIRONMENT") == "production":
            self.detail = "An error occurred while processing your request"
            self.type = "about:blank"


def create_problem_detail(
    status: int,
    title: str,
    detail: str,
    type_: str = "about:blank",
    instance: Optional[str] = None,
    extensions: Optional[Dict[str, Any]] = None,
) -> ProblemDetail:
    """Factory function to create RFC 7807 problem details"""

    return ProblemDetail(
        type=type_,
        title=title,
        status=status,
        detail=detail,
        instance=instance,
        extensions=extensions,
    )


def create_security_problem_detail(
    status: int,
    title: str,
    detail: str,
    type_: str = "about:blank",
    instance: Optional[str] = None,
    extensions: Optional[Dict[str, Any]] = None,
) -> SecurityProblemDetail:
    """Factory function to create security-focused problem details"""

    return SecurityProblemDetail(
        type=type_,
        title=title,
        status=status,
        detail=detail,
        instance=instance,
        extensions=extensions,
    )
