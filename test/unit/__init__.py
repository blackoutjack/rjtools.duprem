
from dgutil.testing import init_stubs, run_modules

from dgutil import fs

def run():
    from . import output

    init_stubs(fs) 

    return run_modules("duprem.unit", locals())

