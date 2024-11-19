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


class Straight(MajorHand):
    def score(self, counts, roll, open_categories):
        if counts[1:-1] == (1, 1, 1, 1):
            if roll == 1:
                return self._score + self._first_roll_bonus
            return self._score
        return 0

    def __str__(self):
        return "Straight"


class FullHouse(MajorHand):
    def score(self, counts, roll, open_categories):
        if 3 in counts and 2 in counts:
            if roll == 1:
                return self._score + self._first_roll_bonus
            return self._score
        return 0

    def __str__(self):
        return "Full house"


class FourOfAKind(MajorHand):
    def score(self, counts, roll, open_categories):
        if 4 in counts:
            if roll == 1:
                return self._score + self._first_roll_bonus
            return self._score
        return 0

    def __str__(self):
        return "Four of a kind"


class Generala(MajorHand):
    def score(self, counts, roll, open_categories):
        if 5 in counts:
            if roll == 1:
                return self._score + self._first_roll_bonus
            return self._score
        return 0

    def __str__(self):
        return "Generala"


class DoubleGenerala(MajorHand):
    def __init__(self, score, first_roll_bonus, generala):
        super().__init__(score, first_roll_bonus)
        self._generala = generala

    def score(self, counts, roll, open_categories):
        if self._generala not in open_categories and 5 in counts:
            if roll == 1:
                return self._score + self._first_roll_bonus
            return self._score
        return 0

    def __str__(self):
        return "Double Generala"


numbers = tuple(Number(n) for n in range(1, 7))

ones, twos, threes, fours, fives, sixes = numbers

straight = Straight(score=30, first_roll_bonus=10)
full_house = FullHouse(score=50, first_roll_bonus=10)
four_of_a_kind = FourOfAKind(score=80, first_roll_bonus=10)
generala = Generala(score=100, first_roll_bonus=math.inf)
double_generala = DoubleGenerala(
    score=200, first_roll_bonus=math.inf, generala=generala
)

all_categories = (
    *numbers,
    straight,
    full_house,
    four_of_a_kind,
    generala,
    double_generala,
)


class MaxScore(Category):
    def __init__(self, categories):
        self._categories = categories

    def score(self, counts, roll, open_categories):
        return max(cat.score(counts, roll, open_categories) for cat in self._categories)

    def __str__(self):
        return "any"
