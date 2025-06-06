from src.infrastructure.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean
from datetime import datetime, timezone

class PasswordReset(Base):
    __tablename__ = 'password_reset'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(), nullable=False)
    minutes_to_live: Mapped[int] = mapped_column(Integer(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)