
from util.testing import init_stubs, run_tests

from util import fs

def run():
    from . import output

    init_stubs(fs) 

    return run_tests("duprem.unit", locals())

