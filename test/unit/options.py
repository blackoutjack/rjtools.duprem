"""Unit tests for command-line option validation"""

import sys

from rjtools.util.msg import dbg
from rjtools.util.testutil import Grep

from argparse import ArgumentError

from duprem.__main__ import validate_options, load_argument_parser


def test_empty_options():
    argv = []

    parser = load_argument_parser()
    opts = parser.parse_args(argv)

    dbg(opts)

    try:
        validate_options(parser, opts)
        return False
    except (SystemExit, ArgumentError) as ex:
        return ex.code == 2

err_empty_options = Grep("error: Provide at least one directory \(or multiple "
                         "files\) to scan for duplicates")

def test_one_path_only():
    args = ["test/"]

    parser = load_argument_parser()
    opts = parser.parse_args(args)

    dbg(opts)

    try:
        validate_options(parser, opts)
        return True
    except (SystemExit, ArgumentError):
        return False

def test_two_paths():
    args = ["test/", "./another/path"]

    parser = load_argument_parser()
    opts = parser.parse_args(args)

    dbg(opts)

    try:
        validate_options(parser, opts)
        return True
    except (SystemExit, ArgumentError):
        return False

def test_force_no_remove():
    args = ["--force", "test/"]

    parser = load_argument_parser()
    opts = parser.parse_args(args)
    dbg(opts)

    try:
        validate_options(parser, opts)
        return False
    except (SystemExit, ArgumentError) as ex:
        return ex.code

err_force_no_remove = Grep("error: Cannot force removal without --remove")

