#! /usr/bin/env python3
# vim:fenc=utf-8

"""

"""

import warnings

class ToDoWarning(Warning):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return repr(self.message)

PAST_TODO_MESSAGES = set()

def todo(msg):
    global PAST_TODO_MESSAGES
    if msg not in PAST_TODO_MESSAGES:
        warnings.warn(msg, ToDoWarning)
        PAST_TODO_MESSAGES.add(msg)
