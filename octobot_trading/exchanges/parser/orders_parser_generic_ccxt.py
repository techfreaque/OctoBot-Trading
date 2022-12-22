import octobot_trading.constants as constants
import octobot_trading.enums as enums
import octobot_trading.exchanges.parser.orders_parser_ccxt as orders_parser_ccxt
import octobot_trading.exchanges.parser.orders_parser_cryptofeed \
    as orders_parser_cryptofeed


class GenericCCXTOrdersParser(orders_parser_ccxt.CCXTOrdersParser):
    """
    Dont override this class, use CCXTOrdersParser instead

    always/only include bulletproof custom code
        into the parser to improve generic support

    parser usage:   parser = GenericCCXTOrdersParser(exchange)
                    orders = await parser.parse_orders(raw_orders)
                    order = await parser.parse_order(raw_order)
    """

    TEST_AND_FIX_SPOT_QUANTITIES: bool = False
    TEST_AND_FIX_FUTURES_QUANTITIES: bool = False

    MARKET_ORDERS_WITH_STOP_PRICE_ARE_STOP_ORDERS: bool = False

    REDUCE_ONLY_KEYS: list = [
        enums.ExchangeOrderCCXTColumns.REDUCE_ONLY.value,
        "reduce_only",
    ]
    USE_INFO_SUB_DICT_FOR_REDUCE_ONLY: bool = True
    PRICE_KEYS: list = [
        # first try average as its more accurate
        enums.ExchangeOrderCCXTColumns.AVERAGE.value,  
        enums.ExchangeOrderCCXTColumns.PRICE.value,
        # use only if others are missing
        enums.ExchangeOrderCCXTColumns.STOP_PRICE.value,  
    ]

    STATUS_MAP: dict = {
        # for example:
        # "weirdClosedStatus": enums.OrderStatus.CLOSED.value,
        # "weirdSecondClosedStatus": enums.OrderStatus.CLOSED.value,
        **orders_parser_ccxt.CCXTOrdersParser.STATUS_MAP,
        "order_new": enums.OrderStatus.OPEN.value,
        "partially_filled_canceled": enums.OrderStatus.PARTIALLY_FILLED.value,
        "order_filled": enums.OrderStatus.FILLED.value,
        "order_canceled": enums.OrderStatus.CANCELED.value,
        "cancelled": enums.OrderStatus.CANCELED.value,
        **orders_parser_cryptofeed.CryptoFeedOrdersParser.STATUS_MAP,
    }

    TRADER_ORDER_TYPE_MAP: dict = {
        # for example:
        # "weirdStopOrder": enums.TraderOrderType.STOP_LOSS.value,
        # "weirdSecondStop": enums.TraderOrderType.STOP_LOSS.value,
        # enums.TraderOrderTypes
        **orders_parser_ccxt.CCXTOrdersParser.TRADER_ORDER_TYPE_MAP,
        **orders_parser_cryptofeed.CryptoFeedOrdersParser.TRADER_ORDER_TYPE_MAP,
    }
    TRADER_ORDER_TYPE_BUY_MAP: dict = {
        # for example:
        # "weirdLimitOrder": enums.TraderOrderType.BUY_LIMIT.value,
        # "weirdSecondLimit": enums.TraderOrderType.BUY_LIMIT.value,
        **orders_parser_ccxt.CCXTOrdersParser.TRADER_ORDER_TYPE_BUY_MAP,
        **orders_parser_cryptofeed.CryptoFeedOrdersParser.TRADER_ORDER_TYPE_BUY_MAP,
    }
    TRADER_ORDER_TYPE_SELL_MAP: dict = {
        # for example:
        # "weirdLimitOrder": enums.TraderOrderType.SELL_LIMIT.value,
        # "weirdSecondLimit": enums.TraderOrderType.SELL_LIMIT.value,
        **orders_parser_ccxt.CCXTOrdersParser.TRADER_ORDER_TYPE_SELL_MAP,
        **orders_parser_cryptofeed.CryptoFeedOrdersParser.TRADER_ORDER_TYPE_SELL_MAP,
    }

    def __init__(
        self,
        exchange,
        parser_type_name: str = "orders",
    ):
        super().__init__(
            exchange=exchange,
            parser_type_name=parser_type_name,
        )

    def _parse_id(self):
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.ID.value,
            self.ID_KEYS,
            not_found_method=self.missing_id,
        )

    def missing_id(self, _):
        # some exchanges dont provide an id
        # use time instead on orders where its not critical
        if (
            (
                status := self.formatted_record.get(
                    enums.ExchangeConstantsOrderColumns.STATUS.value
                )
            )
            == enums.OrderStatus.CLOSED.value
            or status == enums.OrderStatus.CANCELED.value
            or status == enums.OrderStatus.EXPIRED.value
            or status == enums.OrderStatus.REJECTED.value
        ):
            return self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.TIMESTAMP.value
            )
        else:
            self._log_missing(
                enums.ExchangeConstantsOrderColumns.ID.value, f"{self.ID_KEYS}"
            )

    def _parse_side(self, missing_side_value):
        self._try_to_find_and_set(
            enums.ExchangeConstantsOrderColumns.SIDE.value,
            self.SIDE_KEYS,
            parse_method=self._found_side,
            not_found_val=missing_side_value,
            not_found_method=self.missing_side,
            use_info_sub_dict=self.USE_INFO_SUB_DICT_FOR_SIDE,
        )

    def missing_side(self, missing_side_value):
        if missing_side_value:
            return missing_side_value
        if buyer_maker := (
            self.raw_record[enums.ExchangeOrderCCXTColumns.INFO.value].get("isBuyerMaker")
        ):
            return enums.TradeOrderSide.BUY.value
        elif buyer_maker is False:
            return enums.TradeOrderSide.SELL.value
        else:
            self._log_missing(
                enums.ExchangeConstantsOrderColumns.SIDE.value, f"{self.SIDE_KEYS}"
            )

    def _parse_price(self, missing_price_value):
        def handle_found_price(raw_price):
            return self.found_price(raw_price, missing_price_value)

        self._try_to_find_and_set_decimal(
            enums.ExchangeConstantsOrderColumns.PRICE.value,
            self.PRICE_KEYS,
            parse_method=handle_found_price,
            not_found_val=missing_price_value,
        )

    def _parse_order_type(self, missing_type_value=None):
        super()._parse_order_type(missing_type_value)
        if self.MARKET_ORDERS_WITH_STOP_PRICE_ARE_STOP_ORDERS:
            # market orders with no price but with stop price are stop orders
            if self.raw_record.get(
                enums.ExchangeConstantsOrderColumns.STOP_PRICE.value
            ) and not self.raw_record.get(
                enums.ExchangeConstantsOrderColumns.PRICE.value
            ):
                if (
                    (
                        _type := self.formatted_record[
                            enums.ExchangeConstantsOrderColumns.TYPE.value
                        ]
                    )
                    == enums.TraderOrderType.SELL_MARKET.value
                    or _type == enums.TraderOrderType.BUY_MARKET.value
                ):
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.TYPE.value
                    ] = enums.TraderOrderType.STOP_LOSS.value

    def found_price(self, raw_price, missing_price_value):
        order_type = None
        if (
            status := self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.STATUS.value
            )
        ) and (
            order_type := self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.TYPE.value
            )
        ):
            # todo investigate - ccxt is returning a wrong price (~1000k higher on bybit btc)
            # on open market orders so we dont use it
            # tried with ccxt 1.95.36 and 2.1.92
            if (
                missing_price_value
                and (
                    status == enums.OrderStatus.OPEN.value
                    or status == enums.OrderStatus.PENDING_CREATION.value
                )
                and order_type == enums.TradeOrderType.MARKET.value
            ):
                return missing_price_value
            return raw_price
        self._log_missing(
            enums.ExchangeConstantsOrderColumns.PRICE.value,
            f"Parsing price requires status ({status or 'no status'}) "
            f"and order type ({order_type or 'no order type'})",
        )

    def _parse_filled_price(self):
        self._try_to_find_and_set_decimal(
            enums.ExchangeConstantsOrderColumns.FILLED_PRICE.value,
            self.FILLED_PRICE_KEYS,
            not_found_method=self.missing_filled_price,
            enable_log=False,
        )

    def missing_filled_price(self, _):
        # todo check if safe
        filled_quantity = None
        if status := self.formatted_record.get(
            enums.ExchangeConstantsOrderColumns.STATUS.value
        ):
            if (
                status == enums.OrderStatus.FILLED.value
                or status == enums.OrderStatus.CLOSED.value
                or status == enums.OrderStatus.PARTIALLY_FILLED.value
            ) and (
                price := self.formatted_record.get(
                    enums.ExchangeConstantsOrderColumns.PRICE.value
                )
            ):
                return price
            if (
                status == enums.OrderStatus.CANCELED.value
                or status == enums.OrderStatus.OPEN.value
                or status == enums.OrderStatus.PENDING_CANCEL.value
                or status == enums.OrderStatus.EXPIRED.value
                or status == enums.OrderStatus.PENDING_CREATION.value
                or status == enums.OrderStatus.REJECTED.value
            ):
                return 0
        if (
            cost := self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.COST.value
            )
        ) and (
            filled_quantity := self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.FILLED_AMOUNT.value
            )
        ):
            return cost / filled_quantity
        self._log_missing(
            enums.ExchangeConstantsOrderColumns.FILLED_PRICE.value,
            f"key: {self.FILLED_PRICE_KEYS}, "
            f"using status ({status or 'no status'}) and based on "
            f"cost {cost or 'no cost'} / filled quantity "
            f"({filled_quantity or 'no filled quantity'})",
        )

    def _parse_amount(self, missing_quantity_value):
        def handle_amount_found(amount):
            return self._amount_found(amount, missing_quantity_value)

        self._try_to_find_and_set_decimal(
            enums.ExchangeConstantsOrderColumns.AMOUNT.value,
            self.AMOUNT_KEYS,
            parse_method=handle_amount_found,
            not_found_val=missing_quantity_value,
            enable_log=False if missing_quantity_value else True,
        )

    def _amount_found(self, amount, missing_quantity_value):
        if (
            missing_quantity_value
            and self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.STATUS.value
            )
            == enums.OrderStatus.OPEN.value
            and self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.TYPE.value
            )
            == enums.TradeOrderType.MARKET.value
        ):
            # on open market orders dont use values 
            # from the response as they are often wrong
            return missing_quantity_value
        return amount

    def _parse_remaining(
        self,
    ):
        if (
            self.formatted_record.get(enums.ExchangeConstantsOrderColumns.STATUS.value)
            == enums.OrderStatus.OPEN.value
            and self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.TYPE.value
            )
            == enums.TradeOrderType.MARKET.value
        ):
            # dont use fetched value on open market orders
            self.formatted_record[
                enums.ExchangeConstantsOrderColumns.REMAINING.value
            ] = self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.AMOUNT.value
            )
        else:
            super()._parse_remaining()

    async def _apply_after_parse_fixes(self):
        if (
            self.exchange.exchange_manager.is_spot_only
            and self.TEST_AND_FIX_SPOT_QUANTITIES
        ) or (
            self.exchange.exchange_manager.is_future
            and self.TEST_AND_FIX_FUTURES_QUANTITIES
        ):
            amount = self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.AMOUNT.value
            )
            cost = self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.COST.value
            )
            filled = self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.FILLED_AMOUNT.value
            )
            remaining = self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.REMAINING.value
            )
            status = self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.STATUS.value
            )
            price = self.formatted_record.get(
                enums.ExchangeConstantsOrderColumns.PRICE.value
            )
            # fix amount
            if (
                status == enums.OrderStatus.CLOSED.value
                or status == enums.OrderStatus.FILLED.value
                or status == enums.OrderStatus.CANCELED.value
            ):
                if price and amount and cost:
                    if amount * price != cost:
                        # amount mismatch - calculate based on cost
                        amount = self.formatted_record[
                            enums.ExchangeConstantsOrderColumns.AMOUNT.value
                        ] = (cost / price)
                elif status != enums.OrderStatus.CANCELED.value:
                    self._log_missing(
                        enums.ExchangeConstantsOrderColumns.AMOUNT.value,
                        f"price ({price or 'no price'}),"
                        f" amount ({amount or 'no amount'}) and "
                        f"cost ({cost or 'no cost'}) is "
                        "required to test and fix quantities",
                    )

            # fix filled and remaining and cost
            if (
                status == enums.OrderStatus.OPEN.value
                or status == enums.OrderStatus.PENDING_CREATION.value
            ):
                if filled != constants.ZERO:
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.FILLED_AMOUNT.value
                    ] = constants.ZERO
                if cost != constants.ZERO:
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.COST.value
                    ] = constants.ZERO
                if remaining != amount:
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.REMAINING.value
                    ] = amount

            elif (
                status == enums.OrderStatus.CLOSED.value
                or status == enums.OrderStatus.FILLED.value
            ):
                if filled != amount:
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.FILLED_AMOUNT.value
                    ] = amount
                if remaining != constants.ZERO:
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.REMAINING.value
                    ] = constants.ZERO

            elif (
                status == enums.OrderStatus.CANCELED.value
                or status == enums.OrderStatus.EXPIRED.value
                or status == enums.OrderStatus.REJECTED.value
            ):
                if filled != amount:
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.FILLED_AMOUNT.value
                    ] = amount
                if remaining != constants.ZERO:
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.REMAINING.value
                    ] = constants.ZERO
                if cost != constants.ZERO:
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.COST.value
                    ] = constants.ZERO
            elif status == enums.OrderStatus.PARTIALLY_FILLED.value:
                if filled == amount:
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.REMAINING.value
                    ] = constants.ZERO
                    self.formatted_record[
                        enums.ExchangeConstantsOrderColumns.STATUS.value
                    ] = enums.OrderStatus.CLOSED.value
