
from dgutil.testing import run_modules

def run():
    from . import output

    return run_modules("duprem.user", locals())

