from src.db import AsyncSessionLocal
from src.models import Review, User
from sqlalchemy import select
from typing import List, Optional

class ReviewManager:
    @staticmethod
    async def create_review(telegram_id: int, review_type: str, text: str, target_id: Optional[int] = None, rating: Optional[int] = None) -> Optional[Review]:
        async with AsyncSessionLocal() as session:
            # Ищем пользователя
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                # Создаём нового пользователя
                user = User(telegram_id=telegram_id)
                session.add(user)
                await session.commit()
                await session.refresh(user)

            review = Review(
                user_id=user.id,
                review_type=review_type,
                target_id=target_id,
                text=text,
                rating=rating
            )
            session.add(review)
            await session.commit()
            await session.refresh(review)
            return review

    @staticmethod
    async def get_reviews_by_type(review_type: str, target_id: Optional[int] = None, limit: int = 50) -> List[Review]:
        async with AsyncSessionLocal() as session:
            stmt = select(Review).where(Review.review_type == review_type)
            if target_id is not None:
                stmt = stmt.where(Review.target_id == target_id)
            stmt = stmt.order_by(Review.created_at.desc()).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def get_reviews_by_user(telegram_id: int) -> List[Review]:
        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                return []
            stmt = select(Review).where(Review.user_id == user.id).order_by(Review.created_at.desc())
            result = await session.execute(stmt)
            return result.scalars().all()