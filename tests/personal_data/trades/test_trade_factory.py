#  Drakkar-Software OctoBot
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
import decimal
import json
import time

import pytest

from tests import event_loop
from octobot_commons.tests.test_config import load_test_config
from octobot_trading.enums import ExchangeConstantsMarketPropertyColumns, TradeOrderSide, TradeOrderType, TraderOrderType, OrderStatus, FeePropertyColumns
from octobot_trading.constants import ZERO
from octobot_trading.exchanges.exchange_manager import ExchangeManager
from octobot_trading.personal_data.orders.order_factory import create_order_instance_from_raw
from octobot_trading.exchanges.traders.trader_simulator import TraderSimulator
from octobot_trading.enums import ExchangeConstantsOrderColumns

from octobot_trading.personal_data.trades import create_trade_instance_from_raw, create_trade_from_order, \
    create_trade_instance

# All test coroutines will be treated as marked.
from octobot_trading.api.exchange import cancel_ccxt_throttle_task

pytestmark = pytest.mark.asyncio


class TestTradeFactory:
    DEFAULT_SYMBOL = "BTC/USDT"
    EXCHANGE_MANAGER_CLASS_STRING = "binanceus"

    @staticmethod
    async def init_default():
        config = load_test_config()
        exchange_manager = ExchangeManager(config, TestTradeFactory.EXCHANGE_MANAGER_CLASS_STRING)
        await exchange_manager.initialize()

        trader = TraderSimulator(config, exchange_manager)
        await trader.initialize()

        return config, exchange_manager, trader

    @staticmethod
    async def stop(exchange_manager):
        cancel_ccxt_throttle_task()
        await exchange_manager.stop()

    async def test_create_trade_instance_from_raw(self):
        _, exchange_manager, trader = await self.init_default()
        raw_trade = {	
            ExchangeConstantsOrderColumns.ID.value: "12345-67890:09876/54321",
            ExchangeConstantsOrderColumns.STATUS.value: OrderStatus.CLOSED.value,
            ExchangeConstantsOrderColumns.TIMESTAMP.value: 1502962946,
            ExchangeConstantsOrderColumns.SYMBOL.value: "ETH/BTC",
            ExchangeConstantsOrderColumns.ORDER.value: "12345-67890:09876/54321",
            ExchangeConstantsOrderColumns.TYPE.value: TraderOrderType.BUY_LIMIT.value,
            ExchangeConstantsOrderColumns.SIDE.value: TradeOrderSide.BUY.value,
            ExchangeConstantsOrderColumns.TAKER_OR_MAKER.value: ExchangeConstantsMarketPropertyColumns.MAKER.value,
            ExchangeConstantsOrderColumns.PRICE.value: decimal.Decimal("0.06917684"),
            ExchangeConstantsOrderColumns.AMOUNT.value: decimal.Decimal("1.5"),
            ExchangeConstantsOrderColumns.COST.value: decimal.Decimal("0.10376526"),
            ExchangeConstantsOrderColumns.FILLED_PRICE.value: decimal.Decimal("0.06917684"),
            ExchangeConstantsOrderColumns.REMAINING.value: decimal.Decimal("0"),
            ExchangeConstantsOrderColumns.FILLED_AMOUNT.value: decimal.Decimal("1.5"),
            ExchangeConstantsOrderColumns.REDUCE_ONLY.value: None,
            ExchangeConstantsOrderColumns.FEE.value: {
                "cost": 0.0015,
                "currency": "ETH",
                "rate": 0.002
            }
        }


        trade = create_trade_instance_from_raw(trader, raw_trade)

        assert trade.trade_id == '12345-67890:09876/54321'
        assert trade.origin_order_id == '12345-67890:09876/54321'
        assert trade.trade_type == TraderOrderType.BUY_LIMIT
        assert trade.symbol == 'ETH/BTC'
        assert trade.total_cost == decimal.Decimal(str(0.10376526))
        assert trade.executed_quantity == decimal.Decimal(str(1.5))
        assert trade.origin_price == decimal.Decimal(str(0.06917684))
        assert trade.executed_price == decimal.Decimal(str(0.06917684))
        assert trade.executed_time == 1502962946
        assert trade.status == OrderStatus.FILLED
        assert trade.fee == {
            FeePropertyColumns.COST.value: 0.0015,
            FeePropertyColumns.CURRENCY.value: "ETH",
            FeePropertyColumns.RATE.value: 0.002
        }
        assert trade.is_closing_order is True
        assert trade.tag is None

        await self.stop(exchange_manager)

    async def test_create_trade_from_order(self):
        _, exchange_manager, trader = await self.init_default()

        # limit order
        raw_order = {
                ExchangeConstantsOrderColumns.ID.value:                "12345-67890:09876/54321",
                ExchangeConstantsOrderColumns.TIMESTAMP.value:          1502962946,
                ExchangeConstantsOrderColumns.STATUS.value:     "open",
                ExchangeConstantsOrderColumns.SYMBOL.value:     "BTC/USDT",
                ExchangeConstantsOrderColumns.TYPE.value: TraderOrderType.SELL_LIMIT.value,
                ExchangeConstantsOrderColumns.SIDE.value:       "sell",
                ExchangeConstantsOrderColumns.TAKER_OR_MAKER.value: "maker",
                ExchangeConstantsOrderColumns.PRICE.value:       decimal.Decimal("7684"),
                ExchangeConstantsOrderColumns.FILLED_PRICE.value:       decimal.Decimal("7684"),
                ExchangeConstantsOrderColumns.AMOUNT.value:      decimal.Decimal("1.5"),
                ExchangeConstantsOrderColumns.FILLED_AMOUNT.value:      decimal.Decimal("1.1"),
                ExchangeConstantsOrderColumns.REMAINING.value:   decimal.Decimal("0.4"),
                ExchangeConstantsOrderColumns.COST.value:        decimal.Decimal("0.076094524"),
                ExchangeConstantsOrderColumns.FEE.value: {
                    "currency": "BTC",
                    "cost": 0.0009,
                    "rate": 0.002
                }
            }
            

        order = create_order_instance_from_raw(trader, raw_order)
        order.tag = "tag"
        trade = create_trade_from_order(order, close_status=OrderStatus.FILLED)

        assert trade.trade_id == '12345-67890:09876/54321'
        assert trade.origin_order_id == '12345-67890:09876/54321'
        assert trade.simulated is True
        assert trade.trade_type == TraderOrderType.SELL_LIMIT
        assert trade.symbol == 'BTC/USDT'
        assert trade.total_cost == decimal.Decimal(str(0.076094524))
        assert trade.executed_quantity == decimal.Decimal(str(1.1))
        assert trade.origin_quantity == decimal.Decimal(str(1.5))
        assert trade.origin_price == decimal.Decimal("7684")
        assert trade.executed_price == decimal.Decimal("7684")
        assert trade.status == OrderStatus.FILLED
        assert trade.is_closing_order is True
        assert trade.tag == 'tag'

        trade = create_trade_from_order(order)
        assert trade.status == OrderStatus.FILLED

        exec_time = time.time()
        trade = create_trade_from_order(order, executed_time=exec_time)
        assert trade.executed_time == exec_time

        # market order
        raw_order = {
            ExchangeConstantsOrderColumns.ID.value: '362550114',
            ExchangeConstantsOrderColumns.TIMESTAMP.value: 1637579281,
            ExchangeConstantsOrderColumns.SYMBOL.value: 'UNI/USDT',
            ExchangeConstantsOrderColumns.TYPE.value: TraderOrderType.SELL_MARKET.value,
            ExchangeConstantsOrderColumns.SIDE.value: 'sell',
            ExchangeConstantsOrderColumns.TAKER_OR_MAKER.value: "taker",
            ExchangeConstantsOrderColumns.PRICE.value: decimal.Decimal("4500"),
            ExchangeConstantsOrderColumns.STOP_PRICE.value: None,
            ExchangeConstantsOrderColumns.AMOUNT.value: decimal.Decimal(44964.0),
            ExchangeConstantsOrderColumns.COST.value: None,
            ExchangeConstantsOrderColumns.FILLED_PRICE.value: decimal.Decimal("4500"),
            ExchangeConstantsOrderColumns.FILLED_AMOUNT.value: decimal.Decimal(44964.0),
            ExchangeConstantsOrderColumns.REMAINING.value: decimal.Decimal(0.0),
            ExchangeConstantsOrderColumns.STATUS.value: 'closed',
            ExchangeConstantsOrderColumns.FEE.value: {'cost': 0.03764836, 'currency': 'USDT'},
        }
        order = create_order_instance_from_raw(trader, raw_order)
        trade = create_trade_from_order(order, close_status=OrderStatus.FILLED)

        assert trade.trade_id == '362550114'
        assert trade.origin_order_id == '362550114'
        assert trade.trade_type == TraderOrderType.SELL_MARKET
        assert trade.symbol == 'UNI/USDT'
        assert trade.total_cost == decimal.Decimal("202338000")
        assert trade.executed_quantity == decimal.Decimal("44964.0")
        assert trade.origin_quantity == decimal.Decimal("44964.0")
        assert trade.origin_price == decimal.Decimal("4500")
        assert trade.executed_price == decimal.Decimal("4500")
        assert trade.status == OrderStatus.FILLED
        assert trade.executed_time == 1637579281
        assert trade.is_closing_order is True

        await self.stop(exchange_manager)

    async def test_create_trade_from_partially_filled_order(self):
        _, exchange_manager, trader = await self.init_default()

        raw_order =  {
                ExchangeConstantsOrderColumns.ID.value:                "12345-67890:09876/54321",
                ExchangeConstantsOrderColumns.TIMESTAMP.value:          1502962946,
                ExchangeConstantsOrderColumns.STATUS.value:     "open",
                ExchangeConstantsOrderColumns.SYMBOL.value:     "BTC/USDT",
                ExchangeConstantsOrderColumns.TAKER_OR_MAKER.value: "maker",
                ExchangeConstantsOrderColumns.TYPE.value: TraderOrderType.SELL_LIMIT.value,
                ExchangeConstantsOrderColumns.SIDE.value:       "sell",
                ExchangeConstantsOrderColumns.PRICE.value:       decimal.Decimal("7684"),
                ExchangeConstantsOrderColumns.FILLED_PRICE.value:       decimal.Decimal("7684"),
                ExchangeConstantsOrderColumns.AMOUNT.value:      decimal.Decimal("1.5"),
                ExchangeConstantsOrderColumns.FILLED_AMOUNT.value:      decimal.Decimal("1.1"),
                ExchangeConstantsOrderColumns.REMAINING.value:   decimal.Decimal("0.4"),
                ExchangeConstantsOrderColumns.COST.value:        decimal.Decimal("0.076094524"),
                ExchangeConstantsOrderColumns.FEE.value: {
                    "currency": "BTC",
                    "cost": 0.0009,
                    "rate": 0.002
                }
            }

        order = create_order_instance_from_raw(trader, raw_order)
        trade = create_trade_from_order(order, close_status=OrderStatus.OPEN)

        assert trade.trade_id == '12345-67890:09876/54321'
        assert trade.origin_order_id == '12345-67890:09876/54321'
        assert trade.simulated is True
        assert trade.trade_type == TraderOrderType.SELL_LIMIT
        assert trade.symbol == 'BTC/USDT'
        assert trade.total_cost == decimal.Decimal(str(0.076094524))
        assert trade.executed_quantity == decimal.Decimal(str(1.1))
        assert trade.origin_quantity == decimal.Decimal(str(1.5))
        assert trade.origin_price == decimal.Decimal(str(7684))
        assert trade.executed_price == decimal.Decimal(str(7684))
        assert trade.status == OrderStatus.OPEN
        assert trade.is_closing_order is False

        await self.stop(exchange_manager)

    async def test_create_trade_instance(self):
        _, exchange_manager, trader = await self.init_default()

        trade = create_trade_instance(trader,
                                      order_type=TraderOrderType.SELL_MARKET,
                                      symbol="ETH/USDT",
                                      quantity_filled=decimal.Decimal(str(1.2)),
                                      total_cost=decimal.Decimal(str(10)))

        assert trade.trade_id is not None

        assert trade.symbol == "ETH/USDT"
        assert trade.trade_type == TraderOrderType.SELL_MARKET
        assert round(trade.executed_quantity, 3) == decimal.Decimal(str(1.2))
        assert trade.total_cost == decimal.Decimal(str(10))

        await self.stop(exchange_manager)
