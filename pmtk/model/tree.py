"""
This module contains classes for building node trees.

Nodes and trees
---------------
This module defines Node class which is a node of a tree. A node in the tree
can have zero or more children, which are also of Node class. The original node
is then called a parent of any of its child nodes. A child node is said to be
below (or under) its parent and the parent is above its children. Above and
below are transitive relationships, that is parent of the parent is also above
the child and children of any child are below the parent and so forth. The node
which is above all other nodes and doesn't have a parent is called the root of
the tree.  All nodes that are below a certain node are called its subnodes. A
node with all of its subnodes form a subtree. For any two nodes, the smallest
subtree that contains them both is called smallest containing subtree (SCST).
It's easy to see that this tree will have their first common ancestor in the
root.

Node ids and paths
------------------
Each node has an id. A path to the node is a sequence of ids separated by dots
(".") adding some part of reversed ancestors list to the id of the node. Thus
the shortest path to the node is its id and the longest path is all ancestor
ids plus the node id (scanned from the root to the node) separated by dots.
Longest path is also called the absolute path. The id of the root node is taken
to be empty for the purposes of path construction so absolute path starts with
a dot, followed by the id of the closest to the root ancestor and so forth. Any
other path is a relative path.

Navigation in the tree
----------------------
The tree can be navigated from any node to any other node. Let's denote the
node from which the navigation starts 'origin node' and the node where we want
to arrive 'target node'. Valid path from origin to target can be:

* A relative path of the target which uniquely identifies it among all nodes in
  SCST, or

* A relative path of the target such that the target has the shortest absolute
  path of all the nodes in SCST matching the relative path, or

* The absolute path of the target.

The idea behind this is that nodes can be adressed using partial paths as long
as they are non-ambiguous at least locally (in some subtree containing the
origin). Additionally when the path is ambiguous in any subtree containing the
origin, the closest node to the root is returned. This is important to prevent
nodes close to the root being shadowed by their namesakes deep in the tree.
"""

class NavigationError(LookupError):
    """Navigation failed"""

class NonexistentPath(NavigationError):
    """Path doesn't match any nodes"""

class AmbiguousPath(NavigationError):
    """Path matches more than one node"""

    def __init__(self, path, nodes=None):
        self.path = path
        self.nodes = nodes

    def __str__(self):
        if self.nodes is not None:
            return '%s matches several nodes: %s' %\
                    (self.path, ', '.join(str(node) for node in self.nodes))
        else:
            return self.path


