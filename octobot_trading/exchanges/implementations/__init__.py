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

from octobot_trading.exchanges.implementations.cryptofeed import cryptofeed_websocket_exchange
from octobot_trading.exchanges.implementations.cryptofeed.cryptofeed_websocket_exchange import (
    CryptofeedWebSocketExchange,
)
from octobot_trading.exchanges.implementations.simulator import spot_exchange_simulator
from octobot_trading.exchanges.implementations.simulator.spot_exchange_simulator import (
    SpotExchangeSimulator,
)
from octobot_trading.exchanges.implementations.simulator import future_exchange_simulator
from octobot_trading.exchanges.implementations.simulator.future_exchange_simulator import (
    FutureExchangeSimulator,
)
from octobot_trading.exchanges.implementations.simulator import margin_exchange_simulator
from octobot_trading.exchanges.implementations.simulator.margin_exchange_simulator import (
    MarginExchangeSimulator,
)
from octobot_trading.exchanges.implementations.ccxt import future_ccxt_exchange
from octobot_trading.exchanges.implementations.ccxt.future_ccxt_exchange import (
    FutureCCXTExchange,
)
from octobot_trading.exchanges.implementations.ccxt import margin_ccxt_exchange
from octobot_trading.exchanges.implementations.ccxt.margin_ccxt_exchange import (
    MarginCCXTExchange,
)
from octobot_trading.exchanges.implementations.ccxt import spot_ccxt_exchange
from octobot_trading.exchanges.implementations.ccxt.spot_ccxt_exchange import (
    SpotCCXTExchange,
)
from octobot_trading.exchanges.implementations.ccxt import ccxt_exchange_commons
from octobot_trading.exchanges.implementations.ccxt.ccxt_exchange_commons import (
    CCXTExchangeCommons,
)
from octobot_trading.exchanges.implementations.ccxt import ccxt_websocket_exchange
from octobot_trading.exchanges.implementations.ccxt.ccxt_websocket_exchange import (
    CCXTWebSocketExchange,
)
from octobot_trading.exchanges.implementations.ccxt import default_spot_ccxt_exchange
from octobot_trading.exchanges.implementations.ccxt.default_spot_ccxt_exchange import (
    DefaultCCXTSpotExchange,
)
from octobot_trading.exchanges.implementations.cryptofeed import cryptofeed_websocket_exchange
from octobot_trading.exchanges.implementations.cryptofeed.cryptofeed_websocket_exchange import (
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
