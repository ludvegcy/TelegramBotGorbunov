from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Index, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class PaymentStatus(enum.Enum):
    PENDING = "pending"      # Ожидает оплаты
    PAID = "paid"            # Оплачено (для Stars финальный статус)
    SUCCEEDED = "succeeded"  # Успешно завершено (для ЮKassa)
    CANCELLED = "cancelled"  # Отменено
    REFUNDED = "refunded"    # Возврат

class PaymentMethod(enum.Enum):
    STARS = "stars"
    YOOKASSA = "yookassa"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    activity = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    daily_calories = Column(Integer, nullable=True)
    is_premium = Column(Boolean, default=False)
    premium_until = Column(DateTime, nullable=True)

class WeightEntry(Base):
    __tablename__ = 'weight_entries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    weight = Column(Float)
    date = Column(DateTime, default=datetime.now, index=True)

class FoodEntry(Base):
    __tablename__ = 'food_entries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    food_name = Column(String)
    calories = Column(Integer)
    protein = Column(Float)
    fat = Column(Float)
    carbs = Column(Float)
    date = Column(DateTime, default=datetime.now, index=True)

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    review_type = Column(String(20), nullable=False)
    target_id = Column(Integer, nullable=True)
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now, index=True)

    __table_args__ = (
        Index('ix_reviews_type_target', 'review_type', 'target_id'),
    )

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    tariff_id = Column(String, nullable=False)                # идентификатор тарифа из TARIFFS
    amount = Column(Float, nullable=False)                    # сумма в рублях или количество звёзд
    currency = Column(String, default='RUB')                  # валюта (RUB или XTR)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    provider_payment_id = Column(String, unique=True, nullable=True)  # ID платежа от Telegram/ЮKassa
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)