""" get_dir.py  -  for getting current and parent directories """
import os

def getCurrDir():
    """ get current directory """
    return os.getcwd()

def getParentDir(path):
    """ get parent directory """
    return os.path.abspath(os.path.join(path, os.pardir))

def listdirs(path):
    """ list directories inside a path """
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]