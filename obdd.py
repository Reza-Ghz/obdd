"""
Ordered Binary Decision Diagram implementation.
"""

import random
import weakref
from functools import cached_property

import boolean

# existing BDDVariable references
_VARS = {}

# node/bdd cache
_NODES = weakref.WeakValueDictionary()
_BDDS = weakref.WeakValueDictionary()


class OBDDNode:
    """Ordered Binary decision diagram node

    Nodes are uniquely identified by a "root" integer,
    "lo" child node, and "hi" child node:

    The "root" of the zero node is -1,
    and the "root" of the one node is -2.
    Both zero/one nodes have "lo=None" and "hi=None".
    """

    def __init__(self, root, lo, hi):
        self.root = root
        self.lo = lo
        self.hi = hi


BDDNODEZERO = _NODES[(-1, None, None)] = OBDDNode(-1, None, None)
BDDNODEONE = _NODES[(-2, None, None)] = OBDDNode(-2, None, None)


def obddvar(name, index=None):
    """Return a unique BDD variable.
    The "bddvar" function returns a unique Boolean variable instance
    represented by a binary decision diagram.
    Variable instances may be used to symbolically construct larger BDDs.
    """
    bvar = boolean.var(name, index)
    try:
        var = _VARS[bvar.uniqid]
    except KeyError:
        var = _VARS[bvar.uniqid] = OBDDVariable(bvar)
        _BDDS[var.node] = var
    return var


def _expr2obddnode(expr):
    """Convert an expression into a BDD node."""
    if expr.is_zero():
        return BDDNODEZERO
    elif expr.is_one():
        return BDDNODEONE
    else:
        top = expr.top
        # Register this variable
        _ = obddvar(top.names, top.indices)
        root = top.uniqid
        lo = _expr2obddnode(expr.restrict({top: 0}))
        hi = _expr2obddnode(expr.restrict({top: 1}))
        return _obddnode(root, lo, hi)


def expr2obdd(expr):
    """Convert an expression into a binary decision diagram."""
    return _obdd(_expr2obddnode(expr))


def _obddnode(root, lo, hi):
    """Return a unique BDD node."""
    if lo is hi:
        node = lo
    else:
        key = (root, lo, hi)
        try:
            node = _NODES[key]
        except KeyError:
            node = _NODES[key] = OBDDNode(*key)
    return node


def _obdd(node):
    """Return a unique BDD."""
    try:
        bdd = _BDDS[node]
    except KeyError:
        bdd = _BDDS[node] = OrderedBinaryDecisionDiagram(node)
    return bdd


class OrderedBinaryDecisionDiagram(boolean.Function):
    """Boolean function represented by a binary decision diagram

    * Convert an expression using the "expr2bdd" function.

    Use the "bddvar" function to create BDD variables,
    and use the Python "~|&^" operators for NOT, OR, AND, XOR.

    For example::
       >>> a, b, c, d = map(obddvar, "abcd")
       >>> f = ~a | b & c ^ d
    """

    def __init__(self, node):
        self.node = node

    # Operators
    def __invert__(self):
        return _obdd(_neg(self.node))

    def __or__(self, other):
        other_node = self.box(other).node
        # f | g <=> ITE(f, 1, g)
        return _obdd(_ite(self.node, BDDNODEONE, other_node))

    def __and__(self, other):
        other_node = self.box(other).node
        # f & g <=> ITE(f, g, 0)
        return _obdd(_ite(self.node, other_node, BDDNODEZERO))

    def __xor__(self, other):
        other_node = self.box(other).node
        # f ^ g <=> ITE(f, g', g)
        return _obdd(_ite(self.node, _neg(other_node), other_node))

    def __rshift__(self, other):
        other_node = self.box(other).node
        # f => g <=> ITE(f', 1, g)
        return _obdd(_ite(_neg(self.node), BDDNODEONE, other_node))

    def __rrshift__(self, other):
        other_node = self.box(other).node
        # f => g <=> ITE(f', 1, g)
        return _obdd(_ite(_neg(other_node), BDDNODEONE, self.node))

    @cached_property
    def inputs(self):
        inputs_ = []
        for node in self.dfs_postorder():
            if node.root > 0:
                v = _VARS[node.root]
                if v not in inputs_:
                    inputs_.append(v)
        return tuple(reversed(inputs_))

    def restrict(self, point):
        npoint = {v.node.root: self.box(val).node for v, val in point.items()}
        return _obdd(_restrict(self.node, npoint))

    def is_zero(self):
        return self.node is BDDNODEZERO

    def is_one(self):
        return self.node is BDDNODEONE

    @staticmethod
    def box(obj):
        if isinstance(obj, OrderedBinaryDecisionDiagram):
            return obj
        elif obj in (0, "0"):
            return BDDZERO
        elif obj in (1, "1"):
            return BDDONE
        else:
            return BDDONE if boolean(obj) else BDDZERO

    # Specific to BinaryDecisionDiagram
    def dfs_preorder(self):
        """Iterate through nodes in depth first search (DFS) pre-order."""
        yield from _dfs_preorder(self.node, set())

    def dfs_postorder(self):
        """Iterate through nodes in depth first search (DFS) post-order."""
        yield from _dfs_postorder(self.node, set())

    def equivalent(self, other):
        """Return whether this BDD is equivalent to *other*.

        You can also use Python's "is" operator for BDD equivalency testing.

        For example::

           >>> a, b, c = map(obddvar, "abc")
           >>> f1 = a ^ b ^ c
           >>> f2 = a & ~b & ~c | ~a & b & ~c | ~a & ~b & c | a & b & c
           >>> f1 is f2
           True
        """
        other = self.box(other)
        return self.node is other.node

    def to_dot(self, name="BDD"):  # pragma: no cover
        """Convert to DOT language representation(DOT language reference <http://www.graphviz.org/content/dot-language>).
        """
        parts = ["graph", name, "{"]
        for node in self.dfs_postorder():
            if node is BDDNODEZERO:
                parts += ["n" + str(id(node)), "[label=0,shape=box];"]
            elif node is BDDNODEONE:
                parts += ["n" + str(id(node)), "[label=1,shape=box];"]
            else:
                v = _VARS[node.root]
                parts.append("n" + str(id(node)))
                parts.append(f"[label=\"{v}\",shape=circle];")
        for node in self.dfs_postorder():
            if node is not BDDNODEZERO and node is not BDDNODEONE:
                parts += ["n" + str(id(node)), "--",
                          "n" + str(id(node.lo)),
                          "[label=0,style=dashed];"]
                parts += ["n" + str(id(node)), "--",
                          "n" + str(id(node.hi)),
                          "[label=1];"]
        parts.append("}")
        return " ".join(parts)


