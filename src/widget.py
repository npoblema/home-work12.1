from src.masks import masks_account, masks_card


def masks_of_cards(data: str) -> str:
    """
    Функция переиспользует ранее написанные функции
    и возвращает исходную строку с замаскированным номером карты/счета.fla
    """
    right_data = data.split(" ")
    if right_data[0] == "Счет":
        return f"Счет {masks_account(right_data[-1])}"
    else:
        return f'{" ".join(right_data[:-1])} {masks_card(right_data[-1])}'


def convert_datetime_to_date(datetime_string: str) -> str:
    """Функция, которая принимает строку и возвращает строку с датой"""
    date_parts = datetime_string.split("T")[0].split("-")
    return f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"

