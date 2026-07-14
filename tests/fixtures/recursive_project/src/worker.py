def countdown(value: int) -> int:
    if value <= 0:
        return 0
    return countdown(value - 1)
