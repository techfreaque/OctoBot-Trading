from octobot_trading.enums import ExchangeConstantsFundingColumns as FundingCols
from octobot_trading.exchanges import parser


class CCXTFundingRateParser(parser.FundingRateParser):
    """
    override CCXTFundingRateParser class if necessary

    only include code according to ccxt standards

        parser usage:   parser = FundingRateParser(exchange)
                        funding_rate = parser.parse_funding_rate(raw_funding_rate)
                        funding_rates = parser.parse_funding_rates(raw_funding_rates)
    """

    TIMESTAMP_KEYS: list = [FundingCols.TIMESTAMP.value]
    SYMBOL_KEYS: list = [FundingCols.SYMBOL.value]
    FUNDING_RATE_KEYS: list = [FundingCols.FUNDING_RATE.value]
    PREDICTED_FUNDING_RATE_KEYS: list = [FundingCols.PREDICTED_FUNDING_RATE.value]
    NEXT_FUNDING_TIME_KEYS: list = [FundingCols.NEXT_FUNDING_TIME.value]
    LAST_FUNDING_TIME_KEYS: list = [FundingCols.LAST_FUNDING_TIME.value]
