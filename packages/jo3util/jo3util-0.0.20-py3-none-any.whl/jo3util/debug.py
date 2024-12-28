#! /usr/bin/env python3
# vim:fenc=utf-8

import sys
import debugpy


def debugger_is_active() -> bool:
    """Return if the debugger is currently active

    from https://stackoverflow.com/questions/38634988/
        check-if-program-runs-in-debug-mode
    """
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None


def breakpoint(wait=True, address="localhost", port=5678):
    """ Breakpoint that launches debugpy if it's not already active.

    Args:
        wait: Whether debugpy halts execution until a client attaches.
        address: The address where debugpy listens for a client.
        port: The port where debugpy listens for a client.
    """
    if not debugger_is_active():
        debugpy.listen((address, port))
        if wait:
            debugpy.wait_for_client()
    debugpy.breakpoint()
