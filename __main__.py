
import os
from optparse import OptionParser

from util.msg import info

from .file import find_duplicates_in_dir, handle_duplicates

from .file import main

def main():
    parser = OptionParser(usage="python3 -m duprem [-rfg] DIR")
    parser.add_option(
        "-g", "--debug", dest="debug", action="store_true",
        help="Enable debug output")
    parser.add_option(
        "-r", "--remove", dest="remove", action="store_true",
        help="Give the user the option to remove duplicate files.")
    parser.add_option(
        "-f", "--force", dest="force", action="store_true",
        help="With \"remove\", force removal of all but the first copy of duplicate content.")
    opts, args = parser.parse_args()
    if len(args) < 1:
        parser.error(
            """Provide at least one directory (or multiple files) to \
scan for duplicates""")

    set_debug(opts.debug)
    dbg("Arguments: %r" % args)

    found = find_duplicates(args)
    if found:
        handle_duplicates(opts.remove, opts.force)
    else:
        info("No duplicate files found.")

    return 0

if __name__ == "__main__":
    main()


