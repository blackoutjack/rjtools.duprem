
import sys

from util.testing import init_testing, run_tests

def test():
    from . import output

    return run_tests(dir(), locals())

if __name__ == "__main__":
    init_testing()
    sys.exit(test())
