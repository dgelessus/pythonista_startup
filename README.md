# pythonista_startup

Bits and pieces from my pythonista_startup folder.

## Installation

### To install a single script

If you don't have a `pythonista_startup` file/folder already, create a new file named `pythonista_startup.py` under `Documents` or `site-packages`.

Each script is contained in a single function named `run`. Copy the entire function block from the script and paste it into your `pythonista_startup` file, rename the `run` function to something different, and then call it.

For example, a `pythonista_startup.py` with only `enable_faulthandler` could look like this:

```python
def enable_faulthandler():
    import ctypes
    import datetime
    # ... rest of the pasted code ...

enable_faulthandler()
```

### To install the entire package

Back up your existing `pythonista_startup` file/folder, then download this repo, name the folder `pythonista_startup` and put it under `Documents` or `site-packages`. The easiest way to do this is to run these commands in [stash](https://github.com/ywangd/stash):

```sh
mkdir site-packages/pythonista_startup
cd site-packages/pythonista_startup
git clone https://github.com/dgelessus/pythonista_startup.git
```

And to update:

```sh
cd site-packages/pythonista_startup
git pull
```
