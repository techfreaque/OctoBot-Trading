# cython: language_level=3
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
#  Lesser General License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
cimport octobot_trading.personal_data.orders.order as order_class
cimport octobot_trading.exchanges as exchanges

cdef class Trade:
    cdef public exchanges.Trader trader
    cdef public exchanges.ExchangeManager exchange_manager

    cdef public object side # TradeOrderSide
    cdef public object status # OrderStatus
    cdef public object trade_type # TraderOrderType

    cdef public str symbol
    cdef public str currency
    cdef public str market
    cdef public str taker_or_maker
    cdef public str trade_id
    cdef public bint simulated

    cdef public double origin_price
    cdef public double origin_quantity
    cdef public double market_total_fees
    cdef public double executed_quantity
    cdef public double executed_price
    cdef public double total_cost
    cdef public double trade_profitability

    cdef public double timestamp
    cdef public double creation_time
    cdef public double canceled_time
    cdef public double executed_time

    cdef public dict fee # Dict[str, Union[str, double]]

    cdef public object exchange_trade_type # raw exchange trade type, used to create trade dict

    cpdef void update_from_order(self,
                                 order_class.Order order,
                                 double canceled_time=*,
                                 double creation_time=*,
                                 double executed_time=*)