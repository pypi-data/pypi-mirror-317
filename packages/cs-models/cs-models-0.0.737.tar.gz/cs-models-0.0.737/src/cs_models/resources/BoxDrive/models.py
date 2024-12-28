from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
)

from ...database import Base


class BoxDriveModel(Base):
    __tablename__ = "box_drives"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    org_id = Column(String(128), nullable=True)
    webhook_id = Column(String(128), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
