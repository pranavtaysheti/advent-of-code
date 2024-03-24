from collections import Counter, defaultdict
from collections.abc import Callable, Iterable
from itertools import chain
from typing import NamedTuple

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARDS_J = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


class HandBid(NamedTuple):
    hand: str
    bid: int


def joker_to_best(hand: str) -> str:
    hand_count = Counter(hand.replace('J', ''))
    if len(hand_count) == 0:
        max_card = 'J'
    else:
        [(max_card, _)] = hand_count.most_common(1)
    return hand.replace("J", max_card)


def first_order_weight(hand: str) -> int:
    hand_count = Counter(hand)
    return sum(v**2 for v in hand_count.values())


def second_order_key_factory(cards: list[str]) -> Callable[[HandBid], list[int]]:
    def second_order_key(hand_bid: HandBid) -> list[int]:
        return [13 - cards.index(e) for e in hand_bid.hand]

    return second_order_key


def type_classify(
    hand_bids: list[HandBid], weight_modification: Callable[[str], str] | None = None
) -> dict[int, list[HandBid]]:
    type_classified: dict[int, list[HandBid]] = defaultdict()
    type_classified.default_factory = list

    for hand_bid in hand_bids:
        if weight_modification is not None:
            modified_hand = weight_modification(hand_bid.hand)
        else:
            modified_hand = hand_bid.hand
        type_classified[first_order_weight(modified_hand)].append(hand_bid)

    return type_classified


def ordered_handbids(type_classified: dict[int, list[HandBid]], cards: list[str]) -> Iterable[HandBid]:
    for type_hand in type_classified.values():
        type_hand.sort(key=second_order_key_factory(cards))

    return chain.from_iterable(
        type_classified[k] for k in sorted([*type_classified.keys()])
    )


def solve(hand_bids: Iterable[HandBid]) -> int:
    return sum(
        (i + 1) * bid for i, bid in enumerate(hand_bid.bid for hand_bid in hand_bids)
    )

def main():
    with open("input.txt") as input_file:
        input = [HandBid(hand, int(bid)) for hand, bid in (line.split() for line in input_file)]

    p1_sol = solve(ordered_handbids(type_classify(input), CARDS))
    p2_sol = solve(
        ordered_handbids(type_classify(input, joker_to_best), CARDS_J)
    )
    print(f"P1: {p1_sol}")
    print(f"P2: {p2_sol}")

if __name__ == "__main__":
    main()
