"""Short compatibility hack to add fileno and isatty methods to the standard streams.

Some scripts meant for "normal computers" require these methods to exist and return something reasonable. Pythonista's standard streams do not have them by default, which causes such scripts to crash.

The file descriptors returned by fileno are of course not real. Actually, they are *too* real - they belong to the real standard streams, which go nowhere on iOS.

isatty returns False, because the Pythonista console is not a terminal emulator. If you make it return True, scripts may start writing out ANSI escape codes for output formatting and cursor control. Pythonista doesn't support these, so they are printed out literally, which is ugly. Although some scripts also assume that *only* TTYs are interactive, or require the standard streams to be TTYs, so there are valid reasons to make them return True.
"""

from __future__ import absolute_import, division, print_function

def run():
    import sys
    
    print(u"Patching standard stream objects...")
    
    def make_isatty(isit):
        def isatty(self):
            return isit
        return isatty
    
    def make_fileno(no):
        def fileno(self):
            return no
        return fileno
    
    sys.stdin.__class__.fileno = make_fileno(0)
    sys.stdin.__class__.isatty = make_isatty(False)
    
    sys.stdout.__class__.fileno = make_fileno(1)
    sys.stdout.__class__.isatty = make_isatty(False)
    
    sys.stderr.__class__.fileno = make_fileno(2)
    sys.stderr.__class__.isatty = make_isatty(False)
    
    print(u"Done patching standard stream objects.")

if __name__ == "__main__":
    run()
