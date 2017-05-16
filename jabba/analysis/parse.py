
import collections

FunctionArguments = collections.namedtuple('FunctionArguments', ['function', 'arguments'])

argument_splitter = ":"

def parse_analyzer_arguments(arguments):
    """
    Parse string in format `function_1:param1=value:param2 function_2:param` into array of FunctionArguments
    """

    rets = []

    for argument in arguments:
        args = argument.split(argument_splitter)

        # The first one is the function name
        func_name = args[0]

        # The rest is the args
        func_args = {}

        for arg in args[1:]:
            key, value = parse_arg(arg)

            func_args[key] = value

        rets.append(FunctionArguments(function=func_name, arguments=func_args))

    return rets

def parse_arg(arg):
    arg = arg.split("=")

    if len(arg) == 1:
        return arg[0], True

    try:
        return arg[0], float(arg[1])
    except ValueError:
        if arg[1].lower() == 'true':
            return arg[0], True

        if arg[1].lower() == 'false':
            return arg[0], False

        return arg[0], arg[1]
