"""
Tests for the ppl reader
"""

import unittest

from pmtk.ppl.reader import ReaderContext


class ContextTest(unittest.TestCase):

    def test_basic(self):
        a = ReaderContext(x=1, y=2)
        b = ReaderContext(parent=a, y=3, z=4)
        c = ReaderContext(parent=b, z=5)
        for k,l in ((a['x'], 1), (a['y'], 2),
                    (b['x'], 1), (b['y'], 3),
                    (c['x'], 1), (c['y'], 3)):
            self.failUnlessEqual(k, l)
        self.failUnlessEqual(a.get('z', 6), 6)
        try:
            a['z']
            assert False
        except KeyError:
            pass


if __name__ == '__main__':
    unittest.main()

