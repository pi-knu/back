import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class LotPhoto(Base):
    __tablename__ = "lot_photos"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    lot_id = Column(
        UUID(as_uuid=True),
        ForeignKey("lot.id", ondelete="CASCADE"),
        nullable=False,
    )

    url = Column(String(1024), nullable=False)

    lot = relationship("Lot", back_populates="photos")

