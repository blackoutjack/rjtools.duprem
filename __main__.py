"""
Duplicate file detection and removal

This program contains some Linux-specific logic, so using on Windows is not
recommended.
"""

import sys
import importlib

from argparse import ArgumentParser, REMAINDER
from dgutil.msg import info, err, dbg, set_debug
from dgutil.fs import is_root

from duprem.engine import DupEngine, DEFAULT_THREADS

def validate_options(parser, opts):

    if len(opts.paths) < 1:
        parser.error(
            "Provide at least one directory (or multiple files) to scan for "
            "duplicates")
    dbg("Paths: %r" % opts.paths)

    if opts.threads is not None:
        try:
            threads = int(opts.threads)
            if threads < 1 or threads > 16:
                parser.error("Threads should be 1 to 16")
            opts.threads = threads
        except ValueError as ex:
            parser.error("Value of --threads must be an integer")

    if opts.force:
        if not opts.remove:
            parser.error("Cannot force removal without --remove")
        if platform.system() == 'Windows':
            parser.error(
                "duprem has not been tested on Windows, --force not allowed")
        if any([is_root(path) for path in opts.paths]):
            parser.error(
                "not allowing --force when paths include filesystem root")

def load_plugins(parser, opts):
    loadedPlugins = []
    for plugin in opts.plugins:
        try:
            plugin = importlib.import_module(f"duprem.plugin.{plugin}")
            if not hasattr(plugin, "can_handle"):
                parser.error(f"Plugin {plugin} does not implement can_handle")
            if not hasattr(plugin, "load_file"):
                parser.error(f"Plugin {plugin} does not implement load_file")
            loadedPlugins.append(plugin)
        except ImportError:
            parser.error(f"Unable to load plugin {plugin}")
    return loadedPlugins

def load_options():
    parser = ArgumentParser()
    parser.add_argument("paths", nargs=REMAINDER, metavar="PATHS...")
    parser.add_argument("-f", "--force", dest="force", action="store_true",
        help="With --remove, force removal of all but the first copy of "
            "duplicate content without asking.")
    parser.add_argument("-g", "--debug", dest="debug", action="store_true",
        help="Enable debug output")
    parser.add_argument("-p", "--plugin", dest="plugins", action="append",
        default=[], help="File types (defined in [duprem]/plugin) to use for "
            "special duplicate detection logic")
    parser.add_argument("-r", "--remove", dest="remove", action="store_true",
        help="Give the user the option to remove duplicate files.")
    parser.add_argument("-t", "--threads", dest="threads", action="store",
        default=DEFAULT_THREADS,
        help="Number of threads to use for file processing")

    opts = parser.parse_args()

    if opts.debug:
        set_debug(True)

    validate_options(parser, opts)

    plugins = load_plugins(parser, opts)

    return opts, plugins

def run(opts, plugins):
    """
    Find duplicate files within the provide paths, and list sets of duplicate
    files, optionally deleting certain copies.

    :param opts: argparse.Namespace:
    :param plugins: list of ModuleType:
    """
    engine = DupEngine(plugins)
    found = engine.find_duplicates(opts.paths, opts.threads)
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

