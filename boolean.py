"""
This module implements the fundamentals of Boolean variables and functions.
"""

import threading

VARIABLES = {}


def var(name, index=None):
    """
    Return a unique Variable instance.
    """
    if isinstance(name, str):
        names = (name,)
    elif isinstance(name, tuple):
        names = name
    else:
        raise TypeError(f"expected name to be a str or tuple, got {type(name).__name__}")

    if not names:
        raise ValueError("expected at least one name")

    for name_ in names:
        if not isinstance(name_, str):
            raise TypeError(f"expected name to be a str, got {type(name_).__name__}")

    if index is None:
        indices = tuple()
    else:
        if isinstance(index, int):
            indices = (index,)
        elif isinstance(index, tuple):
            indices = index
        else:
            raise TypeError(f"expected index to be an int or tuple, got {type(index).__name__}")

    for index_ in indices:
        if not isinstance(index_, int):
            raise TypeError(f"expected index to be an int, got {type(index_).__name__}")
        if index_ < 0:
            raise ValueError(f"expected index to be >= 0, got {index_}")

    try:
        v = VARIABLES[(names, indices)]
    except KeyError:
        v = Variable(names, indices)
        VARIABLES[(names, indices)] = v
    return v


_UNIQIDS = {}
_COUNT = 1


class Variable:
    """
    Base class for a symbolic Boolean variable.
    """

    def __init__(self, names, indices):
        global _UNIQIDS, _COUNT

        with threading.Lock():
            self.uniqid = _UNIQIDS.get((names, indices), _COUNT)
            if self.uniqid == _COUNT:
                _COUNT += 1
                _UNIQIDS[(names, indices)] = self.uniqid

        self.names = names
        self.indices = indices

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        suffix = f"[{','.join(map(str, self.indices))}]" if self.indices else ""
        return f"{self.qualname}{suffix}"

    def __lt__(self, other):
        if self.names == other.names:
            return self.indices < other.indices
        else:
            return self.names < other.names

    @property
    def name(self):
        """Return the innermost variable name."""
        return self.names[0]

    @property
    def qualname(self):
        """Return the fully qualified name."""
        return ".".join(reversed(self.names))


class Function:
    """
    Abstract base class that defines an interface for a symbolic Boolean function.
    """

    # Operators
    def __invert__(self):
        """Boolean negation operator"""
        raise NotImplementedError()

    def __or__(self, g):
        """Boolean disjunction (sum, OR) operator"""
        raise NotImplementedError()

    def __ror__(self, g):
        return self.__or__(g)

    def __and__(self, g):
        r"""Boolean conjunction (product, AND) operator"""
        raise NotImplementedError()

    def __rand__(self, g):
        return self.__and__(g)

    def __xor__(self, g):
        r"""Boolean exclusive or (XOR) operator"""
        raise NotImplementedError()

    def __rxor__(self, g):
        return self.__xor__(g)

    @property
    def inputs(self):
        """Return the support set in name/index order."""
        raise NotImplementedError()

    @property
    def top(self):
        """Return the first variable in the ordered support set."""
        if self.inputs:
            return self.inputs[0]
        else:
            return None
