from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()

class ReviewHistory(Base):
    __tablename__ = 'review_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    stars = Column(Integer, CheckConstraint('stars >= 1 AND stars <= 10'), nullable=False)
    review_id = Column(String(255), nullable=False)
    tone = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey('product_category.id'), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    category = relationship('Category', back_populates='reviews')

class Category(Base):
    __tablename__ = 'product_category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String, nullable=True)

    reviews = relationship('ReviewHistory', back_populates='category')

class AccessLog(Base):
    __tablename__ = 'access_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)