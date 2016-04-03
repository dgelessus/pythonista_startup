"""Highly unreliable way to register "preflight hooks", which are run every time you run a script (but not an editor action)."""

from __future__ import absolute_import, division, print_function

def run():
    print(u"Installing preflight hooks...")
    
    # There's no official way to add hooks that run before every script run.
    # However Pythonista's preflight code imports pythonista_startup once to check what names it contains.
    # So we hack __import__ to run all functions in preflight_hooks whenever pythonista_startup is imported by specific bytecodes.
    
    try:
        import builtins
    except ImportError:
        import __builtin__ as builtins
    
    preflight_hooks = []
    
    def _make_new_import():
        import sys
        
        _real_import = builtins.__import__
        
        def __import__(name, *args, **kwargs):
            if name == "pythonista_startup":
                try:
                    f = sys._getframe(1)
                except ValueError:
                    pass
                else:
                    # These blobs are the bytecodes of the main function of Pythonista's preflight code (from Pythonista 2 and 3 respectively), which is run once before every script run.
                    if f.f_code.co_code in (
                        b'y\x0e\x00d\x00\x00d\x01\x00l\x00\x00TWn\x07\x00\x01\x01\x01n\x01\x00Xd\x02\x00S',
                        ##b'y\x1c\x00d\x01\x00d\x00\x00l\x00\x00}\x00\x00t\x01\x00|\x00\x00\x83\x01\x00}\x01\x00Wn\x0e\x00\x01\x01\x01g\x00\x00}\x01\x00Yn\x01\x00Xy\x15\x00t\x02\x00\x83\x00\x00\x01t\x03\x00|\x01\x00\x83\x01\x00\x01Wn\x08\x00\x01\x01\x01Yn\x01\x00Xd\x00\x00S',
                        b'y\x1c\x00d\x01\x00d\x00\x00l\x00\x00}\x00\x00t\x01\x00|\x00\x00\x83\x01\x00}\x01\x00Wn\x0e\x00\x01\x01\x01g\x00\x00}\x01\x00Yn\x01\x00Xyy\x00d\x01\x00d\x00\x00l\x02\x00}\x02\x00d\x01\x00d\x00\x00l\x03\x00}\x03\x00d\x01\x00d\x00\x00l\x04\x00}\x04\x00d\x01\x00d\x00\x00l\x05\x00}\x05\x00|\x02\x00j\x06\x00d\x00\x00\x83\x01\x00\x01|\x03\x00j\x06\x00d\x00\x00\x83\x01\x00\x01|\x04\x00j\x06\x00d\x00\x00\x83\x01\x00\x01|\x05\x00j\x06\x00d\x00\x00\x83\x01\x00\x01t\x07\x00\x83\x00\x00\x01t\x08\x00|\x01\x00\x83\x01\x00\x01Wn\x08\x00\x01\x01\x01Yn\x01\x00Xd\x00\x00S',
                    ):
                        for hook in preflight_hooks:
                            hook()
            
            return _real_import(name, *args, **kwargs)
        
        __import__.patched = True
        
        return __import__
    
    if not getattr(builtins.__import__, "patched", False):
        builtins.__import__ = _make_new_import()
    
    del builtins
    del _make_new_import
    
    print(u"Done installing preflight hooks.")

if __name__ == "__main__":
    run()
