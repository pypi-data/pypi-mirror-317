import datetime
from datetime import datetime as dt

import pytz

from xarizmi.candlestick import Candlestick
from xarizmi.config import get_config
from xarizmi.db import run_db_migration
from xarizmi.db.actions.candlestick import get_filtered_candlesticks
from xarizmi.db.actions.candlestick import upsert_candlestick
from xarizmi.db.actions.exchange import bulk_upsert_exchanges
from xarizmi.db.actions.portfolio import upsert_portfolio
from xarizmi.db.actions.portfolio.portfolio_read import (
    get_portfolio_items_between_dates,
)
from xarizmi.db.actions.symbol import bulk_upsert_symbols
from xarizmi.db.actions.symbol import get_symbol
from xarizmi.db.client import session_scope
from xarizmi.enums import IntervalTypeEnum
from xarizmi.models.exchange import Exchange
from xarizmi.models.portfolio import Portfolio
from xarizmi.models.portfolio import PortfolioItem
from xarizmi.models.symbol import Symbol


def xarizmi_db_example() -> None:
    config = get_config()
    config.DATABASE_URL = "postgresql://postgres:1@localhost/xarizmi"

    run_db_migration()
    # insert exchanges to exchange table
    with session_scope() as session:
        exchanges = bulk_upsert_exchanges(
            exchanges=[
                Exchange(name=name)
                for name in [
                    "KUCOIN",
                    "crypto.com",
                    "BINANCE",
                    "COINBASE",
                ]
            ],
            session=session,
        )
        print(
            "Exchanges created in db:\n "
            f"{[vars(exchange) for exchange in exchanges]}",
            end="\n-----------\n",
        )

    # insert symbols to Symbol table
    with session_scope() as session:
        bulk_upsert_symbols(
            [
                Symbol.build(
                    base_currency="BTC",
                    quote_currency="USDT",
                    fee_currency="USDT",
                    exchange="COINBASE",
                ),
                Symbol.build(
                    base_currency="ETH",
                    quote_currency="USDT",
                    fee_currency="USDT",
                    exchange="BINANCE",
                ),
                Symbol.build(
                    base_currency="CRO",
                    quote_currency="USDT",
                    fee_currency="USDT",
                    exchange="KUCOIN",
                ),
                Symbol.build(
                    base_currency="CRO",
                    quote_currency="USD",
                    fee_currency="USD",
                    exchange="crypto.com",
                ),
                Symbol.build(
                    base_currency="BTC",
                    quote_currency="USD",
                    fee_currency="USD",
                    exchange="crypto.com",
                ),
            ],
            session=session,
        )

    target_symbol = Symbol.build(
        base_currency="CRO",
        quote_currency="USD",
        fee_currency="USD",
        exchange="crypto.com",
    )

    symbol_id = get_symbol(target_symbol, session=session).id
    upsert_candlestick(
        symbol_id=symbol_id,
        session=session,
        candlestick=Candlestick(
            symbol=target_symbol,
            close=1000,
            open=4,
            low=3,
            high=30000,
            volume=10000,
            amount=1,
            interval=1732385697000,
            datetime=dt(2024, 11, 23, 18, 14, 0, tzinfo=pytz.UTC),
            interval_type=IntervalTypeEnum.HOUR_1,
        ),
    )

    result = get_filtered_candlesticks(session=session, symbol_name="CRO-USD")
    print(">>>>>>>>>>>>>>>>>>>>>")

    portfolio = Portfolio(
        items=[
            PortfolioItem(
                symbol=Symbol.build(
                    base_currency="CRO",
                    quote_currency="USD",
                    fee_currency="USD",
                    exchange="crypto.com",
                ),
                market_value=1000,
                quantity=0.001,
                datetime=dt(2024, 11, 25),
            ),
            PortfolioItem(
                symbol=Symbol.build(
                    base_currency="BTC",
                    quote_currency="USD",
                    fee_currency="USD",
                    exchange="crypto.com",
                ),
                market_value=1000,
                quantity=10000,
                datetime=dt(2024, 11, 25),
            ),
            PortfolioItem(
                symbol=Symbol.build(
                    base_currency="BTC",
                    quote_currency="USD",
                    fee_currency="USD",
                    exchange="crypto.com",
                ),
                market_value=2000,
                quantity=10000,
                datetime=dt(2024, 11, 26),
            ),
        ]
    )

    upsert_portfolio(
        portfolio=portfolio,
        session=session,
    )

    print(result)

    res = get_portfolio_items_between_dates(
        session=session,
        start_date=datetime.datetime(2024, 11, 25),
        end_date=datetime.datetime(2024, 11, 25),
    )
    print(res)
