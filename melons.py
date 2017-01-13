"""This file should have our order classes in it."""
from random import randint
from datetime import datetime


class AbstractMelonOrder(object):
    """Basic Melon order defined"""

    order_type = None
    tax = None

    def __init__(self, species, qty):
        """Initialize melon order attributes"""

        self.species = species
        if qty > 100:
            raise TooManyMelonsError
        self.qty = qty
        self.shipped = False

    def get_base_price(self):
        """Mel wants splurge pricing, by choosing a rand int for base price each order
        Additional $4 added for morning rush ordering
        """

        base_price = randint(5, 9)

        now = datetime.now()
        day_of_week = now.weekday()
        hour = now.hour

        if day_of_week in range(5) and hour in range(8, 12):
            base_price += 4

        return base_price

    def get_total(self):
        """Calculate price."""

        base_price = self.get_base_price()

        if self.species == "Christmas melon":
            base_price *= 1.5

        total = (1 + self.tax) * self.qty * base_price

        return total

    def mark_shipped(self):
        """Set shipped to true."""

        self.shipped = True


class GovernmentMelonOrder(AbstractMelonOrder):
    """An order from the government"""

    tax = 0
    order_type = 'government'
    passed_inspection = False

    def mark_inspection(self, passed):
        """Marks whether an order has passed inspection"""

        self.passed_inspection = passed


class DomesticMelonOrder(AbstractMelonOrder):
    """A domestic (in the US) melon order."""

    tax = 0.08
    order_type = "domestic"


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    order_type = 'international'
    tax = 0.17

    def __init__(self, species, qty, country_code):
        """Initialize melon order attributes"""

        super(InternationalMelonOrder, self).__init__(species, qty)
        self.country_code = country_code

    def get_country_code(self):
        """Return the country code."""

        return self.country_code

    def get_total(self):
        total = super(InternationalMelonOrder, self).get_total()
        if self.qty < 10:
            total += 3

        return total


class TooManyMelonsError(ValueError):

    def __init__(self):
        msg = "No more than 100 melons!"
        super(TooManyMelonsError, self).__init__(msg)
