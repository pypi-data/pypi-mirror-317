#! /usr/bin/env python3
# vim:fenc=utf-8

"""
Functions for showing which variables take up memory.
by Fred Cirera,  https://stackoverflow.com/a/1094933/1870254, modified
"""

import sys

def sizeof_fmt(num, suffix='B'):
    ''' Pretty print the size of a variable. '''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

def print_largest_variables(variables, top=10):
    """ Print the names and sizes of the top largest variables. """
    variables = list(variables.items())
    variables_with_sizes = ((name, sys.getsizeof(value)) for name, value in variables)

    if not top:
        for name, size in sorted(variables_with_sizes, key= lambda x: -x[1]):
            print("{:>30}: {:>8}".format(name, sizeof_fmt(size)))
    else:
        for name, size in sorted(variables_with_sizes, key= lambda x: -x[1])[:top]:
            print("{:>30}: {:>8}".format(name, sizeof_fmt(size)))
