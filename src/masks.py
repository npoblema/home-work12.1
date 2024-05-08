def masks_card(card: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску"""
    return f"{card[:4]} {card[4:6]}** **** {card[12:]}"


def masks_account(account: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""
    return f"**{account[-4:]}"
