"""
PPL reader
"""

class ReaderContext(dict):
    """Used by reader to keep track of current context"""

    def __init__(self, parent=None, **kw):
        self.parent = parent
        self.update(kw)

    def __getitem__(self, key, default=None):
        try:
            return super(ReaderContext, self).__getitem__(key)
        except KeyError:
            if self.parent is not None:
                return self.parent.__getitem__(key, default)
            else:
                if default is not None:
                    return default
                else:
                    raise KeyError(key)


class Reader:
    """Read and pre-parse .ppl file(s)"""

    def __init__(self):
        pass

    def read(self, stream, context=None, name=''):
        """Read lines from the stream"""
        
