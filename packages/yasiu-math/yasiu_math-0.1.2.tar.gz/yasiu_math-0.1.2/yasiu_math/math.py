import numpy as np


def round_number(number, round=5):
    """
    Round number to fit number in character limit.

    Args:
        number:
        round:

    Returns:

    """
    power = round - 2
    rnd = 0
    num = None

    while power >= 0:
        high = 10 ** power
        if number >= high:
            num = np.round(number, rnd)
            break

        power -= 1
        rnd += 1

    if num is None:
        num = np.round(number, round - 2)

    if rnd == 0:
        num = int(num)

    return num


__all__ = [
    "round_number"
]

if __name__ == "__main__":
    num = 3.3535123
    for i in range(1, 6):
        print(i, round_number(num, i))
