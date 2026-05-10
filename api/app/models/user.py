import uuid

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.types import Time

from app.models.base import Base
from app.models.profile import Profile


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    profile: Mapped['Profile'] = relationship(back_populates='user', uselist=False)
    phone_number: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    bvn_verified: Mapped[bool]
    created_at: Mapped[Time]
