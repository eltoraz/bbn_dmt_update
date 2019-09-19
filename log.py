# log.py - log messages to console
from datetime import datetime

def log(msg):
    """Print `msg` to the stdout with a timestamp prepended
    """
    print(datetime.now(), ': ', msg, sep='')
