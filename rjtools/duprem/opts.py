from argparse import ArgumentParser, REMAINDER
import importlib
import platform

from rjtools.util.msg import dbg, set_debug
from rjtools.util.fs import is_root

from rjtools.duprem.engine import DEFAULT_THREADS

def validate_options(parser, opts):

    if len(opts.paths) < 1:
        parser.error(
            "Provide at least one directory (or multiple files) to scan for duplicates")
    dbg("Paths: %r" % opts.paths)

    if opts.threads is not None:
        try:
            threads = int(opts.threads)
            if threads < 1 or threads > 16:
                parser.error("Threads should be 1 to 16")
            opts.threads = threads
        except ValueError:
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
            plugin = importlib.import_module(f"rjtools.duprem.plugin.{plugin}")
            if not hasattr(plugin, "can_handle"):
                parser.error(f"Plugin {plugin} does not implement can_handle")
            if not hasattr(plugin, "load_file"):
                parser.error(f"Plugin {plugin} does not implement load_file")
            loadedPlugins.append(plugin)
        except ImportError:
            parser.error(f"Unable to load plugin {plugin}")
    return loadedPlugins

def load_argument_parser():
    parser = ArgumentParser()
    parser.add_argument("paths", nargs=REMAINDER, metavar="PATHS...")
    parser.add_argument("-f", "--force", dest="force", action="store_true",
        help="With --remove, force removal of all but the first copy of "
            "duplicate content without asking.")
    parser.add_argument("-g", "--debug", dest="debug", action="store_true",
        help="Enable debug output")
    parser.add_argument("-E", "--include-empty", dest="doEmpty", action="store_true",
        help="Include empty files in duplicate analysis")
    parser.add_argument("-H", "--include-hidden", dest="doHidden", action="store_true",
        help="Include hidden files in duplicate analysis")
    parser.add_argument("-p", "--plugin", dest="plugins", action="append",
        default=[], help="File types (defined in [duprem]/plugin) to use for "
            "special duplicate detection logic")
    parser.add_argument("-r", "--remove", dest="remove", action="store_true",
        help="Give the user the option to remove duplicate files.")
    parser.add_argument("-t", "--threads", dest="threads", action="store",
        default=DEFAULT_THREADS,
        help="Number of threads to use for file processing")

    return parser

def load_options():

    parser = load_argument_parser()

    opts = parser.parse_args()

    if opts.debug:
        set_debug(True)

    validate_options(parser, opts)

    plugins = load_plugins(parser, opts)

    return opts, plugins
