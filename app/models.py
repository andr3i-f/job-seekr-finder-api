# SQL Alchemy models declaration.
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models
# mapped_column syntax from SQLAlchemy 2.0.

# https://alembic.sqlalchemy.org/en/latest/tutorial.html
# Note, it is used by alembic migrations logic, see `alembic/env.py`

# Alembic shortcuts:
# # create migration
# alembic revision --autogenerate -m "migration_name"

# # apply all migrations
# alembic upgrade head


import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Numeric,
    DateTime,
    ForeignKey,
    String,
    Uuid,
    func,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Test(Base):
    __tablename__ = "test_table"

    test_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    test_name: Mapped[str] = mapped_column(String(128), nullable=False)


class Job(Base):
    __tablename__ = "jobs_table"

    id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    source: Mapped[str] = mapped_column(String(128), nullable=False)
    source_id: Mapped[str] = mapped_column(String(128), nullable=True, unique=True)
    company_name: Mapped[str] = mapped_column(String(128), nullable=False)
    experience_level: Mapped[str] = mapped_column(String(128), nullable=False)
    url: Mapped[Text] = mapped_column(Text, nullable=True)
    salary: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    location: Mapped[str] = mapped_column(String(128), nullable=True)
