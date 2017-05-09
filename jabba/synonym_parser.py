class SynonymSet:
    """
    A set of synonyms set
    If two parameters are in the same set, they are considered synonyms
    """

    def __init__(self):
        self.synonyms = []

    def add_set(self, s):
        self.synonyms.append(s)

    def get_synonyms(self, param):
        for syn_set in self.synonyms:
            if param in syn_set:
                return syn_set

        return {}

    def are_synonyms(self, param_1, param_2):
        for syn_set in self.synonyms:
            if param_1 in syn_set and param_2 in syn_set:
                return True

        return False

    def __str__(self):
        return ':'.join(repr(syn_set) for syn_set in self.synonyms)

def parse_from_args(synonyms):
    '''
    Parse an array of string from argparser
    to SynonymSet
    '''

    syns_str = ''.join(synonyms)

    syns_str = syns_str.replace(' ', '')
    
    syn_set = SynonymSet()

    # to check if we are parsing inside the parenthesis
    inside_set = False
    current_syn = ''
    current_syn_set = set()

    for char in syns_str:
        if char == '{':
            inside_set = True
            current_syn_set = set()
            continue

        if char == '}':
            inside_set = False
            current_syn_set.add(current_syn)

            syn_set.add_set(current_syn_set)

            current_syn = ''

            continue

        if not inside_set:
            raise Exception("Incorrect synonyms {}".format(syns_str))

        if char == ',':
            if current_syn == '':
                raise Exception("Incorrect synonyms {}".format(syns_str))

            current_syn_set.add(current_syn)
            current_syn = ''

            continue

        current_syn += char

    return syn_set

def parse_from_array(arr):
    """
    Parse 2d array into synonym set
    Every array inside arr is considered a set of synonyms
    """
    syn_set = SynonymSet()

    for synonyms in arr:
        _set = set()

        for synonym in synonyms:
            _set.add(synonym)

        syn_set.add_set(_set)

    return syn_set

