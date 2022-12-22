import octobot_trading.exchanges.parser as parser


class CCXTTradesParser(parser.TradesParser, parser.CCXTOrdersParser):
    """
    override CCXTTradesParser if you add support for a CCXT exchange
    dont use GenericCCXTTradesParser as a base

        parser usage:   parser = TradesParser(exchange)
                        trades = await parser.parse_trades(raw_trades)
                        trade = await parser.parse_trade(raw_trade)
    """

    def __init__(
        self,
        exchange,
        parser_type_name: str = "trades",
    ):
        super().__init__(
            exchange=exchange,
            parser_type_name=parser_type_name,
        )
