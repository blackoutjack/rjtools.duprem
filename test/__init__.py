
from util.testing import run_test_suites

def run():
    from . import unit
    from . import user

    return run_test_suites("duprem", locals())

