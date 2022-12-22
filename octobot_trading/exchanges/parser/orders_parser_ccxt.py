import octobot_trading.enums as enums
import octobot_trading.exchanges.parser.orders_parser as orders_parser


class CCXTOrdersParser(orders_parser.OrdersParser):
    """
    override CCXTOrdersParser if you add support for a CCXT exchange
    dont use GenericCCXTOrdersParser as a base

    parser usage:   parser = CCXTOrdersParser(exchange)
                    orders = await parser.parse_orders(raw_orders)
                    order = await parser.parse_order(raw_order)
    """

    TIMESTAMP_KEYS: list = [enums.ExchangeOrderCCXTColumns.TIMESTAMP.value]
    STATUS_KEYS: list = [enums.ExchangeOrderCCXTColumns.STATUS.value]
    ID_KEYS: list = [enums.ExchangeOrderCCXTColumns.ID.value]
    SYMBOL_KEYS: list = [enums.ExchangeOrderCCXTColumns.SYMBOL.value]
    SIDE_KEYS: list = [enums.ExchangeOrderCCXTColumns.SIDE.value]
    TYPE_KEYS: list = [enums.ExchangeOrderCCXTColumns.TYPE.value]
    TAKER_OR_MAKER_KEYS: list = [enums.ExchangeOrderCCXTColumns.TAKER_OR_MAKER.value]
    PRICE_KEYS: list = [
        # first try average as its more accurate
        enums.ExchangeOrderCCXTColumns.AVERAGE.value,  
        enums.ExchangeOrderCCXTColumns.PRICE.value,
    ]
    FILLED_PRICE_KEYS: list = [enums.ExchangeOrderCCXTColumns.AVERAGE.value]
    AMOUNT_KEYS: list = [enums.ExchangeOrderCCXTColumns.AMOUNT.value]
    REMAINING_KEYS: list = [enums.ExchangeOrderCCXTColumns.REMAINING.value]
    FILLED_AMOUNT_KEYS: list = [enums.ExchangeOrderCCXTColumns.FILLED.value]
    COST_KEYS: list = [enums.ExchangeOrderCCXTColumns.COST.value]
    REDUCE_ONLY_KEYS: list = [enums.ExchangeOrderCCXTColumns.REDUCE_ONLY.value]
    TIME_IN_FORCE_KEYS: list = []
    TAG_KEYS: list = [enums.ExchangeOrderCCXTColumns.TAG.value]
    FEE_KEYS: list = [enums.ExchangeOrderCCXTColumns.FEE, 
                      enums.ExchangeOrderCCXTColumns.FEES.value]
    QUANTITY_CURRENCY_KEYS: list = [
        enums.ExchangeOrderCCXTColumns.QUANTITY_CURRENCY.value]

    def __init__(
        self,
        exchange,
        parser_type_name: str = "orders",
    ):
        super().__init__(
            exchange=exchange,
            parser_type_name=parser_type_name,
        )
