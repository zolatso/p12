from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship
import datetime
from db_connect import db_connect
import enum

class UserRole(enum.Enum):
    COMMERCIAL = 'commercial'
    GESTION = 'gestion'
    SUPPORT = 'support'


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)

    clients: Mapped[list["Client"]] = relationship("Client", back_populates="user")
    events: Mapped[list["Event"]] = relationship("Event", back_populates="user")


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(100), nullable=False)
    business_name: Mapped[str] = mapped_column(String(100), nullable=False)
    # User is going to input these two dates manually. They may not correspond to table creation/modification.
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),  
        onupdate=datetime.datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="clients")
    contracts: Mapped[list["Contract"]] = relationship("Contract", back_populates="client")
    

class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    amount_remaining: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.datetime.now)
    is_signed: Mapped[bool]

    client: Mapped["Client"] = relationship("Client", back_populates="contracts")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"), unique=True)
    client_contact: Mapped[str] = mapped_column(String(500), nullable=False)
    event_start: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    event_end: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    support_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    attendees: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(String(1000), nullable=True)

    contract: Mapped["Contract"] = relationship("Contract", back_populates="event")
    support: Mapped["User"] = relationship("User", back_populates="events")




if __name__ == "__main__":
    # Create the tables
    engine = db_connect(root=True)
    Base.metadata.create_all(engine)