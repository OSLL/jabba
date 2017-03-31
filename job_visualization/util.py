
import os

def convert_path(path):
    if os.path.isabs(path):
        raise Exception("Cannot include file with absolute path {}. Please use relative path instead".format((path)))

    path = os.path.normpath(path)

    return path
 
