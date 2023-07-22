import uuid
from typing import (
    List,
    Optional,
)

from sqlalchemy import (
    DECIMAL,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Menu(Base):
    """Menu model."""
    __tablename__ = 'menus'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(155), unique=True, nullable=False
    )
    description: Mapped[Optional[String]] = mapped_column(String(500))

    submenus: Mapped[List['Submenu']] = relationship(
        back_populates='menu', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'Menu(id={self.id}, title={self.title})'


class Submenu(Base):
    """Submenu model."""
    __tablename__ = 'submenus'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(155), unique=True, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(String(500))
    menu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('menus.id'))

    menu: Mapped['Menu'] = relationship(back_populates='submenus')
    dishes: Mapped[List['Dish']] = relationship(
        back_populates='submenu', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'Submenu(id={self.id}, title={self.title}, menu={self.menu_id})'


class Dish(Base):
    """Dish model."""
    __tablename__ = 'dishes'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(155), unique=True, nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(String(500))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))
    submenu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('submenus.id'))

    submenu: Mapped['Submenu'] = relationship(back_populates='dishes')

    def __repr__(self):
        return (f'Dish('
                f'id={self.id},'
                f' title={self.title},'
                f' submenu={self.submenu_id},'
                f' price={self.price})')
