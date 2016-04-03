"""Register a custom sys.displayhook and sys.excepthook.

Both of these use custom coloring. The default colors are based on the default theme, if you use something different the colors will not match your theme and may not look nice. If you're using a dark theme, you won't be able to read anything.

Features of the displayhook:
* Basic IPython-style output history. There is a global list named Out (technically added to the builtins/__builtin__ module) which contains the results of all expressions run in the interactive console.
* The result lines show at which position in the Out list the result can be found, for later reference.
* Like the default displayhook, expressions that return None are ignored - nothing is printed, and the value of _ is not changed. This can be changed so that None is displayed and stored in _ and Out, by uncommmenting a line in the displayhook definition.

Features of the excepthook:
* A little more whitespace to make the traceback more readable.
* The traceback uses different colors for text, file paths, line numbers, etc.
* Syntax errors use Unicode magic and color changing to mark at which character the syntax error occurred. Admittedly this does not always work well and may be more "look at my fancy graphics" than useful.
* Source file paths are shortened and do not show the long path of the app sandbox.
* Source file paths are tappable links that open in the Pythonista editor. This uses the normal pythonista:// URL scheme, which means that files are *not* opened in a new tab. Instead they replace whatever was open in your last active tab.
* Python 3 chained exceptions *should* work. No, that cannot be backported to Python 2.
"""

from __future__ import absolute_import, division, print_function

def run():
    try:
        import builtins
    except ImportError:
        import __builtin__ as builtins
    import console
    import os
    import sys
    import traceback
    try:
        from urllib.parse import quote
    except ImportError:
        from urllib import quote
    
    print(u"Customizing sys hooks...")
    
    APP_GROUP_DIR = os.path.expanduser(u"~")
    if os.path.basename(APP_GROUP_DIR) == u"Pythonista3":
        APP_GROUP_DIR = os.path.dirname(APP_GROUP_DIR)
    APP_GROUP_DIR += os.sep
    APP_DIR = u"" + os.path.dirname(os.path.dirname(sys.executable)) + os.sep
    
    REMOVE_PREFIXES = (APP_GROUP_DIR, APP_DIR)
    
    DOCUMENTS = os.path.expanduser("~/Documents")
    
    def write_filename(path):
        if path.startswith(u"<") and path.endswith(u">"):
            print(path, end=u"")
        else:
            short_path = path
            
            for prefix in REMOVE_PREFIXES:
                if short_path.startswith(prefix):
                    short_path = path[len(prefix):]
                    break
            
            console.write_link(short_path, (u"pythonista3://" if sys.version_info > (3,) else u"pythonista://") + quote(os.path.relpath(path, DOCUMENTS)))
    
    def displayhook(obj):
        # Uncomment the next line if you want None to be "visible" like any other object.
        #"""
        if obj is None:
            return
        #"""
        
        try:
            builtins.Out
        except AttributeError:
            builtins.Out = []
        
        builtins._ = obj
        builtins.Out.append(obj)
        console.set_color(0.0, 0.5, 0.0)
        print(u"Out[{}]".format(len(builtins.Out)-1), end=u"")
        console.set_color(0.2, 0.2, 0.2)
        print(u" = ", end=u"")
        console.set_color(0.33, 0.57, 1.0)
        print(repr(obj))
        console.set_color(0.2, 0.2, 0.2)
    
    sys.displayhook = displayhook
    
    def _excepthook(exc_type, exc_value, exc_traceback):
        for filename, lineno, funcname, text in traceback.extract_tb(exc_traceback):
            
            console.set_color(0.2, 0.2, 0.2)
            print(u"\tFile ", end=u"")
            console.set_color(0.81, 0.32, 0.29)
            write_filename(filename)
            
            console.set_color(0.2, 0.2, 0.2)
            print(u", line ", end=u"")
            console.set_color(0.15, 0.51, 0.84)
            print(lineno, end=u"")
            
            console.set_color(0.2, 0.2, 0.2)
            print(u", in ", end=u"")
            console.set_color(0.13, 0.46, 0.49)
            print(funcname, end=u"")
            
            console.set_color(0.2, 0.2, 0.2)
            print(u":")
            
            console.set_color(0.2, 0.2, 0.2)
            if isinstance(text, bytes):
                text = text.decode(u"utf-8", u"replace")
            print(u"\t\t" + (text or u"# Source code unavailable"))
            print()
        
        if issubclass(exc_type, SyntaxError):
            console.set_color(0.2, 0.2, 0.2)
            print(u"\tFile ", end=u"")
            console.set_color(0.81, 0.32, 0.29)
            write_filename(exc_value.filename)
            
            console.set_color(0.2, 0.2, 0.2)
            print(u", line ", end=u"")
            console.set_color(0.15, 0.51, 0.84)
            print(exc_value.lineno, end=u"")
            
            console.set_color(0.2, 0.2, 0.2)
            print(u":")
            
            if exc_value.text is None:
                console.set_color(0.75, 0.0, 0.0)
                print(u"\t\t# Source code unavailable")
            else:
                etext = exc_value.text
                if isinstance(etext, bytes):
                    etext = etext.decode(u"utf-8", u"replace")
                console.set_color(0.2, 0.2, 0.2)
                print(u"\t\t" + etext[:exc_value.offset], end=u"")
                console.set_color(0.75, 0.0, 0.0)
                print(u"\N{COMBINING LOW LINE}" + etext[exc_value.offset:].rstrip())
        
        console.set_color(0.43, 0.25, 0.66)
        print(exc_type.__module__, end=u"")
        console.set_color(0.2, 0.2, 0.2)
        print(u".", end=u"")
        console.set_color(0.13, 0.46, 0.49)
        print(getattr(exc_type, "__qualname__", exc_type.__name__), end=u"")
        
        msg = exc_value.msg if issubclass(exc_type, SyntaxError) else str(exc_value)
        
        if msg:
            console.set_color(0.2, 0.2, 0.2)
            print(u": ", end=u"")
            console.set_color(0.75, 0.0, 0.0)
            print(msg, end=u"")
        
        console.set_color(0.2, 0.2, 0.2)
        print()
    
    def excepthook(exc_type, exc_value, exc_traceback):
        try:
            console.set_color(0.75, 0.0, 0.0)
            print(u"Traceback (most recent call last):")
            _excepthook(exc_type, exc_value, exc_traceback)
            
            # On Python 2, exceptions have no __cause__.
            while getattr(exc_value, "__cause__", None) is not None and not exc_value.__suppress_context__:
                console.set_color(0.75, 0.0, 0.0)
                print()
                if exc_value.__cause__ == exc_value.__context__:
                    print(u"During handling of the above exception, another exception occurred:")
                else:
                    print(u"The above exception was the direct cause of the following exception:")
                
                exc_value = exc_value.__cause__
                exc_type = exc_value.__class__
                exc_traceback = exc_value.__traceback__
                
                _excepthook(exc_type, exc_value, exc_traceback)
        except Exception as err:
            traceback.print_exc()
        finally:
            console.set_color(0.2, 0.2, 0.2)
    
    # sys.excepthook can't be customized, Pythonista overrides it on every script run.
    # So we need to override sys.__excepthook__ instead.
    
    sys.__excepthook__ = excepthook
    
    print(u"Done customizing sys hooks.")

if __name__ == "__main__":
    run()
