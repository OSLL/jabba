
import os

def convert_path(path):
    if os.path.isabs(path):
        raise Exception("Cannot include file with absolute path {}. Please use relative path instead".format((path)))

    path = os.path.normpath(path)

    return path
 
def is_job_config(config):
    try:
        if config[0]['job']['name'] is not None:
            return True
    except KeyError:
        return False
    except TypeError:
        return False
    except IndexError:
        return False

    return False
