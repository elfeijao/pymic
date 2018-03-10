import logging
import sys

def get_entrypoing():
    '''Return the entrypoint for this module'''

    return sys.argv[0].replace('.py', '').replace('.exe', '');

def setup():

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=logging.DEBUG,
        filename='.'.join([get_entrypoing(), 'log']),
        datefmt='%Y-%m-%d %H:%M:%S'
    )
