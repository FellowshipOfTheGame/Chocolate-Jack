__author__ = 'iury'

'''
    Module that contains utils functions
'''

def safe_load(function, *args):
    import sys
    if 'linux' in sys.platform:
        path = args[0].replace('\\','/')
    else:
        path = args[0].replace('/','\\')

    return function(path)
