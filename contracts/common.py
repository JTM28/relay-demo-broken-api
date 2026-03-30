from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error: str = Field(description="Stable machine-readable error code.")
    message: str = Field(description="Human-readable summary of what went wrong.")
    context: dict[str, str] = Field(default_factory=dict, description="Optional structured context.")
