from src.masks import masks_account, masks_card


def masks_of_cards(data: str) -> str:
    """
    The function reuses previously written functions
    and returns the original string with the masked card/account number.fla
    """
    right_data = data.split(" ")
    if right_data[0] == "Счет":
        return f"Счет {masks_account(right_data[-1])}"
    else:
        return f'{" ".join(right_data[:-1])} {masks_card(right_data[-1])}'


def convert_datetime_to_date(datetime_string: str) -> str:
    """A function that accepts a string and returns a string with a date"""
    date_parts = datetime_string.split("T")[0].split("-")
    return f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
