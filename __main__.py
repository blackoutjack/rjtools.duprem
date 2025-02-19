"""Duplicate file detection and removal"""

import sys
from argparse import ArgumentParser, REMAINDER

from dgutil.msg import info, dbg, set_debug

from duprem.dup_engine import DupEngine

def validate_options(parser, opts):

    if len(opts.paths) < 1:
        parser.error(
            "Provide at least one directory (or multiple files) to scan for "
            "duplicates")
    dbg("Paths: %r" % opts.paths)

    if opts.force and not opts.remove:
        parser.error("Cannot force removal without --remove")


def load_options():
    parser = ArgumentParser()
    parser.add_argument("paths", nargs=REMAINDER, metavar="PATHS...")
    parser.add_argument("-f", "--force", dest="force", action="store_true",
        help="With --remove, force removal of all but the first copy of "
            "duplicate content.")
    parser.add_argument("-g", "--debug", dest="debug", action="store_true",
        help="Enable debug output")
    parser.add_argument("-r", "--remove", dest="remove", action="store_true",
        help="Give the user the option to remove duplicate files.")

    opts = parser.parse_args()

    if opts.debug:
        set_debug(True)

    validate_options(parser, opts)

    return opts

def run(opts):
    engine = DupEngine()
    found = engine.find_duplicates(opts.paths)
    if found:
        engine.handle_duplicates(opts.remove, opts.force)
    else:
        info("No duplicate files found.")

    return 0

def main():
    opts = load_options()

    sys.exit(run(opts))

if __name__ == "__main__":
    main()

