import pytest

from utils.money import Money


def test_money_rejects_negative_amounts_and_unsupported_currencies():
    with pytest.raises(ValueError, match="negative"):
        Money(-1, "PLN")

    with pytest.raises(ValueError, match="supported"):
        Money(100, "GBP")


def test_amount_property_can_be_updated_but_not_set_negative():
    money = Money(125, "PLN")

    money.amount = 250
    assert money.amount == 250

    with pytest.raises(ValueError, match="negative"):
        money.amount = -1

    with pytest.raises(ValueError, match="delete"):
        del money.amount


def test_currency_property_rejects_unsupported_currency():
    money = Money(125, "PLN")

    with pytest.raises(ValueError, match="supported"):
        money.currency = "GBP"


def test_money_formats_as_decimal_amount_and_currency():
    assert str(Money(1234, "PLN")) == "12.34PLN"


def test_money_comparison_and_arithmetic_in_same_currency():
    first = Money(1000, "PLN")
    second = Money(750, "PLN")

    assert first == Money(1000, "PLN")
    assert second < first
    assert first < 1001
    assert first + 250 == Money(1250, "PLN")
    assert first - 250 == Money(750, "PLN")


def test_money_arithmetic_converts_other_money_to_this_currency():
    pln = Money(1000, "PLN")

    assert pln + Money(100, "PLN") == Money(1100, "PLN")
    assert pln - Money(100, "PLN") == Money(900, "PLN")


def test_money_arithmetic_rejects_results_below_zero():
    with pytest.raises(ValueError, match="negative"):
        Money(10, "PLN") - 11


def test_money_arithmetic_returns_not_implemented_for_unsupported_types():
    money = Money(10, "PLN")

    assert money.__add__("10") is NotImplemented
    assert money.__sub__("10") is NotImplemented
