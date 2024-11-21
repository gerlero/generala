import abc
import functools
import math
from collections import Counter
from itertools import chain, product, repeat
from operator import add

__version__ = "1.1.0"


def counts(dice):
    counts = [0, 0, 0, 0, 0, 0]

    for die in dice:
        counts[die - 1] += 1

    return tuple(counts)


def dice(counts):
    return tuple(chain(*(repeat(n, c) for n, c in enumerate(counts, start=1))))


class Category(abc.ABC):
    @abc.abstractmethod
    def score(self, counts, roll, open_categories):
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError


def possible_held(counts):
    return product(*(range(count + 1) for count in counts))


@functools.lru_cache(maxsize=6)
def possible_new(num_new):
    return Counter(
        tuple(counts(dice)) for dice in product((1, 2, 3, 4, 5, 6), repeat=num_new)
    )


def expected_score(category, counts, roll, open_categories, *, return_held=False):
    if roll == 3:
        score = category.score(counts, roll, open_categories)

        if return_held:
            return score, []
        return score

    max_expected = -math.inf

    if return_held:
        best_held = []

    for held in possible_held(counts):
        num_held = sum(held)

        if num_held == 5:
            expected = category.score(counts, roll, open_categories)

        else:
            cum_weighted_expected = 0
            cum_weight = 0

            for new, weight in possible_new(5 - num_held).items():
                c = tuple(map(add, held, new))

                cum_weighted_expected += weight * expected_score(
                    category, c, roll + 1, open_categories
                )
                cum_weight += weight

            expected = cum_weighted_expected / cum_weight

        if return_held and math.isclose(expected, max_expected):
            best_held.append(held)

        elif expected > max_expected:
            max_expected = expected
            if return_held:
                best_held = [held]

    if return_held:
        return max_expected, best_held

    return max_expected
