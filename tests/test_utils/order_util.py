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

from octobot_commons.asyncio_tools import wait_asyncio_next_cycle

from tests.util.random_numbers import random_recent_trade, random_price


async def fill_limit_or_stop_order(limit_or_stop_order):
    await limit_or_stop_order.on_fill()
    await wait_asyncio_next_cycle()


async def fill_market_order(market_order):
    await market_order.on_fill()
    await wait_asyncio_next_cycle()
