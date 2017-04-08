

class Result(object):

    def is_ok(self):
        return len(self.errors) == 0
