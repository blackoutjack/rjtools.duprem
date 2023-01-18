
from util.testing import summarize_results
from util import fs

from . import unit
from . import user

def run():
    unitresult = unit.run()
    userresult = user.run()

    summary = summarize_results("duprem", unitresult, userresult)
    summary.print()
    return summary

