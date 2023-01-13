
import sys

from util.testing import init_testing, run_tests
from . import test

if __name__ == "__main__":
    init_testing()
    sys.exit(test())

