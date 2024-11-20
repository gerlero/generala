# 🎲 generala

[![CI](https://github.com/gerlero/generala/actions/workflows/ci.yml/badge.svg)](https://github.com/gerlero/generala/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Publish](https://github.com/gerlero/generala/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/gerlero/generala/actions/workflows/pypi-publish.yml)
[![PyPI](https://img.shields.io/pypi/v/generala)](https://pypi.org/project/generala/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/generala)](https://pypi.org/project/generala/)

**generala** is a probabilistic tool for the [dice game of Generala](https://en.wikipedia.org/wiki/Generala).

**generala** helps you decide which dice to hold after each roll. Starting from the dice you have, the tool considers all possible future rolls to find which combinations of held dice give the best expected scores for the different categories. While written in pure Python—which is not at all efficient for these kinds of tasks—, it uses multiprocessing to lower the computation times to just a few seconds per invocation at the most.

The categories and scores in the tool correspond to the variant of the game played in my family. As there are many variants of the game—each of which assigns scores to the categories differently—you may want to check out the ```generala.categories``` module and modify it as desired.

## Installation

**generala** is available as a [Python package on PyPI](https://pypi.org/project/generala). Assuming you have Python 3.9 or later, install it by running the command:

```bash
$ pip install generala
```

or:

```bash
$ python3 -m pip install generala
```

## Usage

### Command-line usage

Suppose we got the dice (4,4,1,2,6) on the first roll in a game. Run **generala** as:

```bash
$ generala 1 44126
```

or, alternatively:

```bash
$ python3 -m generala 1 44126
```

The program responds with the best expected scores for each category. The third column ("Hold dice") tells us which dice we should hold for the expected score to apply. The final row ("any") looks to maximize the overall expected score irrespective of category.

```
Computing. This may take a few seconds....
   Category    Expected score Hold dice
      1s             2.22     1
      2s             4.44     2
      3s             4.58     none
      4s            11.67     44
      5s             7.64     none
      6s            13.33     6
   Straight          5.52     24
  Full house        13.47     44
Four of a kind      17.18     44
   Generala          2.91     44
Double Generala      0.00     any
      any           33.15     44
```

Let's say we kept (4,4) and got (5,4,3) on the second roll. We run **generala** again:

```bash
$ generala 2 44543
```

The tool outputs:

```
   Category    Expected score Hold dice
      1s             0.83     none
      2s             1.67     none
      3s             5.00     3
      4s            13.33     444
      5s             8.33     5
      6s             5.00     none
   Straight          3.33     345
  Full house         8.33     4445 or 3444
Four of a kind      22.22     444
   Generala          2.78     444
Double Generala      0.00     any
      any           38.61     444
```

After the third and final roll, the tool can give the final scores. Assuming we have the dice (4,4,4,3,2):

```bash
$ generala 3 44432
```

```
   Category      Score   
      1s            0
      2s            2
      3s            3
      4s           12
      5s            0
      6s            0
   Straight         0
  Full house        0
Four of a kind      0
   Generala         0
Double Generala     0
      any          12
```

#### Closed categories

You can also specify, via options, which categories are closed (i.e., no longer available for scoring). For example, with:

```bash
$ generala -46fpg 1 44126
```

we tell the tool that the categories 4s, 6s, Full house, Four of a kind, and Generala are closed—which results in those categories not being considered in the computation:

```
   Category    Expected score Hold dice
      1s             2.22     1
      2s             4.44     2
      3s             4.58     none
      5s             7.64     none
   Straight          5.52     24
Double Generala      5.81     44
      any           12.00     44
```

For a list of all available options, run:

```bash
$ generala --help
```

### As a Python library

It is also possible to call into the functionality from a Python program. Here's an example.

```python
from generala import expected_score, counts, dice
from generala.categories import straight, all_categories

c = counts((4,4,1,2,6))

score, held = expected_score(category=straight, counts=c, roll=1, open_categories=all_categories, return_held=True)

print("Hold dice {}. Expected score: {:.2f}".format(dice(held[0]), score))

```

When run, that snippet will print:

```
Hold dice (2, 4). Expected score: 5.52
```

That's all. Good luck!