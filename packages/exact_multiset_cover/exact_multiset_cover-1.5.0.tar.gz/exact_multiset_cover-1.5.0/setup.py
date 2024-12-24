# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exact_multiset_cover']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=51.1.2']

extras_require = \
{':python_version == "3.10"': ['numpy>=1.21'],
 ':python_version == "3.11"': ['numpy>=1.23'],
 ':python_version == "3.7"': ['numpy>=1.14'],
 ':python_version == "3.8"': ['numpy>=1.17'],
 ':python_version == "3.9"': ['numpy>=1.19'],
 ':python_version >= "3.12"': ['numpy>=1.24']}

entry_points = \
{'console_scripts': ['debug = tools.debug:run_debug',
                     'doctest = tools.run_tests:run_doctest',
                     'parse_valgrind = tools.debug:parse_valgrind_results',
                     'quicktest = tools.run_tests:quicktest',
                     'test = tools.run_tests:test']}

setup_kwargs = {
    'name': 'exact_multiset_cover',
    'version': '1.5.0',
    'description': 'Solve exact cover problems for multisets. Fork of exact_cover',
    'long_description': 'Finding Exact Covers in NumPy for Multisets\n===========================================\n\n[![PyPI version](https://badge.fury.io/py/exact-multiset-cover.svg)](https://badge.fury.io/py/exact-multiset-cover)\n![Deploy wheels to pypi](https://github.com/questforwisdom/exact_multiset_cover/workflows/Deploy%20wheels%20to%20pypi/badge.svg)\n![Run Python tests](https://github.com/questforwisdom/exact_multiset_cover/workflows/Run%20Python%20tests/badge.svg)\n\nThis is a Python 3 package to solve exact cover problems using Numpy. It is based on https://github.com/moygit/exact_cover_np by Moy Easwaran. Jack Grahl ported it to Python 3, fixed some bugs and made lots of small improvements to the packaging. Niklas Zapatka extended to algorithm to multisets.\n\nThe original package by Moy was designed to solve sudoku. Now this package is only designed to solve exact cover problems given as byte arrays. The number in each cell states the multiplicity of the respective elementin the multiset. It can be used to solve sudoku and a variety of combinatorial problems. However the code to reduce a sudoku to an exact cover problem is no longer part of this project. It can be found at:\n - https://pypi.org/project/xudoku/\n - https://github.com/jwg4/xudoku\n\nAnother project, \'polyomino\' by Jack Grahl uses this algorithm to solve polyomino tiling problems. It can be found at:\n - https://pypi.org/project/polyomino/\n - https://github.com/jwg4/polyomino\n\nSummary\n-------\n\nThe exact cover problem is as follows: given a set X and a\ncollection S of subsets of X, we want to find a subcollection S*\nof S that is an exact cover or partition of X.  In other words,\nS* is a bunch of subsets of X whose union is X, and which have\nempty intersection with each other.  (Example below; more details [on\nwikipedia](https://en.wikipedia.org/wiki/Exact_cover).)\n\nThis NumPy module uses Donald Knuth\'s Algorithm X\n(also known as Dancing Links) to find\nexact covers of sets.\nFor details on Algorithm X please see either\n[the Wikipedia page](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X)\nor [Knuth\'s paper](http://arxiv.org/pdf/cs/0011047v1).\nSpecifically, we use the Knuth/Hitotsumatsu/Noshita method of\nDancing Links for efficient backtracking.  Please see\n[Knuth\'s paper](http://arxiv.org/pdf/cs/0011047v1)\nfor details.\n\nThis fork extends the algorithm such that X and the sets in S\nare multisets (also known as bags). For instance, if X contains the\nelement _a_ two times, a solution must include either exactly one set\ncontaining _a_ twice or exactly two sets containing _a_ once. \n\nHow to Use It\n-------------\n\nSuppose X = {0,1,2,3,4}, and suppose S = {A,B,C,D}, where\n\n    A = {0, 3}\n    B = {0, 1, 2}\n    C = {1, 2}\n    D = {4}.\n\nHere we can just eyeball these sets and conclude that S* = {A,C,D} forms an\nexact cover: each element of X is in one of these sets (i.e. is\n"covered" by one of these sets), and no element of X is in more than\none.\n\nWe\'d use `exact_multiset_cover` to solve the problem as follows:\nusing 1 to denote that a particular member of X is in a subset and 0 to\ndenote that it\'s not, we can represent the sets as\n\n    A = 1,0,0,1,0    # The 0th and 3rd entries are 1 since 0 and 3 are in A; the rest are 0.\n    B = 1,1,1,0,0    # The 0th, 1st, and 2nd entries are 1, and the rest are 0,\n    C = 0,1,1,0,0    # etc.\n    D = 0,0,0,0,1\n\nNow we can call `exact_multiset_cover`:\n\n    >>> import numpy as np\n    >>> import exact_multiset_cover as ec\n    >>> S = np.array([[1,0,0,1,0],[1,1,1,0,0],[0,1,1,0,0],[0,0,0,0,1]], dtype=bool)\n    >>> print(ec.get_exact_cover(S))\n    [0 2 3]\n\nThis is telling us that the 0th row (i.e. A), the 2nd row (i.e. C),\nand the 3rd row (i.e. D) together form an exact cover.\n\nTo see the total number of distinct solutions, we can use the function get_solution_count:\n\n    >>> ec.get_solution_count(S)\n    1\n\nSee the file examples.md for more detailed examples of use.\n\n\nImplementation Overview\n-----------------------\n\nThe NumPy module (`exact_cover`) is implemented in four pieces:\n\n- The lowest level is `quad_linked_list`, which implements a circular\n  linked-list with left-, right-, up-, and down-links.\n- This is used in `sparse_matrix` to implement the type of sparse\n  representation of matrices that Knuth describes in his paper (in\n  brief, each column contains all its non-zero entries, and each\n  non-zero cell also points to the (horizontally) next non-zero cell\n  in either direction).\n- Sparse matrices are used in `dlx` to implement Knuth\'s Dancing\n  Links version of his Algorithm X, which calculates exact covers.\n- `exact_cover` provides the glue code letting us invoke\n  `dlx` on NumPy arrays.\n\nThe package now has some pure Python modules for helper functions, with the main algorithm in the C-only package `exact_cover_impl`.\n\nHow to develop\n--------------\n\nThe package uses poetry and most of the setup for development uses that tool.\n\nTo install locally (as an editable package):\n`poetry install`\n\nTo build:\n`poetry build`\n\nTo run tests:\n`poetry run test` or `poetry run doctest`\n\nTo open a Python shell with the package available:\n`poetry run python`\n\nThe exception is running the C unit tests:\n`make c_tests`\n\nRepository\n----------\n\n- build/ The location where files are built.\n- dist/ The location for fully prepared files.\n- exact_multiset_cover/ The Python code.\n- obj/ Where the compiled C code is going to be output.\n- src/ The C sources.\n- tests/ Tests for both the Python package and the C code.\n- tools/ Code used in analysing and working with the library. This is not distributed with the package.\n\nAcknowledgements\n----------------\n\nThanks very much to Moy Easwaran (https://github.com/moygit) for his inspiring work!\n\nThanks to Jack Grahl for porting this to Python 3 and improving the code!\n\nMunit aka µnit (https://nemequ.github.io/munit/) is a wonderful unit testing framework for C code.\n',
    'author': 'Moy Easwaran',
    'author_email': 'None',
    'maintainer': 'Jack Grahl',
    'maintainer_email': 'jack.grahl@gmail.com',
    'url': 'https://github.com/questforwisdom/exact_multiset_cover',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
