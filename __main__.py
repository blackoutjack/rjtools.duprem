'''Command-line entry point for the duprem module'''

from argparse import ArgumentParser, REMAINDER

from dgutil.msg import info, dbg, set_debug

from .duplicates import find_duplicates, handle_duplicates

def main():
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

    paths = opts.paths

    if len(paths) < 1:
        parser.error("Provide at least one directory (or multiple files) to "
            "scan for duplicates")

    if opts.debug:
        set_debug(True)
    dbg("Paths: %r" % paths)

    found = find_duplicates(paths)
    if found:
        handle_duplicates(opts.remove, opts.force)
    else:
        info("No duplicate files found.")

    return 0

if __name__ == "__main__":
    main()


