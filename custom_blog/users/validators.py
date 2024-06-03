import string


def correct_username(value: str) -> None:
    correct = string.ascii_letters + '@/./+/-/_.' + string.digits
    symbols = set(value)
    return any([symbol not in correct for symbol in symbols])
