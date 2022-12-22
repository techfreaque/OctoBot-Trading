import cryptofeed.defines as cryptofeed_constants
import octobot_trading.enums as enums
import cryptofeed.types as cryptofeed_types
import octobot_trading.exchanges.parser.orders_parser as orders_parser


class CryptoFeedOrdersParser(orders_parser.OrdersParser):
    """
    override CryptoFeedOrdersParser if you add support for a crypto feed exchange

    parser usage:   parser = CryptoFeedOrdersParser(exchange)
                    orders = await parser.parse_orders(raw_orders)
                    order = await parser.parse_order(raw_order)
    """

    TIMESTAMP_KEYS: list = [enums.ExchangeConstantsOrderColumns.TIMESTAMP.value]
    STATUS_KEYS: list = [enums.ExchangeConstantsOrderColumns.STATUS.value]
    ID_KEYS: list = [enums.ExchangeConstantsOrderColumns.ID.value]
    SYMBOL_KEYS: list = [enums.ExchangeConstantsOrderColumns.SYMBOL.value]
    SIDE_KEYS: list = [enums.ExchangeConstantsOrderColumns.SIDE.value]
    TYPE_KEYS: list = [enums.ExchangeConstantsOrderColumns.TYPE.value]
    TAKER_OR_MAKER_KEYS: list = []
    PRICE_KEYS: list = [enums.ExchangeConstantsOrderColumns.PRICE.value]
    FILLED_PRICE_KEYS: list = []
    AMOUNT_KEYS: list = [enums.ExchangeConstantsOrderColumns.AMOUNT.value]
    REMAINING_KEYS: list = [enums.ExchangeConstantsOrderColumns.REMAINING.value]
    FILLED_AMOUNT_KEYS: list = []
    COST_KEYS: list = []
    REDUCE_ONLY_KEYS: list = []
    TIME_IN_FORCE_KEYS: list = []
    TAG_KEYS: list = []
    FEE_KEYS: list = []
    QUANTITY_CURRENCY_KEYS: list = []

    def __init__(
        self,
        exchange,
        parser_type_name: str = "orders",
    ):
        super().__init__(
            exchange=exchange,
            parser_type_name=parser_type_name,
        )

    STATUS_MAP: dict = {
        # for example:
        # "weirdClosedStatus": enums.OrderStatus.CLOSED.value,
        # "weirdSecondClosedStatus": enums.OrderStatus.CLOSED.value,
        cryptofeed_constants.OPEN: enums.OrderStatus.OPEN.value,
        cryptofeed_constants.PENDING: enums.OrderStatus.OPEN.value,
        cryptofeed_constants.FILLED: enums.OrderStatus.FILLED.value,
        cryptofeed_constants.PARTIAL: enums.OrderStatus.PARTIALLY_FILLED.value,
        cryptofeed_constants.CANCELLED: enums.OrderStatus.CANCELED.value,
        cryptofeed_constants.UNFILLED: enums.OrderStatus.OPEN.value,
        cryptofeed_constants.EXPIRED: enums.OrderStatus.EXPIRED.value,
        cryptofeed_constants.FAILED: enums.OrderStatus.REJECTED.value,
        cryptofeed_constants.SUBMITTING: enums.OrderStatus.PENDING_CREATION.value,
        cryptofeed_constants.CANCELLING: enums.OrderStatus.PENDING_CANCEL.value,
        cryptofeed_constants.CLOSED: enums.OrderStatus.CLOSED.value,
        # cryptofeed_constants.SUSPENDED:  # todo is it canceled?
    }

    TRADER_ORDER_TYPE_MAP: dict = {
        # for example:
        # "weirdStopOrder": enums.TraderOrderType.STOP_LOSS.value,
        # "weirdSecondStop": enums.TraderOrderType.STOP_LOSS.value,
        cryptofeed_constants.STOP_LIMIT: enums.TraderOrderType.STOP_LOSS_LIMIT.value,
        cryptofeed_constants.STOP_MARKET: enums.TraderOrderType.STOP_LOSS.value,
        cryptofeed_constants.MAKER_OR_CANCEL: enums.TraderOrderType.SELL_LIMIT.value,
        # cryptofeed_constants.FILL_OR_KILL: ,
        # cryptofeed_constants.IMMEDIATE_OR_CANCEL: ,
        # cryptofeed_constants.GOOD_TIL_CANCELED: ,
        # cryptofeed_constants.TRIGGER_LIMIT: ,
        # cryptofeed_constants.TRIGGER_MARKET: ,
        # cryptofeed_constants.MARGIN_LIMIT: ,
        # cryptofeed_constants.MARGIN_MARKET: ,
    }
    TRADER_ORDER_TYPE_BUY_MAP: dict = {
        # for example:
        # "weirdLimitOrder": enums.TraderOrderType.BUY_LIMIT.value,
        # "weirdSecondLimit": enums.TraderOrderType.BUY_LIMIT.value,
        cryptofeed_constants.LIMIT: enums.TraderOrderType.BUY_LIMIT.value,
        cryptofeed_constants.MARKET: enums.TraderOrderType.BUY_MARKET.value,
        cryptofeed_constants.MAKER_OR_CANCEL: enums.TraderOrderType.BUY_LIMIT.value,
    }
    TRADER_ORDER_TYPE_SELL_MAP: dict = {
        # for example:
        # "weirdLimitOrder": enums.TraderOrderType.SELL_LIMIT.value,
        # "weirdSecondLimit": enums.TraderOrderType.SELL_LIMIT.value,
        cryptofeed_constants.LIMIT: enums.TraderOrderType.SELL_LIMIT.value,
        cryptofeed_constants.MARKET: enums.TraderOrderType.SELL_MARKET.value,
        cryptofeed_constants.MAKER_OR_CANCEL: enums.TraderOrderType.SELL_LIMIT.value,
    }

    TRADE_ORDER_SIDE_MAP: dict = {
        enums.TradeOrderSide.BUY.value: enums.TradeOrderSide.BUY.value,
        enums.TradeOrderSide.SELL.value: enums.TradeOrderSide.SELL.value,
    }

    async def parse_orders(self):
        raise NotImplementedError

    async def parse_order(
        self,
        crypto_feed_order: cryptofeed_types.OrderInfo,
        check_completeness: bool = True,
    ) -> dict:
        """
        use this method to format a single order

        :param crypto_feed_order: crypto_feed_order with eventually missing data

        :param check_completeness: if true checks all attributes,
            if somethings missing it'll try to fetch it from the exchange

        :return: formatted order dict (100% complete or we raise NotImplemented)

        """
        order_dict = {
            enums.ExchangeConstantsOrderColumns.TIMESTAMP.value: 
                crypto_feed_order.timestamp,
            enums.ExchangeConstantsOrderColumns.STATUS.value: crypto_feed_order.status,
            enums.ExchangeConstantsOrderColumns.ID.value: crypto_feed_order.id,
            enums.ExchangeConstantsOrderColumns.SYMBOL.value: crypto_feed_order.symbol,
            enums.ExchangeConstantsOrderColumns.SIDE.value: crypto_feed_order.side,
            enums.ExchangeConstantsOrderColumns.TYPE.value: crypto_feed_order.type,
            enums.ExchangeConstantsOrderColumns.PRICE.value: crypto_feed_order.price,
            enums.ExchangeConstantsOrderColumns.AMOUNT.value: crypto_feed_order.amount,
            enums.ExchangeConstantsOrderColumns.REMAINING.value:
                crypto_feed_order.remaining,
        }
        return await super().parse_order(
            raw_order=order_dict, check_completeness=check_completeness
        )

    def _parse_cost(self):
        # not used for crypto_feed_order
        pass
