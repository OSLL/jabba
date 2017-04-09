

class Result(object):

    def __init__(self):
        self.errors = []

    def is_ok(self):
        return len(self.errors) == 0

    def add(self, err):
        self.errors.append(err)
