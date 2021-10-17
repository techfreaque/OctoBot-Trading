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
import octobot_trading.constants as constants
import octobot_trading.errors as errors


class Asset:
    def __init__(self, name, available, total):
        self.name = name

        self.available = available
        self.total = total

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} | Available: {self.available} | Total: {self.total}"

    def update(self, available=constants.ZERO, total=constants.ZERO):
        """
        Update asset portfolio
        :param available: the available delta
        :param total: the total delta
        """
        self.available += self._ensure_update_validness(self.available, available)
        self.total += self._ensure_update_validness(self.total, total)

    def set(self, available, total):
        """
        Set available and total values for portfolio asset
        :param available: the available value
        :param total: the total value
        """
        self.available = available
        self.total = total

    def balance_available(self):
        """
        Balance available value with total
        """
        self.available = self.total

    def reset(self):
        """
        Reset asset portfolio to zero
        """
        self.set(available=constants.ZERO, total=constants.ZERO)

    def _ensure_update_validness(self, origin_quantity, update_quantity):
        """
        Ensure that the portfolio final value is not negative.
        Raise a PortfolioNegativeValueError if the final value is negative
        :param origin_quantity: the original currency value
        :param update_quantity: the update value
        :return: the updated quantity
        """
        if origin_quantity + update_quantity < constants.ZERO:
            raise errors.PortfolioNegativeValueError(f"Trying to update {self.name} with {update_quantity} "
                                                     f"but quantity was {origin_quantity}")
        return update_quantity