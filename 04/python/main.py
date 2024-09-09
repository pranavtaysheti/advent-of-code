import fileinput
from typing import TypedDict


class CardBundle(TypedDict):
    winning_numbers: list[int]
    numbers_have: list[int]
    qty: int


def get_numbers(s: str) -> list[int]:
    return [int(n) for n in s.split()]


def winner_num(card: CardBundle) -> int:
    wns, nhs, _qty = card.values()
    return len(set(wns) & set(nhs))  # type: ignore


def calculate_score(n: int) -> int:
    if n == 0:
        return 0
    return 2 ** (n - 1)


card_set: list[CardBundle] = []
sum_p1 = 0
sum_p2 = 0

with fileinput.input(encoding="utf-8") as input_file:
    for card_str in input_file:
        card_set.append(
            {
                "winning_numbers": get_numbers(card_str[10:40]),
                "numbers_have": get_numbers(card_str[42:-1]),
                "qty": 1,
            }
        )

for i, card_bundle in enumerate(card_set):
    no_winners = winner_num(card_bundle)
    sum_p1 += calculate_score(no_winners)

    for k in range(no_winners):
        card_set[i + k + 1]["qty"] += card_bundle["qty"]

    sum_p2 += card_bundle["qty"]

print(f"P1: {sum_p1}")
print(f"P2: {sum_p2}")
