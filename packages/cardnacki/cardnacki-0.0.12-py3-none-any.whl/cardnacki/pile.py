from dataclasses import dataclass
from itertools import count
import random
from typing import Optional
from enum import Enum, auto

from .card import Card, deck_unshuffled


class PileType(Enum):
    DECK = auto()
    DISCARD = auto()
    STAGED = auto()
    HAND = auto()


@dataclass
class PileProps:
    """Dataclass that evaluates aspects of a list of cards. Can be part of a Pile or instantiated independently.
    Attributes: cards: list[Card] & the_suit: str (helpful if used in some type of trump game)
    """
    cards: list[Card]
    the_suit: str = None

    @property
    def suit_cards(self) -> list[Card]:
        """Returns cards of a self.the_suit ordered by rank_int desc"""
        return sorted([c for c in self.cards if c.suit == self.the_suit], key=lambda x: x.rank_int, reverse=True)

    @property
    def non_suit_cards(self) -> list[Card]:
        return [c for c in self.cards if c.suit != self.the_suit]

    @property
    def suit_length(self) -> int:
        return len(self.suit_cards)

    @property
    def suit_rank_ints(self) -> list[int]:
        return sorted([c.rank_int for c in self.suit_cards], reverse=True)

    def suit_length_by_ranks(self, ranks: list[int]) -> int:
        return len([c for c in self.suit_cards if c.rank_int in ranks])

    def suit_has_rank(self, rank: int) -> bool:
        """Accepts a rank (e.g. 11 for Jack), returns bool if card exists for self.the_suit"""
        return rank in self.suit_rank_ints

    @property
    def suit_highest_card(self) -> Card | None:
        return self.suit_cards[0] if self.suit_length else None

    @property
    def suit_second_highest_card(self) -> Card | None:
        return self.suit_cards[1] if self.suit_length >= 2 else None

    def has_a_non_suit_rank(self, rank: int) -> bool:
        return rank in [c.rank_int for c in self.non_suit_cards]


class Pile:
    def __init__(self, type_: PileType, owner=None, cards=None, start_shuffled=False, face_up_default=False):
        self.id_ = count().__next__
        self.type: str = type_
        self.owner: str = owner
        self.cards: list[Card] = cards if cards else []  # having cards as a mutable default argument caused errors
        self.face_up_default: bool = face_up_default
        self.pile_props: PileProps = PileProps(self.cards)
        if start_shuffled:
            self.shuffle()

    def __repr__(self):
        return f'{self.cards}'

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    @property
    def card_cnt(self) -> int:
        return len(self)

    @property
    def point_total(self) -> int:
        return sum([c.game_points for c in self])

    @property
    def top_card(self) -> Card:
        return self.cards[0]

    @property
    def bottom_card(self) -> Card:
        return self.cards[-1]

    @property
    def last_face_up_card(self) -> Optional[Card]:
        """May return None"""
        for c in self.cards[::-1]:
            if c.face_up:
                return c

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def add_card(self, card: Card, location: str = 'top', face_up: bool = None):
        self.cards.append(card) if location == 'bottom' else self.cards.insert(0, card)
        self.set_face_side(card, face_up)

    def set_face_side(self, card, face_up: bool = None):
        card.face_up = self.face_up_default if face_up is None else face_up

    def add_all_cards(self, cards: list[Card], location: str = 'top', face_up: bool = None):
        [self.cards.append(card) if location == 'bottom' else self.cards.insert(0, card) for card in cards]
        for card in cards:
            card.face_up = self.face_up_default if face_up is None else face_up

    def remove_card(self, card: Card = None, location: str = 'top'):
        if card:
            self.cards.remove(card)
        else:
            self.cards.pop() if location == 'bottom' else self.cards.pop(0)

    def remove_all_cards(self):
        self.cards.clear()

    def sort_by_rank(self, descending: bool = False):
        self.cards.sort(key=lambda card: card.rank_int, reverse=descending)

    def move_card(self, card: Card, location: str = 'top'):
        if location == 'bottom':
            self.cards.remove(card)
            self.cards.append(card)
        else:
            self.cards.remove(card)
            self.cards.insert(0, card)


def create_deck():
    return [Card(idx, *c) for idx, c in enumerate(deck_unshuffled)]


class Deck(Pile):
    def __init__(self):
        super().__init__(type_=PileType.DECK, cards=create_deck())


class Discard(Pile):
    def __init__(self):
        super().__init__(type_=PileType.DISCARD, face_up_default=True)
