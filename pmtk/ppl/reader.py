"""
PPL reader
"""

no_default = []

class ReaderContext(dict):
    """Used by reader to keep track of current context"""

    def __init__(self, parent_context=None, **kw):
        self.parent_context = parent_context
        self.update(kw)

    def __getitem__(self, key, default=no_default):
        try:
            return super(ReaderContext, self).__getitem__(key)
        except KeyError:
            if self.parent_context is not None:
                return self.parent_context.get(key, default)
            else:
                if default is not no_default:
                    return default
                else:
                    raise KeyError(key)

class Reader:
    """Read and pre-parse .ppl file(s)"""

