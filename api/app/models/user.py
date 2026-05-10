from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.functions import func
from typing_extensions import TYPE_CHECKING

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import Profile


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    profile: Mapped['Profile'] = relationship(back_populates='user', uselist=False)
    phone_number: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    bvn_verified: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
