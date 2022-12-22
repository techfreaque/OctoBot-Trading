import decimal

import octobot_trading.constants as constants
import octobot_trading.enums as enums
import octobot_trading.exchanges.parser.parser as parser_util


class OrdersParser(parser_util.Parser):
    """
    use OrdersParser as a base class if you implement
    a new parser for a non ccxt or crypto feed exchange

    parser usage:   parser = OrdersParser(exchange)
                    orders = await parser.parse_orders(raw_orders)
                    order = await parser.parse_order(raw_order)
    """

    TIMESTAMP_KEYS: list = []
    STATUS_KEYS: list = []
    ID_KEYS: list = []
    SYMBOL_KEYS: list = []
    SIDE_KEYS: list = []
    TYPE_KEYS: list = []
    TAKER_OR_MAKER_KEYS: list = []
    PRICE_KEYS: list = []
    FILLED_PRICE_KEYS: list = []
    AMOUNT_KEYS: list = []
    REMAINING_KEYS: list = []
    FILLED_AMOUNT_KEYS: list = []
    COST_KEYS: list = []
    REDUCE_ONLY_KEYS: list = []
    TIME_IN_FORCE_KEYS: list = []
    TAG_KEYS: list = []
    FEE_KEYS: list = []
    QUANTITY_CURRENCY_KEYS: list = []

    USE_INFO_SUB_DICT_FOR_TIMESTAMP: bool = False
    USE_INFO_SUB_DICT_FOR_STATUS: bool = False
    USE_INFO_SUB_DICT_FOR_ID: bool = False
    USE_INFO_SUB_DICT_FOR_SYMBOL: bool = False
    USE_INFO_SUB_DICT_FOR_SIDE: bool = False
    USE_INFO_SUB_DICT_FOR_TYPE: bool = False
    USE_INFO_SUB_DICT_FOR_TAKER_OR_MAKER: bool = False
    USE_INFO_SUB_DICT_FOR_PRICE: bool = False
    USE_INFO_SUB_DICT_FOR_FILLED_PRICE: bool = False
    USE_INFO_SUB_DICT_FOR_AMOUNT: bool = False
    USE_INFO_SUB_DICT_FOR_REMAINING: bool = False
    USE_INFO_SUB_DICT_FOR_FILLED_AMOUNT: bool = False
    USE_INFO_SUB_DICT_FOR_COST: bool = False
    USE_INFO_SUB_DICT_FOR_REDUCE_ONLY: bool = False
    USE_INFO_SUB_DICT_FOR_TIME_IN_FORCE: bool = False
    USE_INFO_SUB_DICT_FOR_TAG: bool = False
    USE_INFO_SUB_DICT_FOR_FEES: bool = False
    USE_INFO_SUB_DICT_FOR_CONTRACT_SIZE_CURRENCY: bool = False

    STATUS_MAP: dict = {
        # for example:
        # "weirdClosedStatus": enums.OrderStatus.CLOSED.value,
        # "weirdSecondClosedStatus": enums.OrderStatus.CLOSED.value,
        enums.OrderStatus.PENDING_CREATION.value:
            enums.OrderStatus.PENDING_CREATION.value,
        enums.OrderStatus.OPEN.value: enums.OrderStatus.OPEN.value,
        enums.OrderStatus.PARTIALLY_FILLED.value:
            enums.OrderStatus.PARTIALLY_FILLED.value,
        enums.OrderStatus.FILLED.value: enums.OrderStatus.FILLED.value,
        enums.OrderStatus.CANCELED.value: enums.OrderStatus.CANCELED.value,
        enums.OrderStatus.PENDING_CANCEL.value: enums.OrderStatus.PENDING_CANCEL.value,
        enums.OrderStatus.CLOSED.value: enums.OrderStatus.CLOSED.value,
        enums.OrderStatus.EXPIRED.value: enums.OrderStatus.EXPIRED.value,
        enums.OrderStatus.REJECTED.value: enums.OrderStatus.REJECTED.value,
    }

    TRADER_ORDER_TYPE_MAP: dict = {
        # for example:
        # "weirdStopOrder": enums.TraderOrderType.STOP_LOSS.value,
        # "weirdSecondStop": enums.TraderOrderType.STOP_LOSS.value,
        # enums.TraderOrderTypes
        enums.TraderOrderType.BUY_MARKET.value: enums.TraderOrderType.BUY_MARKET.value,
        enums.TraderOrderType.BUY_LIMIT.value: enums.TraderOrderType.BUY_LIMIT.value,
        enums.TraderOrderType.STOP_LOSS.value: enums.TraderOrderType.STOP_LOSS.value,
        enums.TraderOrderType.STOP_LOSS_LIMIT.value:
            enums.TraderOrderType.STOP_LOSS_LIMIT.value,
        enums.TraderOrderType.SELL_MARKET.value:
            enums.TraderOrderType.SELL_MARKET.value,
        enums.TraderOrderType.SELL_LIMIT.value: enums.TraderOrderType.SELL_LIMIT.value,
        enums.TraderOrderType.TRAILING_STOP.value:
            enums.TraderOrderType.TRAILING_STOP.value,
        enums.TraderOrderType.TRAILING_STOP_LIMIT.value:
            enums.TraderOrderType.TRAILING_STOP_LIMIT.value,
        enums.TraderOrderType.TAKE_PROFIT.value:
            enums.TraderOrderType.TAKE_PROFIT.value,
        enums.TraderOrderType.TAKE_PROFIT_LIMIT.value:
            enums.TraderOrderType.TAKE_PROFIT_LIMIT.value,
        # enums.TradeOrderTypes
        enums.TradeOrderType.STOP_LOSS.value: enums.TraderOrderType.STOP_LOSS.value,
        enums.TradeOrderType.STOP_LOSS_LIMIT.value:
            enums.TraderOrderType.STOP_LOSS_LIMIT.value,
        enums.TradeOrderType.TAKE_PROFIT.value:
            enums.TraderOrderType.TAKE_PROFIT.value,
        enums.TradeOrderType.TAKE_PROFIT_LIMIT.value:
            enums.TraderOrderType.TAKE_PROFIT_LIMIT.value,
        enums.TradeOrderType.TRAILING_STOP.value:
            enums.TraderOrderType.TRAILING_STOP.value,
        enums.TradeOrderType.TRAILING_STOP_LIMIT.value:
            enums.TraderOrderType.TRAILING_STOP_LIMIT.value,
    }
    TRADER_ORDER_TYPE_BUY_MAP: dict = {
        # for example:
        # "weirdLimitOrder": enums.TraderOrderType.BUY_LIMIT.value,
        # "weirdSecondLimit": enums.TraderOrderType.BUY_LIMIT.value,
        enums.TradeOrderType.LIMIT.value: enums.TraderOrderType.BUY_LIMIT.value,
        enums.TradeOrderType.MARKET.value: enums.TraderOrderType.BUY_MARKET.value,
        enums.TradeOrderType.LIMIT_MAKER.value: enums.TraderOrderType.BUY_LIMIT.value,
    }
    TRADER_ORDER_TYPE_SELL_MAP: dict = {
        # for example:
        # "weirdLimitOrder": enums.TraderOrderType.SELL_LIMIT.value,
        # "weirdSecondLimit": enums.TraderOrderType.SELL_LIMIT.value,
        enums.TradeOrderType.LIMIT.value: enums.TraderOrderType.SELL_LIMIT.value,
        enums.TradeOrderType.MARKET.value: enums.TraderOrderType.SELL_MARKET.value,
        enums.TradeOrderType.LIMIT_MAKER.value: enums.TraderOrderType.SELL_LIMIT.value,
    }

    TRADE_ORDER_SIDE_MAP: dict = {
        enums.TradeOrderSide.BUY.value: enums.TradeOrderSide.BUY.value,
        enums.TradeOrderSide.SELL.value: enums.TradeOrderSide.SELL.value,
    }

    def __init__(self, exchange, parser_type_name: str = "orders"):
        super().__init__(
            exchange=exchange,
            parser_type_name=parser_type_name,
        )
        self.fetched_order: dict = {}

    async def parse_orders(
        self,
        raw_orders: list,
        order_type: str = None,
        quantity: decimal.Decimal = None,
        price: decimal.Decimal = None,
        status: str = None,
        symbol: str = None,
        side: str = None,
        timestamp: int or float = None,
        check_completeness: bool = True,
    ) -> list:
        """
        use this method to parse a raw list of orders

        :param raw_orders:

        optional:
        :param status: to use if it's missing in the order
        :param order_type: to use if it's missing in the order
        :param price: to use if it's missing in the order
        :param quantity: to use if it's missing in the order
        :param symbol: to use if it's missing in the order
        :param side: to use if it's missing in the order
        :param timestamp: to use if it's missing in the order

        :param check_completeness: if true checks all attributes,
            if somethings missing it'll try to fetch it from the exchange

        :return: formatted orders list of order dicts
        """
        check_completeness = (
            check_completeness if check_completeness is not None else True
        )
        self._ensure_list(raw_orders)
        self.formatted_records = (
            [
                await self.parse_order(
                    raw_order,
                    order_type=order_type,
                    quantity=quantity,
                    price=price,
                    status=status,
                    symbol=symbol,
                    side=side,
                    timestamp=timestamp,
                    check_completeness=check_completeness,
                )
                for raw_order in raw_orders
            ]
            if self.raw_records
            else []
        )
        if check_completeness:
            self.reporter.create_debugging_report(self)
        return self.formatted_records

    async def parse_order(
        self,
        raw_order: dict,
        order_type: str = None,
        quantity: decimal.Decimal = None,
        price: decimal.Decimal = None,
        status: str = None,
        symbol: str = None,
        side: str = None,
        timestamp: int or float = None,
        check_completeness: bool = True,
    ) -> dict:
        """
        use this method to format a single order

        :param raw_order: raw order with eventually missing data

        optional:
        :param status: to use if it's missing in the order
        :param order_type: to use if it's missing in the order
        :param price: to use if it's missing in the order
        :param quantity: to use if it's missing in the order
        :param symbol: to use if it's missing in the order
        :param side: to use if it's missing in the order
        :param timestamp: to use if it's missing in the order

        :param check_completeness: if true checks all attributes,
            if somethings missing it'll try to fetch it from the exchange

        :return: formatted order dict (100% complete or we raise NotImplemented)

        """
        self.fetched_order = None  # clear previous fetched order
        self._ensure_dict(raw_order)
        try:
            self._parse_timestamp(timestamp)
            self._parse_status(status)
            self._parse_id()  # parse after status and timestamp
            self._parse_symbol(symbol)
            self._parse_side(side)
            self._parse_order_type(order_type)  # parse after side
            self._parse_taker_or_maker()  # parse after type
            self._parse_price(price)  # parse after type, status
            self._parse_filled_price()  # parse after price
            self._parse_amount(quantity)  # parse after price
            self._parse_remaining()  # parse after amount and status
            self._parse_filled_amount()  # parse after amount and remaining
            self._parse_cost()
            self._parse_reduce_only()  # parse after type
            self._parse_time_in_force()
            self._parse_tag()
            self._parse_fees()
            self._parse_quantity_currency()  # remove? is it used?

            await self._apply_after_parse_fixes()
        except Exception as error:
            # just in case something bad happens
            # this should never happen, check the parser code
            self._log_missing(
                "failed to parse orders",
                "not able to complete orders parser",
                error=error,
            )
        if check_completeness:
            await self._fetch_if_missing()
            self.reporter.create_debugging_report_for_record(self)
        return self.formatted_record

    async def _apply_after_parse_fixes(self):
        """
        override if you need to patch a order after parsing
        otherwise override methods
        """
        pass

    def _parse_timestamp(self, missing_timestamp_value):
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.TIMESTAMP.value,
            self.TIMESTAMP_KEYS,
            parse_method=parser_util.convert_any_time_to_seconds,
            not_found_val=missing_timestamp_value,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_TIMESTAMP,
        )

    def _parse_status(self, missing_status_value):
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.STATUS.value,
            self.STATUS_KEYS,
            parse_method=self._found_status,
            not_found_val=missing_status_value,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_STATUS,
        )

    def _found_status(self, raw_status):
        try:
            return enums.OrderStatus(self.STATUS_MAP[raw_status.lower()]).value
        except (ValueError, KeyError):
            pass
        self._log_missing(
            enums.ExchangeConstantsOrderColumns.STATUS.value,
            f"{self.STATUS_KEYS} found raw_status ({raw_status or 'no status'})",
        )

    def _parse_id(self):
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.ID.value,
            self.ID_KEYS,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_ID,
        )

    def _parse_symbol(self, missing_symbol):
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.SYMBOL.value,
            self.SYMBOL_KEYS,
            not_found_val=missing_symbol,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_SYMBOL,
        )

    def _parse_order_type(self, missing_type_value=None):
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.TYPE.value,
            self.TYPE_KEYS,
            parse_method=self._octobot_order_type_found,
            not_found_method=self._missing_octobot_order_type,
            not_found_val=missing_type_value,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_TYPE,
        )

    def _octobot_order_type_found(
        self,
        raw_order_type,
    ):
        raw_order_type = raw_order_type.lower()  # just in case
        try:
            return enums.TraderOrderType(
                self.TRADER_ORDER_TYPE_MAP[raw_order_type]
            ).value
        except (KeyError, ValueError):
            side = self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.SIDE.value
            )
            try:
                if side == enums.TradeOrderSide.BUY.value:
                    return enums.TraderOrderType(
                        self.TRADER_ORDER_TYPE_BUY_MAP[raw_order_type]
                    ).value
                if side == enums.TradeOrderSide.SELL.value:
                    return enums.TraderOrderType(
                        self.TRADER_ORDER_TYPE_SELL_MAP[raw_order_type]
                    ).value
            except (KeyError, ValueError):
                pass
            raise parser_util.ParserKeyNotFoundError

    def _missing_octobot_order_type(self, missing_type_value):
        taker_or_maker = None
        if missing_type_value:
            return enums.TraderOrderType(missing_type_value).value
        if taker_or_maker := self.raw_record.get(
            enums.ExchangeConstantsOrderColumns.TAKER_OR_MAKER.value
        ):
            # todo check - is it safe?
            if (
                self.formatted_record[enums.ExchangeConstantsOrderColumns.SIDE.value]
                == enums.TradeOrderSide.BUY.value
            ):
                if (
                    taker_or_maker
                    == enums.ExchangeConstantsMarketPropertyColumns.TAKER.value
                ):
                    return enums.TraderOrderType.BUY_MARKET.value
                if (
                    taker_or_maker
                    == enums.ExchangeConstantsMarketPropertyColumns.MAKER.value
                ):
                    return enums.TraderOrderType.BUY_LIMIT.value
            elif (
                self.formatted_record[enums.ExchangeConstantsOrderColumns.SIDE.value]
                == enums.TradeOrderSide.SELL.value
            ):
                if (
                    taker_or_maker
                    == enums.ExchangeConstantsMarketPropertyColumns.TAKER.value
                ):
                    return enums.TraderOrderType.SELL_MARKET.value
                if (
                    taker_or_maker
                    == enums.ExchangeConstantsMarketPropertyColumns.MAKER.value
                ):
                    return enums.TraderOrderType.SELL_LIMIT.value
        self._log_missing(
            enums.ExchangeConstantsOrderColumns.TYPE.value,
            f"{self.TYPE_KEYS} not found and based on taker_or_maker "
            f"({taker_or_maker or 'no taker_or_maker'}) which also failed to parse",
        )

    def _parse_side(self, missing_side_value):
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.SIDE.value,
            self.SIDE_KEYS,
            parse_method=self._found_side,
            not_found_val=missing_side_value,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_SIDE,
        )

    def _found_side(self, raw_side):
        return enums.TradeOrderSide(self.TRADE_ORDER_SIDE_MAP[raw_side.lower()]).value

    def _parse_price(self, missing_price_value):
        self._try_to_find_and_set_decimal(
            enums.ExchangeConstantsOrderColumns.PRICE.value,
            self.PRICE_KEYS,
            not_found_val=missing_price_value,
            enable_log=False if missing_price_value else True,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_PRICE,
        )

    def _parse_filled_price(self):
        self._try_to_find_and_set_decimal(
            enums.ExchangeConstantsOrderColumns.FILLED_PRICE.value,
            self.FILLED_PRICE_KEYS,
            not_found_method=self.missing_filled_price,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_FILLED_PRICE,
        )

    def missing_filled_price(self, _):
        if status := self.formatted_record.get(
            enums.ExchangeConstantsOrderColumns.STATUS.value
        ):
            if status in (
                enums.OrderStatus.FILLED.value,
                enums.OrderStatus.CLOSED.value,
                enums.OrderStatus.PARTIALLY_FILLED.value,
            ) and (
                price := self.formatted_record.get(
                    enums.ExchangeConstantsOrderColumns.PRICE.value
                )
            ):
                return price
            if status in (
                enums.OrderStatus.CANCELED.value,
                enums.OrderStatus.OPEN.value,
                enums.OrderStatus.PENDING_CANCEL.value,
                enums.OrderStatus.EXPIRED.value,
                enums.OrderStatus.PENDING_CREATION.value,
                enums.OrderStatus.REJECTED.value,
            ):
                return 0
        self._log_missing(
            enums.ExchangeConstantsOrderColumns.FILLED_PRICE.value,
            f"key: {self.FILLED_PRICE_KEYS}, "
            f"and using status ({status or 'no status'})",
        )

    def _parse_amount(self, missing_quantity_value):
        self._try_to_find_and_set_decimal(
            enums.ExchangeConstantsOrderColumns.AMOUNT.value,
            self.AMOUNT_KEYS,
            not_found_val=missing_quantity_value,
            enable_log=False if missing_quantity_value else True,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_AMOUNT,
        )

    def _parse_cost(self):
        self._try_to_find_and_set_decimal(
            enums.ExchangeConstantsOrderColumns.COST.value,
            self.COST_KEYS,
            not_found_method=self.missing_cost,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_COST,
        )

    def missing_cost(self, _):
        # check and should it be with fees?
        filled_price = None
        if (
            self.exchange.exchange_manager.is_spot_only
            and (
                filled_quantity := self.formatted_record.get(
                    enums.ExchangeConstantsOrderColumns.FILLED_AMOUNT.value
                )
            )
            is not None
            and (
                filled_price := self.formatted_record.get(
                    enums.ExchangeConstantsOrderColumns.FILLED_PRICE.value
                )
            )
        ):
            return filled_quantity * filled_price
        if (
            status := self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.STATUS.value
            )
        ) and status not in (
            enums.OrderStatus.FILLED,
            enums.OrderStatus.CLOSED,
            enums.OrderStatus.PARTIALLY_FILLED,
        ):
            return constants.ZERO
        # only required for filled orders
        spot_message = (
            f" and failed to calculate based on: "
            f"filled-quantity ({filled_quantity or 'no filled_quantity'}) "
            f"* ({filled_price or 'no filled_price'})"
            if self.exchange.exchange_manager.is_spot_only
            else ""
        )
        self._log_missing(
            enums.ExchangeConstantsOrderColumns.COST.value,
            f"key: {self.COST_KEYS} is missing" + spot_message,
        )

    def _parse_quantity_currency(self):
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.QUANTITY_CURRENCY.value,
            self.QUANTITY_CURRENCY_KEYS,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_CONTRACT_SIZE_CURRENCY,
            enable_log=False,  # todo is this important?
        )

    def _parse_remaining(self):
        self._try_to_find_and_set_decimal(
            enums.ExchangeConstantsOrderColumns.REMAINING.value,
            self.REMAINING_KEYS,
            not_found_method=self.missing_remaining,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_REMAINING,
        )

    def missing_remaining(self, _):
        if status := self.formatted_record.get(
            enums.ExchangeConstantsOrderColumns.STATUS.value
        ):
            if status in (
                enums.OrderStatus.FILLED.value,
                enums.OrderStatus.CLOSED.value,
                enums.OrderStatus.CANCELED.value,
                enums.OrderStatus.REJECTED.value,
                enums.OrderStatus.EXPIRED.value,
            ):
                return 0
            if (
                amount := self.formatted_record.get(
                    enums.ExchangeConstantsOrderColumns.AMOUNT.value
                )
            ) and status in (
                enums.OrderStatus.PENDING_CREATION.value,
                enums.OrderStatus.OPEN.value,
                enums.OrderStatus.PENDING_CANCEL.value,
            ):
                return amount
            if status == enums.OrderStatus.PARTIALLY_FILLED.value:
                pass  # just here to let you know whats unhandled

        self._log_missing(
            enums.ExchangeConstantsOrderColumns.REMAINING.value,
            f"key {self.REMAINING_KEYS} and based on status ({status or 'no status'})",
        )

    def _parse_filled_amount(self):
        self._try_to_find_and_set_decimal(
            enums.ExchangeConstantsOrderColumns.FILLED_AMOUNT.value,
            self.FILLED_AMOUNT_KEYS,
            not_found_method=self._missing_filled_amount,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_FILLED_AMOUNT,
        )

    def _missing_filled_amount(self, _):
        remaining = None
        if status := self.formatted_record.get(
            enums.ExchangeConstantsOrderColumns.STATUS.value
        ):
            if (
                amount := self.formatted_record.get(
                    enums.ExchangeConstantsOrderColumns.AMOUNT.value
                )
            ) and status in (
                enums.OrderStatus.FILLED.value,
                enums.OrderStatus.CLOSED.value,
            ):
                return amount
            if status in (
                enums.OrderStatus.EXPIRED.value,
                enums.OrderStatus.CANCELED.value,
                enums.OrderStatus.REJECTED.value,
                enums.OrderStatus.EXPIRED.value,
                enums.OrderStatus.PENDING_CREATION.value,
                enums.OrderStatus.OPEN.value,
                enums.OrderStatus.PENDING_CANCEL.value,
            ):
                return constants.ZERO
            if status == enums.OrderStatus.PARTIALLY_FILLED.value:
                pass  # just here to let you know whats unhandled
        if (
            amount := self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.AMOUNT.value
            )
        ) and (
            remaining := self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.REMAINING.value
            )
        ):
            return amount - remaining

        self._log_missing(
            enums.ExchangeConstantsOrderColumns.FILLED_AMOUNT.value,
            f"based on {self.FILLED_AMOUNT_KEYS}, "
            f"based on amount ({amount or 'no amount'}) - "
            f"remaining ({remaining or 'no remaining'})"
            f"based on status ({status or 'no status'})",
        )

    def _parse_taker_or_maker(self):
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.TAKER_OR_MAKER.value,
            self.TAKER_OR_MAKER_KEYS,
            not_found_method=self.missing_taker_or_maker,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_TAKER_OR_MAKER,
        )

    def missing_taker_or_maker(self, _):
        if order_type := self.formatted_record.get(
            enums.ExchangeConstantsOrderColumns.TYPE.value
        ):
            if order_type in (
                enums.TraderOrderType.BUY_MARKET.value,
                enums.TraderOrderType.SELL_MARKET.value,
                enums.TraderOrderType.STOP_LOSS.value,
                enums.TraderOrderType.TRAILING_STOP.value,
            ):
                return enums.ExchangeConstantsMarketPropertyColumns.TAKER.value
            if order_type in (
                enums.TraderOrderType.SELL_LIMIT.value,
                enums.TraderOrderType.BUY_LIMIT.value,
                enums.TraderOrderType.STOP_LOSS_LIMIT.value,
                enums.TraderOrderType.TAKE_PROFIT_LIMIT.value,
                enums.TraderOrderType.TRAILING_STOP_LIMIT.value,
            ):
                return enums.ExchangeConstantsMarketPropertyColumns.MAKER.value
        self._log_missing(
            enums.ExchangeConstantsOrderColumns.TAKER_OR_MAKER.value,
            f"with key {self.TAKER_OR_MAKER_KEYS} and based on"
            f" order type ({order_type or 'no order_type'})",
        )

    def _parse_reduce_only(self):
        # optional
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.REDUCE_ONLY.value,
            self.REDUCE_ONLY_KEYS,
            not_found_method=self.missing_reduce_only,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_REDUCE_ONLY,
            allowed_falsely_values=(False,),
        )

    def _parse_time_in_force(self):
        # optional
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.TIME_IN_FORCE.value,
            self.TIME_IN_FORCE_KEYS,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_TIME_IN_FORCE,
            enable_log=False,
        )

    def missing_reduce_only(self, _):
        if (
            self.formatted_record.get(enums.ExchangeConstantsOrderColumns.TYPE.value)
            == enums.TraderOrderType.STOP_LOSS.value
        ):
            return True
        return None  # dont raise as it's optional

    def _parse_tag(self):
        # optional
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.TAG.value,
            self.TAG_KEYS,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_TAG,
            enable_log=False,
        )

    def _parse_fees(self):
        # optional
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.FEE.value,
            self.FEE_KEYS,
            parse_method=self.found_fees,
            enable_log=False,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_FEES,
        )

    def found_fees(self, fees_dict_or_list):
        # fees example for paid fees in USDT:
        # {'code': 'USDT', 'cost': -0.015922}
        fees_dict = None
        if isinstance(fees_dict_or_list, dict):
            fees_dict = fees_dict_or_list
        elif isinstance(fees_dict_or_list, list):
            fees_dict = fees_dict_or_list[0]
        if fees_dict:
            if enums.ExchangeConstantsFeesColumns.CURRENCY.value not in fees_dict and (
                currency := fees_dict.get("code")
            ):
                fees_dict[enums.ExchangeConstantsFeesColumns.CURRENCY.value] = currency
                fees_dict.pop("code")
            if fee := fees_dict[enums.ExchangeConstantsFeesColumns.COST.value]:
                fees_dict[enums.ExchangeConstantsFeesColumns.COST.value] = (
                    fee if fee < 0 else fee * -1
                )
            if (
                fees_dict[enums.ExchangeConstantsFeesColumns.CURRENCY.value]
                and fees_dict[enums.ExchangeConstantsFeesColumns.COST.value]
            ):
                return fees_dict

    async def _fetch_if_missing(self):
        to_find_id = self.formatted_record.get(
            enums.ExchangeConstantsOrderColumns.ID.value
        )
        if (
            self.reporter.debugging_report_dict
            and to_find_id
            and (
                symbol := self.formatted_record.get(
                    enums.ExchangeConstantsOrderColumns.SYMBOL.value
                )
            )
        ):
            if fetched_order := await self.exchange.get_order(
                order_id=to_find_id, symbol=symbol, check_completeness=False
            ):
                self.fetched_order = fetched_order  # just for debugging purpose
                # overwrite with fetched order details
                for key in (
                    enums.ExchangeConstantsOrderColumns.STATUS.value,
                    enums.ExchangeConstantsOrderColumns.TIMESTAMP.value,
                    enums.ExchangeConstantsOrderColumns.SYMBOL.value,
                    enums.ExchangeConstantsOrderColumns.SIDE.value,
                    enums.ExchangeConstantsOrderColumns.TYPE.value,
                    enums.ExchangeConstantsOrderColumns.TAKER_OR_MAKER.value,
                    enums.ExchangeConstantsOrderColumns.PRICE.value,
                    enums.ExchangeConstantsOrderColumns.FILLED_PRICE.value,
                    enums.ExchangeConstantsOrderColumns.AMOUNT.value,
                    enums.ExchangeConstantsOrderColumns.REMAINING.value,
                    enums.ExchangeConstantsOrderColumns.FILLED_AMOUNT.value,
                    enums.ExchangeConstantsOrderColumns.COST.value,
                    enums.ExchangeConstantsOrderColumns.REDUCE_ONLY.value,
                    enums.ExchangeConstantsOrderColumns.TAG.value,
                    enums.ExchangeConstantsOrderColumns.FEE.value,
                ):
                    self.set_fetched_attribute(fetched_order, key)

    def set_fetched_attribute(self, fetched_order, key):
        value = fetched_order.get(key, None)
        if value is None:
            return
        self.formatted_record[key] = value
        if key in self.reporter.debugging_report_dict:
            self.reporter.debugging_report_dict.pop(key)