"""Enable Python's faulthandler.

When you crash the app, a traceback is written into the faultlog folder and a warning message is displayed the next time you launch Pythonista.
"""

from __future__ import absolute_import, division, print_function

def run():
    import sys
    
    if sys.version_info < (3,):
        print(u"The faulthandler module is only available under Python 3.", file=sys.stderr)
        print(u"Please edit pythonista_startup/__init__.py and comment out the enable_faulthandler submodule.", file=sys.stderr)
        return
    
    # From this point on, code must be syntactically valid Python 2, but further compatibility is not necessary.
    
    import datetime
    import faulthandler
    import os
    import shutil
    
    print("Enabling fault handler...")
    
    LOGDIR = os.path.expanduser("~/Documents/faultlog")
    LOGNAME_TEMPLATE = "faultlog-{:%Y-%m-%d-%H-%M-%S}.txt"
    LOGNAME_DEFAULT = "faultlog-temp.txt"
    
    try:
        os.mkdir(LOGDIR)
    except FileExistsError:
        pass
    
    did_fault = False
    
    try:
        f = open(os.path.join(LOGDIR, LOGNAME_DEFAULT), "rb")
    except FileNotFoundError:
        pass
    else:
        with f:
            if f.read(1):
                did_fault = True
    
    if did_fault:
        print(u"Pythonista quit abnormally last time.", file=sys.stderr)
        mtime = datetime.datetime.fromtimestamp(os.stat(os.path.join(LOGDIR, LOGNAME_DEFAULT)).st_mtime)
        print(u"For details, see the log file '{}'.".format(LOGNAME_TEMPLATE.format(mtime)), file=sys.stderr)
        shutil.move(os.path.join(LOGDIR, LOGNAME_DEFAULT), os.path.join(LOGDIR, LOGNAME_TEMPLATE.format(mtime)))
    
    logfile = open(os.path.join(LOGDIR, LOGNAME_DEFAULT), "wb")
    faulthandler.enable(logfile)
    
    print(u"Done enabling fault handler.")

if __name__ == "__main__":
    run()
