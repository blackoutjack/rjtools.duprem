
from rjtools.util.testing import run_modules

def run():
    from . import output
    from . import image

    return run_modules("duprem.user", locals())

