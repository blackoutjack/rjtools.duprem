
from util.testing import init_stubs
from util import fs

from . import unit
from . import user

def run():
    init_stubs(fs)
    result = unit.run()
    result = max(result, user.run())
    return result
