from __future__ import absolute_import, division, print_function

import sys
print(u"Python", sys.version)
del sys

print(u"Executing pythonista_startup...")

try:
    print(u"Importing submodules of pythonista_startup...")
    
    import importlib
    import sys
    import traceback
    
    # Modify this tuple to include the features you want.
    # See the individual files for a full description of each submodule.
    for name in (
        ##"_preflight_hook_experiment",
        ##"customize_sys_hooks",
        ##"enable_faulthandler",
        "patch_stdstreams",
        ##"restore_types",
    ):
        try:
            importlib.import_module("pythonista_startup." + name).run()
        except: # Catch everything
            print(u"Exception while running submodule {}:".format(name), file=sys.stderr)
            traceback.print_exc()
    
    del importlib
    del sys
    del traceback
    del name
    
    print(u"Done importing submodules of pythonista_startup.")
    
    # To disable globals clearing, comment out the next line.
    """
    print(u"Preventing globals clearing...")
    
    import sys
    import types
    
    class DirAllTheGlobals(types.ModuleType):
        import __main__
        
        def __dir__(self):
            return dir(type(self).__main__)
    
    # THESE LINES MUST COME LAST.
    # Anything past this point is executed in the context of the old pythonista_startup module, which may already be partially garbage-collected.
    new_module = DirAllTheGlobals(__name__, __doc__)
    vars(new_module).update(vars(sys.modules["pythonista_startup"]))
    sys.modules["pythonista_startup"] = new_module
    
    del sys
    del types
    del DirAllTheGlobals
    del new_module
    
    print(u"Done preventing globals clearing.")
    #"""
    
except: # Catch everything
    import sys
    import traceback
    
    print(u"Swallowed exception:", file=sys.stderr)
    traceback.print_exc()
    
    print(u"Trying to reraise.", file=sys.stderr)
    del sys
    del traceback
    raise

print(u"Done executing pythonista_startup.")
