from octobot_trading.enums import ExchangeConstantsFundingColumns as FundingCols
from octobot_trading.exchanges import parser
from octobot_commons import constants as commons_constants


class GenericCCXTFundingRateParser(parser.CCXTFundingRateParser):
    """
    dont override this class, use CCXTFundingRateParser as abase instead

    only include code that is safe for any ccxt exchange

        parser usage:   parser = GenericCCXTFundingRateParser(exchange)
                        funding_rate = parser.parse_funding_rate(raw_funding_rate)
                        funding_rates = parser.parse_funding_rates(raw_funding_rates)
    """

    FUNDING_TIME_UPDATE_PERIOD: int = 8 * commons_constants.HOURS_TO_SECONDS

    TIMESTAMP_KEYS: list = [FundingCols.TIMESTAMP.value]
    SYMBOL_KEYS: list = [FundingCols.SYMBOL.value]
    FUNDING_RATE_KEYS: list = [FundingCols.FUNDING_RATE.value, "fundingRate"]
    PREDICTED_FUNDING_RATE_KEYS: list = [FundingCols.PREDICTED_FUNDING_RATE.value]
    NEXT_FUNDING_TIME_KEYS: list = [
        FundingCols.NEXT_FUNDING_TIME.value,
        "nextFundingTime",
    ]
    LAST_FUNDING_TIME_KEYS: list = [FundingCols.LAST_FUNDING_TIME.value, "fundingTime"]

    USE_INFO_SUB_DICT_FOR_FUNDING_RATE: bool = True
    USE_INFO_SUB_DICT_FOR_PREDICTED_FUNDING_RATE: bool = True
    USE_INFO_SUB_DICT_FOR_NEXT_FUNDING_TIME: bool = True
    USE_INFO_SUB_DICT_FOR_LAST_FUNDING_TIME: bool = True
