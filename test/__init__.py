
from util.testing import run_test_suites

from . import unit
from . import user

def run():
    return run_test_suites("duprem", unit, user)

