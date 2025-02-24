"""
Duplicate file detection and removal

This program contains some Linux-specific logic, so using on Windows is not
recommended.
"""

import sys

from rjtools.util.msg import info

from rjtools.duprem.opts import load_options
from rjtools.duprem.engine import DupEngine

def run(opts, plugins):
    """
    Find duplicate files within the provide paths, and list sets of duplicate
    files, optionally deleting certain copies.

    :param opts: argparse.Namespace:
    :param plugins: list of ModuleType:
    """
    engine = DupEngine(plugins)
    found = engine.find_duplicates(opts.paths, opts.doHidden, opts.doEmpty, opts.threads)
    if found:
        engine.handle_duplicates(opts.remove, opts.force)
    else:
        info("No duplicate files found.")

    return 0

def main():
    opts, plugins = load_options()

    sys.exit(run(opts, plugins))

if __name__ == "__main__":
    main()

