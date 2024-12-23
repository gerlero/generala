import argparse
import functools
import multiprocessing
import signal
import sys

from . import Category, categories, counts, dice, possible_held


def counts_from_str(dice_str):
    dice = tuple(int(character) for character in dice_str)

    if len(dice) != 5 or not all(1 <= d <= 6 for d in dice):
        sys.exit("Invalid value for dice")

    return counts(dice)


def counts_to_str(counts):
    if sum(counts) == 0:
        return "none"

    if sum(counts) == 5:
        return "all"

    return "".join(str(d) for d in dice(counts))


def dice_to_hold_to_str(to_hold, counts):
    if set(to_hold) == set(possible_held(counts)):
        return "any"

    return " or ".join(counts_to_str(counts) for counts in to_hold)


def interrupt_handler(signal, frame):
    print("Canceled!")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, interrupt_handler)

    parser = argparse.ArgumentParser(
        prog="generala", description="Know yout expected scores in a turn of Generala."
    )
    parser.add_argument("roll", type=int, choices=range(1, 4), help="roll number")
    parser.add_argument("dice", type=str, help="e.g. 44126")
    for category in categories.NUMBERS:
        parser.add_argument(
            f"--no-{category}",
            action="store_const",
            const=category,
            help=f"category {category} closed",
        )
    parser.add_argument(
        "-s",
        "--no-straight",
        action="store_const",
        const=categories.STRAIGHT,
        help="category Straight closed",
    )
    parser.add_argument(
        "-f",
        "--no-full-house",
        action="store_const",
        const=categories.FULL_HOUSE,
        help="category Full house closed",
    )
    parser.add_argument(
        "-p",
        "--no-four-of-a-kind",
        action="store_const",
        const=categories.FOUR_OF_A_KIND,
        help="category Four of a kind closed",
    )
    parser.add_argument(
        "-g",
        "--no-generala",
        action="store_const",
        const=categories.GENERALA,
        help="category Generala closed",
    )
    parser.add_argument(
        "-d",
        "--no-double-generala",
        action="store_const",
        const=categories.DOUBLE_GENERALA,
        help="category Double Generala closed",
    )

    args = parser.parse_args()

    open_categories = list(categories.ALL)

    closed_categories = [
        args.no_1s,
        args.no_2s,
        args.no_3s,
        args.no_4s,
        args.no_5s,
        args.no_6s,
        args.no_straight,
        args.no_full_house,
        args.no_four_of_a_kind,
        args.no_generala,
        args.no_double_generala,
    ]

    for category in closed_categories:
        if category is not None:
            open_categories.remove(category)

    c = counts_from_str(args.dice)

    with multiprocessing.Pool() as p:
        f = functools.partial(
            Category.expected_score,
            counts=c,
            roll=args.roll,
            open_categories=open_categories,
            return_held=True,
        )

        x = [*open_categories, categories.MaxScore(open_categories)]

        if args.roll == 1:
            print("Computing. This may take a few seconds....")
            results = p.imap(f, x)

        else:
            results = map(f, x)

        if args.roll != 3:
            header = False
            for category, (expected, hold) in zip(x, results):
                if not header:
                    print(
                        "{:^15}{:^15}{}".format(
                            "Category", "Expected score", "Hold dice"
                        )
                    )
                    header = True
                print(
                    f"{str(category)[:15]:^15}     {expected:>5.2f}     {dice_to_hold_to_str(hold, c)}"
                )

        else:
            print("{:^15}{:^10}".format("Category", "Score"))

            for category, (score, _) in zip(x, results):
                print(f"{str(category)[:15]:^15}   {score:>3}")
