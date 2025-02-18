
from dgutil.testing import run_packages

def run():
    from . import unit
    from . import user

    return run_packages("duprem", locals())

