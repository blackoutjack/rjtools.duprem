
import sys

from util.testing import init_testing
from . import run

init_testing()
sys.exit(run().code)

from util.testing import run_main_suite
from . import run

run_main_suite()

