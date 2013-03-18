"""
Tests for the tree building module model.tree.
"""

import unittest
import base

from pmtk.model.tree import Node, NonexistentPath, AmbiguousPath


class Record(object):
    pass


class TestNode(unittest.TestCase):
    """Test the tree building and navigation."""

    def test_addSubnode(self):
        """Test addSubnode for a very simple case."""
        root = Node()
        foo = Node('foo', root)
        bar = Node('bar', root)
        baz = Node('baz', foo)
        unz = Node('unz', baz)
        self.assertEqual(root.children, {'foo': foo, 'bar': bar})
        self.assertEqual(foo.children, {'baz': baz})

    def _build_tree(self):
        """Build a reasonably complicated tree."""
        T = Record()
        T.root = Node()
        T.a = Node('a', T.root)
        T.ab = Node('b', T.a)
        T.abe = Node('e', T.ab)
        T.abed = Node('d', T.abe)
        T.ac = Node('c', T.a)
        T.aca = Node('a', T.ac)
        T.acd = Node('d', T.ac)
        T.ace = Node('e', T.ac)
        T.aced = Node('d', T.ace)
        T.b = Node('b', T.root)
        T.bc = Node('c', T.b)
        T.bcd = Node('d', T.bc)
        T.bcf = Node('f', T.bc)
        return T

    def test_getAbsolutePath(self):
        """Test getAbsolutePath method."""
        T = self._build_tree()
        self.assertEqual(T.root.getAbsolutePath(), '.')
        self.assertEqual(T.a.getAbsolutePath(), '.a')
        self.assertEqual(T.abed.getAbsolutePath(), '.a.b.e.d')

    def test_fuzzyNavigation(self):
        """Test fuzzy navigation."""
        T = self._build_tree()
        self.assertEqual(T.bcf.navigate('d'), T.bcd)
        self.assertEqual(T.ace.navigate('d'), T.aced)
        self.assertEqual(T.bcf.navigate('c.d'), T.bcd)
        self.assertEqual(T.a.navigate('c.d'), T.acd)
        self.assertEqual(T.bcf.navigate('c.e'), T.ace)
        self.assertEqual(T.bcf.navigate('a.c'), T.ac)
        self.assertEqual(T.ac.navigate('e.d'), T.aced)
        self.assertEqual(T.ab.navigate('e.d'), T.abed)
        self.assertEqual(T.a.navigate('d'), T.acd)
        self.assertEqual(T.a.navigate('c.d'), T.acd)
        self.assertEqual(T.aca.navigate('d'), T.acd)
        self.assertEqual(T.ace.navigate('d'), T.aced)
        self.assertEqual(T.bcf.navigate('b'), T.b)
        self.assertEqual(T.root.navigate('b'), T.b)
        self.assertRaises(NonexistentPath, T.bcf.navigate, 'z')
        self.assertRaises(AmbiguousPath, T.bcf.navigate, 'e.d')
        self.assertRaises(AmbiguousPath, T.root.navigate, 'c.d')

    def test_fuzzyNavigation2(self):
        root = Node()
        a = Node('a', root)
        ac = Node('c', a)
        ad = Node('d', a)
        b = Node('b', root)
        ba = Node('a', b)
        bac = Node('c', ba)
        self.assertEqual(ad.navigate('a.c'), ac)

    def test_directNavigation(self):
        """Test navigation by absolute path."""
        T = self._build_tree()
        self.assertEqual(T.b.navigate('.a.c.e.d'), T.aced)
        self.assertEqual(T.aca.navigate('.a'), T.a)
        self.assertEqual(T.b.navigate('.'), T.root)

    def test_listChildren(self):
        T = self._build_tree()
        self.assertItemsEqual(T.root.listChildren(), [T.a, T.b])
        self.assertItemsEqual(T.a.listChildren(), [T.ab, T.ac])
        self.assertItemsEqual(T.ac.listChildren(), [T.aca, T.acd, T.ace])

    def test_yieldDescendants(self):
        T = self._build_tree()
        self.assertItemsEqual(list(T.root.yieldDescendants()),
            [v for (k,v) in T.__dict__.items() if k[0] in ('a', 'b')])


if __name__ == '__main__':
    unittest.main()

