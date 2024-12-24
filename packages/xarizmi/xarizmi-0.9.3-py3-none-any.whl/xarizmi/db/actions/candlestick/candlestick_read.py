from datetime import datetime
from typing import Any
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from xarizmi.db.models.candlestick import CandleStick
from xarizmi.db.models.symbol import Symbol


def get_filtered_candlesticks(
    session: Session,
    symbol_name: Optional[str] = None,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 1000,
) -> list[dict[str, Any]]:

    # Base query
    query = select(
        CandleStick,  # All columns from CandleStick
        Symbol.name.label("symbol_name"),  # Symbol name with alias
    ).join(
        Symbol, CandleStick.symbol_id == Symbol.id
    )  # Join with Symbol

    # Add filters
    filters = []
    if symbol_name:
        filters.append(Symbol.name == symbol_name)
    if start_datetime:
        filters.append(CandleStick.datetime >= start_datetime)
    if end_datetime:
        filters.append(CandleStick.datetime <= end_datetime)

    if filters:
        query = query.where(and_(*filters))

    # Add ordering, skip, and limit for pagination
    query = (
        query.order_by(CandleStick.datetime.desc()).offset(skip).limit(limit)
    )

    # Execute the query
    result = session.execute(query)
    return [
        item._asdict() for item in result.all()
    ]  # Return the list of results