class Node:
    """Base class for building hierarchies"""

    def __init__(self, id='', parent=None):
        self.id = id
        self.parent = None
        self.abs_path = ('',) # absolute path as a tuple of ids
        self.children = {} # direct subnodes (children) by id
        self.subnodes_index = {} # unique relative paths of subnodes
        if parent is not None:
            parent.addChild(self)

    def __str__(self):
        return '.'.join(self.abs_path)

    def __repr__(self):
        return '<Node at %s>' % '.'.join(self.abs_path)

    def getLevel(self):
        """Return the length of self.abs_path -- level in the tree"""
        return len(self.abs_path)

    def relative_paths_generator(self):
        """Yield all relative paths of this node starting from shortest"""
        rel_path = None
        for part in reversed(self.abs_path[1:]):
            if rel_path:
                rel_path = part + '.' + rel_path
            else:
                rel_path = part
            yield rel_path

    def _indexSubnode(self, node, rel_path=None, rel_path_gen=None,
            recurse=True):
        """Index subnode with its shortest unique relative path

        This is sometimes called recursively with the paths generator partially
        consumed. The idea is that the shortest unique relative path for a node
        inside the parent can't be shorter than the one inside a child.
        """
        if self.parent is None: recurse = False # nowhere to recurse

        if rel_path_gen is None: rel_path_gen = node.relative_paths_generator()
        if rel_path is None: rel_path = next(rel_path_gen)

        if rel_path in self.subnodes_index:
            other = self.subnodes_index[rel_path]
            if isinstance(other, list):
                # there are several nodes with this subpath -- they must have
                # the same level, let's take first one
                other = other[0]
                if node.getLevel() < other.getLevel():
                    # we take this slot in the index
                    self.subnodes_index[rel_path] = node
                    if recurse:
                        self.parent._indexSubnode(node, rel_path, rel_path_gen)
                else:
                    # keep going
                    self._indexSubnode(node, None, rel_path_gen)
            else:
                # there's one node with this subpath, let's compare levels
                if node.getLevel() < other.getLevel(): # closer to the top:
                    # we replace other
                    self.subnodes_index[rel_path] = node
                    if recurse:
                        self.parent._indexSubnode(node, rel_path, rel_path_gen)
                    self._indexSubnode(other, recurse=False)
                elif node.getLevel() == other.getLevel(): # draw :(
                    # put both in the index slot
                    self.subnodes_index[rel_path] = [other, node]
                    # and calculate unique paths for both
                    self._indexSubnode(other, recurse=False)
                    self._indexSubnode(node, None, rel_path_gen)
                else: # other is closer to the top:
                    # keep going
                    self._indexSubnode(node, None, rel_path_gen)
        else:
            self.subnodes_index[rel_path] = node
            if recurse:
                self.parent._indexSubnode(node, rel_path, rel_path_gen)

    def listChildren(self):
        """Return a list of all children of this node"""
        return self.children.values()

    def _readdChildren(self):
        """Readd all the children to this node

        This is used to update all the indexes when a tree is added as a branch
        under some other node.
        """
        children = self.listChildren()
        self.children = {}
        self.subnodes_index = {}
        for child in children:
            self.addChild(child)

    def addChild(self, child):
        """Add child node to this node

        If the child contains its own children, all subtree will be reindexed.
        """
        if child.id in self.children:
            raise ValueError("Duplicate child id: %s" % child.id)
        self.children[child.id] = child
        child.parent = self
        child.abs_path = self.abs_path + (child.id,)
        self._indexSubnode(child)
        child._readdChildren()

        # now the node is indexed with its shortest unique relative path, so
        # we can navigate by trying progressively shorter subpaths of the path
        # that we're give and the first one that matches is the solution.

    def _navigateDirect(self, path):
        """Navigate without any smart lookup"""
        try:
            if '.' in path:
                first_id, rest = path.split('.', 1)
                return self.children[first_id]._navigateDirect(rest)
            else:
                return self.children[path]
        except (KeyError, NonexistentPath):
            raise NonexistentPath(path)

    def _matchesRelPath(self, path):
        """Check if our path ends with path"""
        path = tuple(path.split('.'))
        if len(path) > len(self.abs_path):
            return False
        else:
            return self.abs_path[-len(path):] == path

    def _navigateFuzzy(self, path):
        """Navigate by looking up unique subpaths in the index"""
        if path in self.subnodes_index:
            return self.subnodes_index[path]
        else:
            if '.' in path:
                # try subpath
                _, subpath = path.split('.', 1)
                sr = self._navigateFuzzy(subpath)
                if isinstance(sr, Node) and sr._matchesRelPath(path):
                    return sr # not list or None and matches full path
                else:
                    return None
            else:
                return None

    def navigate(self, path, fuzzy=False):
        """Navigate to path starting from current node"""
        if path.startswith('.'):
            return self.getRoot()._navigateDirect(path[1:])
        else:
            t = self._navigateFuzzy(path)
            if isinstance(t, list):
                raise AmbiguousPath(path, t)
            elif t is not None:
                return t
            elif self.parent is not None:
                return self.parent.navigate(path)
            else:
                raise NonexistentPath(path)

    def getRoot(self):
        """Return the root of the hierarchy"""
        if self.parent is None:
            return self
        else:
            return self.parent.getRoot()
