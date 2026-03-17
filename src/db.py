from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from src.models import Base, User, WeightEntry, FoodEntry
from datetime import datetime, timedelta
import os
import asyncio
from typing import Optional, List, Dict
from cachetools import TTLCache
from src.config import ADMINS

if not os.path.exists('data'):
    os.makedirs('data')

engine = create_async_engine(
    'sqlite+aiosqlite:///data/fitness_bot.db',
    echo=False,
    connect_args={"check_same_thread": False, "timeout": 30}
)

# Асинхронная фабрика сессий
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # type: ignore

# Кэш для пользователей
user_cache = TTLCache(maxsize=1000, ttl=300)

async def create_tables():
    """Создает все таблицы в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы успешно созданы")

try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(create_tables())
    else:
        loop.run_until_complete(create_tables())
except RuntimeError:
    asyncio.run(create_tables())

class DatabaseManager:
    @staticmethod
    async def get_user(telegram_id: int) -> Optional[User]:
        cache_key = f"user_{telegram_id}"
        if cache_key in user_cache:
            return user_cache[cache_key]

        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                user_cache[cache_key] = user
            return user

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            return await session.get(User, user_id)

    @staticmethod
    async def create_user(telegram_id: int, first_name: str = None, last_name: str = None, weight=None, height=None, age=None,
                         gender=None, activity=None, goal=None, daily_calories=None,
                         is_premium=False, premium_until=None) -> User:
        async with AsyncSessionLocal() as session:
            user = User(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                weight=weight,
                height=height,
                age=age,
                gender=gender,
                activity=activity,
                goal=goal,
                daily_calories=daily_calories,
                is_premium=is_premium,
                premium_until=premium_until
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            user_cache[f"user_{telegram_id}"] = user
            return user

    @staticmethod
    async def update_user(telegram_id: int, **kwargs) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                await session.commit()
                await session.refresh(user)
                user_cache[f"user_{telegram_id}"] = user
            return user

    @staticmethod
    async def add_weight_entry(telegram_id: int, weight: float) -> Optional[WeightEntry]:
        async with AsyncSessionLocal() as session:
            user = await DatabaseManager.get_user(telegram_id)
            if not user:
                return None
            entry = WeightEntry(user_id=user.id, weight=weight)
            session.add(entry)
            user.weight = weight
            await session.commit()
            await session.refresh(entry)
            user_cache[f"user_{telegram_id}"] = user
            return entry

    @staticmethod
    async def get_weight_history(telegram_id: int, days: int = 30) -> List[WeightEntry]:
        async with AsyncSessionLocal() as session:
            user = await DatabaseManager.get_user(telegram_id)
            if not user:
                return []
            cutoff_date = datetime.now() - timedelta(days=days)
            stmt = select(WeightEntry).where(
                WeightEntry.user_id == user.id,
                WeightEntry.date >= cutoff_date
            ).order_by(WeightEntry.date)
            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def add_food_entry(telegram_id: int, food_name: str, calories: int, protein: float, fat: float, carbs: float) -> Optional[FoodEntry]:
        async with AsyncSessionLocal() as session:
            user = await DatabaseManager.get_user(telegram_id)
            if not user:
                return None
            entry = FoodEntry(
                user_id=user.id,
                food_name=food_name,
                calories=calories,
                protein=protein,
                fat=fat,
                carbs=carbs
            )
            session.add(entry)
            await session.commit()
            await session.refresh(entry)
            return entry

    @staticmethod
    async def get_today_food(telegram_id: int) -> List[FoodEntry]:
        async with AsyncSessionLocal() as session:
            user = await DatabaseManager.get_user(telegram_id)
            if not user:
                return []
            today = datetime.now().date()
            stmt = select(FoodEntry).where(
                FoodEntry.user_id == user.id,
                FoodEntry.date >= today
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def get_today_totals(telegram_id: int) -> Dict[str, float]:
        entries = await DatabaseManager.get_today_food(telegram_id)
        return {
            'calories': sum(e.calories for e in entries),
            'protein': sum(e.protein for e in entries),
            'fat': sum(e.fat for e in entries),
            'carbs': sum(e.carbs for e in entries)
        }

    @staticmethod
    async def get_all_users_count() -> int:
        async with AsyncSessionLocal() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            return len(result.scalars().all())

    @staticmethod
    async def get_premium_users_count() -> int:
        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.is_premium == True)
            result = await session.execute(stmt)
            return len(result.scalars().all())

    @staticmethod
    async def is_premium_user(telegram_id: int) -> bool:
        """Проверяет, является ли пользователь премиум (с учётом срока действия и админов)"""
        if telegram_id in ADMINS:
            return True

        user = await DatabaseManager.get_user(telegram_id)
        if not user:
            return False
        if user.is_premium:
            if user.premium_until and user.premium_until < datetime.now():
                await DatabaseManager.update_user(telegram_id, is_premium=False)
                return False
            return True
        return False