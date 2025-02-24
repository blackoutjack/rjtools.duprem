
from rjtools.util.testing import run_modules

from rjtools.util import fs
from .testfs import files as mockfiles

def run():
    from . import output
    from . import options

    fs.install_mocks(mockfiles)

    return run_modules("rjtools.duprem.test.unit", locals())

