class Result(object):
    """
    Base class for analysis results
    """

    def __init__(self):
        self.results = []
        self.header = 'Abstract analysis result'

    def is_ok(self):
        return len(self.results) == 0

    def add(self, err):
        self.results.append(err)

    def format_header(self):
        return "\n{}\n---\n".format(self.header)
