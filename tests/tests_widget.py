import pytest
from src.widget import get_new_type_of_date, mask_card_or_account_number


@pytest.fixture
def card_number() -> list:
    return [
        ("Visa Platinum 7000 7922 8960 6361", "Visa Platinum 7000 7922 8960 6361 ** **** 6361"),
        ("Maestro 7000 7922 8960 6361", "Maestro 7000 7922 8960 6361 ** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ]


@pytest.fixture
def date_string() -> list:
    return [
        ("2018-07-11T02:26:18.671407", "11.07.2018"),
        ("2019-07-11T02:26:18.671407", "11.07.2019"),
        ("2019-10-11T02:26:18.671407", "11.10.2019"),
    ]


def test_masks_of_cards() -> None:
    assert mask_card_or_account_number("Visa 7000 7922 8960 6361") == "Visa 7000 7922 8960 6361 ** **** "
    assert mask_card_or_account_number("Maestro 7000 7922 8960 6361") == "Maestro 7000 7922 8960 6361 ** **** "
    assert mask_card_or_account_number("Счет 73654108430135874305") == "Счет **4305"


def test_convert_datetime_to_date() -> None:
    assert get_new_type_of_date("2018-07-11T02:26:18.671407") == "11.07.2018"
    assert get_new_type_of_date("2019-07-11T02:26:18.671407") == "11.07.2019"
    assert get_new_type_of_date("2019-10-11T02:26:18.671407") == "11.10.2019"


if __name__ == "__main__":
    pytest.main()
    test_masks_of_cards()
    test_convert_datetime_to_date()
