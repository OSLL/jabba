
from jabba.analysis import Result

def extension_name(options, **kwargs):
    return _Result()

class _Result(Result):
    def __str__(self):
        return "OK"
