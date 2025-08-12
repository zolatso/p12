import datetime
import enum
from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.orm import relationship
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError



# Initialize the password hasher
ph = PasswordHasher()

class UserRoleEnum(enum.Enum):
    COMMERCIAL = 'commercial'
    GESTION = 'gestion'
    SUPPORT = 'support'


class Base(DeclarativeBase):
    pass


role_permission_association = Table(
    'role_permission_association',
    Base.metadata,
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', ForeignKey('permissions.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False)

    clients: Mapped[list["Client"]] = relationship("Client", back_populates="user")
    events: Mapped[list["Event"]] = relationship("Event", back_populates="support")
    role_obj: Mapped["Role"] = relationship(back_populates="users")

    def set_password(self, password: str):
        self.hashed_password = ph.hash(password)

    def verify_password(self, password: str) -> bool:
        try:
            ph.verify(self.hashed_password, password)
            return True
        except VerifyMismatchError:
            return False
        except Exception as e:
            # Handle other potential errors during verification (e.g., malformed hash)
            print(f"Error during password verification: {e}")
            return False


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), nullable=False)

    # Define the many-to-many relationship with Permission
    permissions: Mapped[list["Permission"]] = relationship(
        secondary=role_permission_association,
        back_populates="roles"
    )
    # Define a one-to-many relationship with User
    users: Mapped[list["User"]] = relationship(back_populates="role_obj")


class Permission(Base):
    __tablename__ = 'permissions'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)

    # Define the many-to-many relationship with Role
    roles: Mapped[list["Role"]] = relationship(
        secondary=role_permission_association,
        back_populates="permissions"
    )


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    business_name: Mapped[str] = mapped_column(String(100), nullable=False)
    # User is going to input these two dates manually. They may not correspond to table creation/modification.
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),  
        onupdate=datetime.datetime.now)
    # this should be assigned to the user that creates the client
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
    event: Mapped["Event"] = relationship(back_populates="contract", uselist=False)

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





    
    