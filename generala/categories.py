import abc
import math

from generala import Category


class Number(Category):
    def __init__(self, n):
        self._n = n

    def score(self, counts, roll, open_categories):
        return self._n * counts[self._n - 1]

    def __str__(self):
        return f"{self._n}s"


class MajorHand(Category):
    def __init__(self, score, first_roll_bonus):
        self._score = score
        self._first_roll_bonus = first_roll_bonus

    def score(self, counts, roll, open_categories):
        if self._is_valid(counts, open_categories):
            if roll == 1:
                return self._score + self._first_roll_bonus
            return self._score
        return 0

    @abc.abstractmethod
    def _is_valid(self, counts, open_categories):
        raise NotImplementedError


class Straight(MajorHand):
    def _is_valid(self, counts, open_categories):
        return counts[1:-1] == (1, 1, 1, 1)

    def __str__(self):
        return "Straight"


class FullHouse(MajorHand):
    def _is_valid(self, counts, open_categories):
        return 3 in counts and 2 in counts

    def __str__(self):
        return "Full house"


class FourOfAKind(MajorHand):
    def _is_valid(self, counts, open_categories):
        return 4 in counts

    def __str__(self):
        return "Four of a kind"


class Generala(MajorHand):
    def _is_valid(self, counts, open_categories):
        return 5 in counts

    def __str__(self):
        return "Generala"


class DoubleGenerala(MajorHand):
    def __init__(self, score, first_roll_bonus, generala):
        super().__init__(score, first_roll_bonus)
        self._generala = generala

    def _is_valid(self, counts, open_categories):
        return 5 in counts and self._generala not in open_categories

    def __str__(self):
        return "Double Generala"


NUMBERS = tuple(Number(n) for n in range(1, 7))

ONES, TWOS, THREES, FOURS, FIVES, SIXES = NUMBERS

STRAIGHT = Straight(score=30, first_roll_bonus=10)
FULL_HOUSE = FullHouse(score=50, first_roll_bonus=10)
FOUR_OF_A_KIND = FourOfAKind(score=80, first_roll_bonus=10)
GENERALA = Generala(score=100, first_roll_bonus=math.inf)
DOUBLE_GENERALA = DoubleGenerala(
    score=200, first_roll_bonus=math.inf, generala=GENERALA
)

ALL = (
    *NUMBERS,
    STRAIGHT,
    FULL_HOUSE,
    FOUR_OF_A_KIND,
    GENERALA,
    DOUBLE_GENERALA,
)


class MaxScore(Category):
    def __init__(self, categories):
        self._categories = categories

    def score(self, counts, roll, open_categories):
        return max(cat.score(counts, roll, open_categories) for cat in self._categories)

    def __str__(self):
        return "any"


MAX_SCORE = MaxScore(ALL)
