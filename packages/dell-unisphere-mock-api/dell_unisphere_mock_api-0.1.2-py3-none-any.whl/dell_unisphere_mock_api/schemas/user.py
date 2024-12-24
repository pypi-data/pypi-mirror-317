"""User schema models."""

from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Base user model."""

    id: str = Field(..., description="Unique identifier for the user")
    username: str = Field(..., description="Username")
    role: str = Field(..., description="User role (e.g., admin)")


class UserCreate(UserBase):
    """Model for creating a new user."""

    password: str = Field(..., description="User password")


class UserUpdate(BaseModel):
    """Model for updating an existing user."""

    password: Optional[str] = Field(None, description="New password")
    role: Optional[str] = Field(None, description="New role")


class UserResponse(UserBase):
    """Model for user response."""

    class Config:
        """Pydantic configuration."""

        from_attributes = True
