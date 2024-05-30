from src.logging import logger_setup
logger = logger_setup()


def masks_card(card: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску"""
    if len(card) == 16:
        logger.info("Функция masks_card выполнена успешно!")
        return f"{card[:4]} {card[4:6]}** {'*' * 4} {card[12:16]}"
    else:
        logger.error("С функцией masks_card что-то не так!")
    return card


def masks_account(account: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""
    if len(account) == 21:
        logger.info("Функция masks_account выполнена успешно!")
        return f"**{account[-4:]}"
    else:
        logger.error("С функцией masks_account что-то не так!")
    return account


masks_card("1234567891453146")
masks_account("123456789145314626093")
