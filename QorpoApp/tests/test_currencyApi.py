import ccxt

from unittest import IsolatedAsyncioTestCase
from unittest import mock

from QorpoApp.utils.currencyApi import get_price_currency


class TestCurrencyApi(IsolatedAsyncioTestCase):
    @mock.patch("ccxt.async_support.kucoin")
    async def test_ok_btc(self, mock_kucoin) -> None:
        mock_exchange = mock.AsyncMock()
        mock_exchange.fetch_ticker.return_value = {"bid": 12345}
        mock_kucoin.return_value = mock_exchange

        result = await get_price_currency("BTC")
        self.assertEqual(result, 12345)

    @mock.patch("ccxt.async_support.kucoin")
    async def test_failed_in_symbol(self, mock_kucoin) -> None:
        mock_exchange = mock.AsyncMock()
        mock_exchange.fetch_ticker.side_effect = ccxt.BadSymbol
        mock_kucoin.return_value = mock_exchange

        with self.assertLogs(level='ERROR') as cm:
            result = await get_price_currency("sdfkjsndfkjsndk")

        self.assertEqual(result, None)
        self.assertIn("Unknown currency", cm.output[0])

    @mock.patch("ccxt.async_support.kucoin")
    async def test_failed_in_unexpected(self, mock_kucoin) -> None:
        mock_exchange = mock.AsyncMock()
        mock_exchange.fetch_ticker.side_effect = TypeError
        mock_kucoin.return_value = mock_exchange

        with self.assertLogs(level='ERROR') as cm:
            result = await get_price_currency("BTC")

        self.assertEqual(result, None)
        self.assertIn("Unexpected error in get_price_currency", cm.output[0])
