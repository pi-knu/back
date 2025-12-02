import uuid
from sqlalchemy import Column, String, Text, Numeric, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Lot(Base):
    __tablename__ = "lot"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4, 
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String(255), nullable=False)

    description = Column(Text, nullable=True)

    min_price = Column(Numeric(12, 2), nullable=False)

    min_step = Column(Numeric(12, 2), nullable=False)
    
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    is_finished = Column(Boolean, default=False, nullable=False)
    current_price = Column(Numeric(12, 2), nullable=True)

    user = relationship("User", back_populates="lots")

    photos = relationship(
        "LotPhoto",
        back_populates="lot",
        cascade="all, delete-orphan",
    )
