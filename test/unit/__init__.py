
from rjtools.util.testing import run_modules

from rjtools.util import fs
from .testfs import files as mockfiles

def run():
    from . import output

    fs.install_mocks(mockfiles)

    return run_modules("duprem.unit", locals())

