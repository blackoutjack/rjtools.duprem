
import sys

from util.testing import init_testing

from .unit import test as unittest
from .user import test as usertest

if __name__ == "__main__":
    init_testing()
    result = unittest.run()
    result &= usertest.run()
    sys.exit(result)