class BDDConstant(OrderedBinaryDecisionDiagram):
    """Binary decision diagram constant zero/one
    """

    def __init__(self, node, value):
        super().__init__(node)
        self.value = value

    def __bool__(self):
        return boolean(self.value)

    def __int__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.value)


BDDZERO = _BDDS[BDDNODEZERO] = BDDConstant(BDDNODEZERO, 0)
BDDONE = _BDDS[BDDNODEONE] = BDDConstant(BDDNODEONE, 1)


class OBDDVariable(boolean.Variable, OrderedBinaryDecisionDiagram):
    """Binary decision diagram variable

    The "BDDVariable" class is useful for type checking,
    e.g. "isinstance(f, BDDVariable)".

    Do **NOT** create a BDD using the "BDDVariable" constructor.
    Use the :func:`bddvar` function instead.
    """

    def __init__(self, bvar):
        boolean.Variable.__init__(self, bvar.names, bvar.indices)
        node = _obddnode(bvar.uniqid, BDDNODEZERO, BDDNODEONE)
        OrderedBinaryDecisionDiagram.__init__(self, node)


def _neg(node):
    """Return the inverse of *node*."""
    if node is BDDNODEZERO:
        return BDDNODEONE
    elif node is BDDNODEONE:
        return BDDNODEZERO
    else:
        return _obddnode(node.root, _neg(node.lo), _neg(node.hi))


def _ite(f, g, h):
    """Return node that results from recursively applying ITE(f, g, h)."""
    # ITE(f, 1, 0) = f
    if g is BDDNODEONE and h is BDDNODEZERO:
        return f
    # ITE(f, 0, 1) = f'
    elif g is BDDNODEZERO and h is BDDNODEONE:
        return _neg(f)
    # ITE(1, g, h) = g
    elif f is BDDNODEONE:
        return g
    # ITE(0, g, h) = h
    elif f is BDDNODEZERO:
        return h
    # ITE(f, g, g) = g
    elif g is h:
        return g
    else:
        # ITE(f, g, h) = ITE(x, ITE(fx', gx', hx'), ITE(fx, gx, hx))
        root = min(node.root for node in (f, g, h) if node.root > 0)
        npoint0 = {root: BDDNODEZERO}
        npoint1 = {root: BDDNODEONE}
        fv0, gv0, hv0 = [_restrict(node, npoint0) for node in (f, g, h)]
        fv1, gv1, hv1 = [_restrict(node, npoint1) for node in (f, g, h)]
        return _obddnode(root, _ite(fv0, gv0, hv0), _ite(fv1, gv1, hv1))


def _restrict(node, npoint, cache=None):
    """Restrict a subset of support variables to {0, 1}."""
    if node is BDDNODEZERO or node is BDDNODEONE:
        return node

    if cache is None:
        cache = {}

    try:
        ret = cache[node]
    except KeyError:
        try:
            val = npoint[node.root]
        except KeyError:
            lo = _restrict(node.lo, npoint, cache)
            hi = _restrict(node.hi, npoint, cache)
            ret = _obddnode(node.root, lo, hi)
        else:
            child = {BDDNODEZERO: node.lo, BDDNODEONE: node.hi}[val]
            ret = _restrict(child, npoint, cache)
        cache[node] = ret
    return ret


def _find_path(start, end, path=tuple()):
    """Return the path from start to end.
    If no path exists, return None.
    """
    path = path + (start,)
    if start is end:
        return path
    else:
        ret = None
        if start.lo is not None:
            ret = _find_path(start.lo, end, path)
        if ret is None and start.hi is not None:
            ret = _find_path(start.hi, end, path)
        return ret


def _iter_all_paths(start, end, rand=False, path=tuple()):
    """Iterate through all paths from start to end."""
    path = path + (start,)
    if start is end:
        yield path
    else:
        nodes = [start.lo, start.hi]
        if rand:  # pragma: no cover
            random.shuffle(nodes)
        for node in nodes:
            if node is not None:
                yield from _iter_all_paths(node, end, rand, path)


def _dfs_preorder(node, visited):
    """Iterate through nodes in DFS pre-order."""
    if node not in visited:
        visited.add(node)
        yield node
    if node.lo is not None:
        yield from _dfs_preorder(node.lo, visited)
    if node.hi is not None:
        yield from _dfs_preorder(node.hi, visited)


def _dfs_postorder(node, visited):
    """Iterate through nodes in DFS post-order."""
    if node.lo is not None:
        yield from _dfs_postorder(node.lo, visited)
    if node.hi is not None:
        yield from _dfs_postorder(node.hi, visited)
    if node not in visited:
        visited.add(node)
        yield node
