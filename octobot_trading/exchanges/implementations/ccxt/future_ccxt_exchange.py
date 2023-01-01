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
import decimal

from octobot_trading.exchanges.implementations.ccxt import ccxt_exchange_commons
import octobot_trading.exchanges.types as exchanges_types
import octobot_trading.enums as trading_enums

#TODO remove
class FutureCCXTExchange(exchanges_types.FutureExchange,
                         ccxt_exchange_commons.CCXTExchangeCommons):

    def get_default_type(self):
        return 'future'

    async def get_positions(self, symbols=None, **kwargs: dict) -> list:
        return await self.connector.get_positions(symbols=symbols, **kwargs)

    async def get_position(self, symbol: str, **kwargs: dict) -> dict:
        return await self.connector.get_position(symbol=symbol, **kwargs)

    async def get_funding_rate(self, symbol: str, **kwargs: dict) -> dict:
        return await self.connector.get_funding_rate(symbol=symbol, **kwargs)

    async def get_funding_rate_history(self, symbol: str, limit: int = 1, **kwargs: dict) -> list:
        return await self.connector.get_funding_rate_history(symbol=symbol, limit=limit, **kwargs)

    async def set_symbol_leverage(self, symbol: str, leverage: int, **kwargs: dict):
        return await self.connector.set_symbol_leverage(leverage=leverage, symbol=symbol, **kwargs)

    async def set_symbol_margin_type(self, symbol: str, isolated: bool):
        return await self.connector.set_symbol_margin_type(symbol=symbol, isolated=isolated)

    async def set_symbol_position_mode(self, symbol: str, one_way: bool):
        return await self.connector.set_symbol_position_mode(symbol=symbol, one_way=one_way)

    async def set_symbol_partial_take_profit_stop_loss(self, symbol: str, inverse: bool,
                                                       tp_sl_mode: trading_enums.TakeProfitStopLossMode):
        return await self.connector.set_symbol_partial_take_profit_stop_loss(symbol=symbol, inverse=inverse,
                                                                             tp_sl_mode=tp_sl_mode)

    def get_pair_market_type(self, pair, property_name, def_value=False):
        return self.connector.client.safe_string(
            self.connector.client.safe_value(self.connector.client.markets, pair, {}), property_name, def_value
        )

    def is_linear_symbol(self, symbol):
        return self.get_pair_market_type(symbol, "linear") == "True"

    def is_inverse_symbol(self, symbol):
        return self.get_pair_market_type(symbol, "inverse") == "True"

    def is_futures_symbol(self, symbol):
        return self.get_pair_market_type(symbol, "futures") == "True"

    def is_swap_symbol(self, symbol):
        return self.get_pair_market_type(symbol, "swap") == "True"

    def is_option_symbol(self, symbol):
        return self.get_pair_market_type(symbol, "option") == "True"

    def parse_position(self, position_dict) -> dict:
        try:
            position_dict.update({
                trading_enums.ExchangeConstantsPositionColumns.SYMBOL.value:
                    position_dict.get(position_dict[trading_enums.ExchangePositionCCXTColumns.SYMBOL.value]),
                trading_enums.ExchangeConstantsPositionColumns.TIMESTAMP.value:
                    position_dict.get(trading_enums.ExchangePositionCCXTColumns.TIMESTAMP.value,
                                      self.connector.get_exchange_current_time()),
                trading_enums.ExchangeConstantsPositionColumns.SIDE.value:
                    self.parse_position_side(
                        position_dict.get(trading_enums.ExchangePositionCCXTColumns.SIDE.value,
                                          trading_enums.PositionSide.UNKNOWN.value), None),
                trading_enums.ExchangeConstantsPositionColumns.MARGIN_TYPE.value:
                    position_dict.get(trading_enums.ExchangePositionCCXTColumns.MARGIN_TYPE.value, None),
                trading_enums.ExchangeConstantsPositionColumns.POSITION_SIZE.value:
                    decimal.Decimal(
                        f"{position_dict.get(trading_enums.ExchangePositionCCXTColumns.CONTRACTS.value, 0)}"),
                trading_enums.ExchangeConstantsPositionColumns.CONTRACT_SIZE.value:
                    decimal.Decimal(
                        f"{position_dict.get(trading_enums.ExchangePositionCCXTColumns.CONTRACT_SIZE.value, 0)}"),
                trading_enums.ExchangeConstantsPositionColumns.COLLATERAL.value:
                    decimal.Decimal(
                        f"{position_dict.get(trading_enums.ExchangePositionCCXTColumns.COLLATERAL.value, 0)}"),
                trading_enums.ExchangeConstantsPositionColumns.POSITION_VALUE.value:
                    decimal.Decimal(
                        f"{position_dict.get(trading_enums.ExchangePositionCCXTColumns.NOTIONAL.value, 0)}"),
                trading_enums.ExchangeConstantsPositionColumns.LEVERAGE.value:
                    decimal.Decimal(
                        f"{position_dict.get(trading_enums.ExchangePositionCCXTColumns.LEVERAGE.value, 0)}"),
                trading_enums.ExchangeConstantsPositionColumns.UNREALIZED_PNL.value:
                    decimal.Decimal(
                        f"{position_dict.get(trading_enums.ExchangePositionCCXTColumns.UNREALIZED_PNL.value, 0)}"),
                trading_enums.ExchangeConstantsPositionColumns.REALIZED_PNL.value:
                    decimal.Decimal(
                        f"{position_dict.get(trading_enums.ExchangePositionCCXTColumns.REALIZED_PNL.value, 0)}"),
                trading_enums.ExchangeConstantsPositionColumns.LIQUIDATION_PRICE.value:
                    decimal.Decimal(
                        f"{position_dict.get(trading_enums.ExchangePositionCCXTColumns.LIQUIDATION_PRICE.value, 0)}"),
                trading_enums.ExchangeConstantsPositionColumns.MARK_PRICE.value:
                    decimal.Decimal(
                        f"{position_dict.get(trading_enums.ExchangePositionCCXTColumns.MARK_PRICE.value, 0)}"),
                trading_enums.ExchangeConstantsPositionColumns.ENTRY_PRICE.value:
                    decimal.Decimal(
                        f"{position_dict.get(trading_enums.ExchangePositionCCXTColumns.ENTRY_PRICE.value, 0)}"),
            })
        except KeyError as e:
            self.logger.error(f"Fail to parse position dict ({e})")
        return position_dict
