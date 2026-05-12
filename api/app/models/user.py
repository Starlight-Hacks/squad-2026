from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.functions import func

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.payment_confirmation_token import PaymentConfirmationToken
    from app.models.profile import Profile
    from app.models.virtual_account import VirtualAccount


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    profile: Mapped[Optional['Profile']] = relationship(back_populates='user', uselist=False)
    virtual_account: Mapped[Optional['VirtualAccount']] = relationship(back_populates='user', uselist=False)
    payment_confirmation_token: Mapped[Optional['PaymentConfirmationToken']] = relationship(
        back_populates='user', uselist=False
    )

    phone_number: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[Optional[str]]
    date_of_birth: Mapped[Optional[str]]
    address: Mapped[Optional[str]]
    gender: Mapped[Optional[str]]

    bvn_hash: Mapped[Optional[str]]
    bvn_verified: Mapped[bool] = mapped_column(default=False)
    phone_verified: Mapped[bool] = mapped_column(default=False)

    account_number: Mapped[Optional[str]]
    bank_code: Mapped[Optional[str]]

    geo_lat: Mapped[Optional[float]]
    geo_lng: Mapped[Optional[float]]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
