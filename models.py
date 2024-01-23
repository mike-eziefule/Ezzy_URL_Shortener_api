"""Describe the database."""
from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class URL(Base):
    """Define the URL model."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    private_key = Column(String, unique=True)
    target_url = Column(String,)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
