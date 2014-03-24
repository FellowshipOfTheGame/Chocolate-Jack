__author__ = 'iury'

'''
    Module that contains utils functions
'''

def safe_load(function, *args):
    import sys
    if 'linux' in sys.platform:
        args = args[0].replace('\\','/')
    else:
        args = args[0].replace('/','\\')

    return function(args)
