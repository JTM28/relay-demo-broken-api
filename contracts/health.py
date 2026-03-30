from pydantic import BaseModel, Field


class HealthContract(BaseModel):
    service: str = Field(description="Public service name.")
    environment: str = Field(description="Current runtime environment name.")
    version: str = Field(description="Application version string.")
    seed_version: str = Field(description="Version marker for the in-memory demo state.")
    storage_mode: str = Field(description="How the current service holds state.")
    resource_counts: dict[str, int] = Field(description="Counts for seeded top-level resources.")
