import logging
import ccxt.async_support as ccxt
from ccxt import BadSymbol


async def get_price_currency(currency) -> float | None:
    pair = f"{currency}/USDT"
    exchange = ccxt.kucoin()
    price = None
    try:
        res = await exchange.fetch_ticker(pair)
        price = res.get("bid")

    except BadSymbol:
        logging.error(f"Unknown currency {currency}")
    except Exception as e:
        logging.error(f"Unexpected error in get_price_currency: {e}")

    await exchange.close()
    return price
