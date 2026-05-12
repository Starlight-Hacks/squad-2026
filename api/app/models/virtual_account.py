from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class VirtualAccount(Base):
    __tablename__ = 'virtual_accounts'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), unique=True)
    user: Mapped['User'] = relationship(back_populates='virtual_account')

    virtual_account_number: Mapped[str]
    bank_name: Mapped[str]
    account_name: Mapped[str]
    squad_customer_id: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
