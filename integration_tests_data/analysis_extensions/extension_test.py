
from jabba.analysis import Result

def dummy_check(options, **kwargs):
    return _Result()

class _Result(Result):
    def __str__(self):
        return "OK"
