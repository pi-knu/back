from sqlalchemy import Column, String, Date, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """User account model."""
    __tablename__ = "users"
    
    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    data = relationship(
        "UserData",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


class UserData(Base):
    """User profile data model."""
    __tablename__ = "user_data"
    
    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    user_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    name = Column(String(40))
    birth_date = Column(Date)
    phone = Column(String(30))

    user = relationship("User", back_populates="data")