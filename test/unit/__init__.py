
from dgutil.testing import run_modules

from dgutil import fs
from .testfs import files as mockfiles

def run():
    from . import output

    fs.install_mocks(mockfiles)

    return run_modules("duprem.unit", locals())

