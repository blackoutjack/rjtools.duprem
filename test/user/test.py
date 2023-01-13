
from util.testing import run_tests

def run():
    from . import output

    return run_tests(dir(), locals())

