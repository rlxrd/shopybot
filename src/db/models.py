from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    
    basket_rel: Mapped[list['Basket']] = relationship(back_populates='user_rel')


class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    
    item_rel: Mapped[list['Item']] = relationship(back_populates='category_rel')


class Item(Base):
    __tablename__ = 'items'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    photo: Mapped[str] = mapped_column(String(200))
    price: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category_rel: Mapped['Category'] = relationship(back_populates='item_rel')
    basket_rel: Mapped[list['Basket']] = relationship(back_populates='item_rel')
    

class Basket(Base):
    __tablename__ = 'basket'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item: Mapped[int] = mapped_column(ForeignKey('items.id'))
    
    user_rel: Mapped['User'] = relationship(back_populates='basket_rel')
    item_rel: Mapped['Item'] = relationship(back_populates='basket_rel')
