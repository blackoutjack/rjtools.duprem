
from util.testing import init_stubs, run_modules

from util import fs

def run():
    from . import output

    init_stubs(fs) 

    return run_modules("duprem.unit", locals())

