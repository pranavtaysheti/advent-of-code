from collections import Counter, defaultdict
from itertools import chain
from typing import NamedTuple


class HandBid(NamedTuple):
    hand: str
    bid: int


cards = [*reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"])]


def first_order_weight(hand: str) -> int:
    count = Counter(hand)
    return sum(v**2 for v in count.values())


def second_order_key(hand_bid: HandBid) -> list[int]:
    return [cards.index(e) for e in hand_bid.hand]


if __name__ == "__main__":
    input: list[HandBid] = []
    p1_sol = 0
    p2_sol = 0

    type_classified: dict[int, list[HandBid]] = defaultdict()
    type_classified.default_factory = list[HandBid]

    with open("input.txt") as input_file:
        for line in input_file:
            hand, bid = line.split()
            input.append(HandBid(hand, int(bid)))

    for hand_bid in input:
        type_classified[first_order_weight(hand_bid.hand)].append(hand_bid)

    for type_hand in type_classified.values():
        type_hand.sort(key=second_order_key)

    ordered_handbids = chain.from_iterable(
        type_classified[k] for k in sorted([*type_classified.keys()])
    )

    for i,bid in enumerate(hand_bid.bid for hand_bid in ordered_handbids):
        p1_sol += (i+1)*bid

    print(f"P1: {p1_sol}")
    print(f"P2: {p2_sol}")
