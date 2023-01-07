#  Drakkar-Software OctoBot-Trading
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

from octobot_trading.exchanges.implementations.cryptofeed cimport cryptofeed_websocket_exchange
from octobot_trading.exchanges.implementations.cryptofeed.cryptofeed_websocket_exchange cimport (
    CryptofeedWebSocketExchange,
)
from octobot_trading.exchanges.implementations.simulator cimport spot_exchange_simulator
from octobot_trading.exchanges.implementations.simulator.spot_exchange_simulator cimport (
    SpotExchangeSimulator,
)
from octobot_trading.exchanges.implementations.simulator cimport future_exchange_simulator
from octobot_trading.exchanges.implementations.simulator.future_exchange_simulator cimport (
    FutureExchangeSimulator,
)
from octobot_trading.exchanges.implementations.simulator cimport margin_exchange_simulator
from octobot_trading.exchanges.implementations.simulator.margin_exchange_simulator cimport (
    MarginExchangeSimulator,
)
from octobot_trading.exchanges.implementations.ccxt cimport future_ccxt_exchange
from octobot_trading.exchanges.implementations.ccxt.future_ccxt_exchange cimport (
    FutureCCXTExchange,
)
from octobot_trading.exchanges.implementations.ccxt cimport margin_ccxt_exchange
from octobot_trading.exchanges.implementations.ccxt.margin_ccxt_exchange cimport (
    MarginCCXTExchange,
)
from octobot_trading.exchanges.implementations.ccxt cimport spot_ccxt_exchange
from octobot_trading.exchanges.implementations.ccxt.spot_ccxt_exchange cimport (
    SpotCCXTExchange,
)
from octobot_trading.exchanges.implementations.ccxt cimport ccxt_exchange_commons
from octobot_trading.exchanges.implementations.ccxt_exchange_commons cimport (
    CCXTExchangeCommons,
)
from octobot_trading.exchanges.implementations.ccxt cimport ccxt_websocket_exchange
from octobot_trading.exchanges.implementations.ccxt.ccxt_websocket_exchange cimport (
    CCXTWebSocketExchange,
)
from octobot_trading.exchanges.implementations.ccxt cimport default_spot_ccxt_exchange
from octobot_trading.exchanges.implementations.ccxt.default_spot_ccxt_exchange cimport (
    DefaultCCXTSpotExchange,
)
from octobot_trading.exchanges.implementations.cryptofeed cimport cryptofeed_websocket_exchange
from octobot_trading.exchanges.implementations.cryptofeed.cryptofeed_websocket_exchange cimport (
    CryptofeedWebSocketExchange,
)

__all__ = [
    "SpotExchangeSimulator",
    "FutureExchangeSimulator",
    "MarginExchangeSimulator",
    "FutureCCXTExchange",
    "MarginCCXTExchange",
    "SpotCCXTExchange",
    "CCXTWebSocketExchange",
    "DefaultCCXTSpotExchange",
    "CryptofeedWebSocketExchange",
    "CCXTExchangeCommons",
]
