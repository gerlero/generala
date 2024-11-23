import abc
import functools
from collections import Counter
from itertools import chain, product, repeat
from operator import add

import numpy as np

__version__ = "2.0.0"


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

    def expected_score(self, counts, roll, open_categories, *, return_held=False):
        if roll == 3:
            score = self.score(counts, roll, open_categories)

            if return_held:
                return score, []
            return score

        max_expected = -np.inf

        if return_held:
            best_held = []

        for held in possible_held(counts):
            num_held = sum(held)

            if num_held == 5:
                expected = self.score(counts, roll, open_categories)

            elif roll == 2:
                new = np.array(list(possible_new(5 - num_held).keys()))
                weights = np.array(list(possible_new(5 - num_held).values()))

                expected = np.dot(
                    weights, self.expected_score(held + new, 3, open_categories)
                ) / np.sum(weights)

            else:
                cum_weighted_expected = 0
                cum_weight = 0

                for new, weight in possible_new(5 - num_held).items():
                    c = tuple(map(add, held, new))

                    cum_weighted_expected += weight * self.expected_score(
                        c, roll + 1, open_categories
                    )
                    cum_weight += weight

                expected = cum_weighted_expected / cum_weight

            if return_held and np.isclose(expected, max_expected):
                best_held.append(held)

            elif expected > max_expected:
                max_expected = expected
                if return_held:
                    best_held = [held]

        if return_held:
            return max_expected, best_held

        return max_expected


def possible_held(counts):
    return product(*(range(count + 1) for count in counts))


@functools.lru_cache(maxsize=6)
def possible_new(num_new):
    return Counter(
        tuple(counts(dice)) for dice in product((1, 2, 3, 4, 5, 6), repeat=num_new)
    )
