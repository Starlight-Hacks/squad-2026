import uuid

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.types import Time

from app.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    phone_number: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    bvn_verified: Mapped[bool]
    created_at: Mapped[Time]
