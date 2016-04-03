"""This little thing walks through the entire type hierarchy, starting at object, and assigns all type objects to their "owner" modules based on their __module__ and __name__ attributes. Especially the __builtin__/builtins module has many "hidden" types that can only be accessed indirectly. Some of these are useful (like instancemethod), some are interesting to play around with (like code), and most are useless (like the many iterator types)."""

from __future__ import absolute_import, division, print_function

def run():
    import importlib
    import re
    import sys
    import types
    
    print(u"Making all types available...")
    
    def restore_types(cls):
        try:
            mod = importlib.import_module(cls.__module__)
        except ImportError:
            return
        
        name = re.sub(r"(^[0-9]|[^A-Za-z0-9]+)", "_", cls.__name__)
        
        do_set = True
        
        if hasattr(mod, name):
            if getattr(mod, name) == cls:
                do_set = False
            
            if do_set:
                if not isinstance(getattr(mod, name), type):
                    name += "___class__"
                
                if hasattr(mod, name):
                    if getattr(mod, name) == cls:
                        do_set = False
                    
                    if do_set:
                        basename = name
                        i = 0
                        name = basename + "_" + str(i)
                        
                        while hasattr(mod, name):
                            if getattr(mod, name) == cls:
                                do_set = False
                                break
                            i += 1
                            name = basename + "_" + str(i)
        
        if do_set:
            setattr(mod, name, cls)
        
        try:
            subs = cls.__subclasses__()
        except TypeError:
            subs = type(cls).__subclasses__(cls)
        
        for sub in subs:
            restore_types(sub)
    
    restore_types(object)
    
    print(u"Done making all types available.")

if __name__ == "__main__":
    run()
