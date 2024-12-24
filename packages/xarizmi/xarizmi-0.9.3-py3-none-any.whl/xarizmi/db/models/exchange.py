from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from xarizmi.db.models.base import Base


class Exchange(Base):  # type: ignore
    __tablename__ = "xarizmi_exchange"
    name = Column(String, primary_key=True, unique=True)

    symbols: Mapped[list["Symbol"]] = relationship(  # type: ignore  # noqa: F821,E501
        "Symbol", back_populates="exchange"
    )
