#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for working with containers, particularly BTree containers.
"""

import struct

from functools import total_ordering
from functools import lru_cache

from zope.interface import implementer
from zope.location.interfaces import ISublocations
from zope.container.constraints import checkObject
from zope.container.contained import uncontained
from zope.container.btree import BTreeContainer

from zope.site.folder import Folder

# ! means network byte order, in case we cross architectures
# anywhere (doesn't matter), but also causes the sizes to be
# standard, which may matter between 32 and 64 bit machines
# q is 64-bit long int, d is 64-bit double

_float_to_double_bits = struct.Struct('!d').pack
_double_bits_to_long = struct.Struct('!q').unpack

_long_to_double_bits = struct.Struct('!q').pack
_double_bits_to_float = struct.Struct('!d').unpack


def time_to_64bit_int(value):
    """
    Given a Python floating point object (usually a time value),
    losslessly return a 64-bit long int that represents it. Useful for
    storing as the value in a OL tree, when you really want a float
    (since BTrees does not provide OF), or as a key in a Lx tree.
    """
    # Note that to handle negative values we must be signed,
    # otherwise we get ValueError from the btree
    if value is None:  # pragma: no cover
        raise ValueError("You must supply the lastModified value")
    return _double_bits_to_long(_float_to_double_bits(value))[0]

ZERO_64BIT_INT = time_to_64bit_int(0.0)


def bit64_int_to_time(value):
    """
    Convert a 64 bit integer to its floating point value.

    Inverse of :func:`time_to_64bit_int`.
    """
    return _double_bits_to_float(_long_to_double_bits(value))[0]

assert bit64_int_to_time(ZERO_64BIT_INT) == 0.0


@total_ordering
class CaseInsensitiveKey:
    """
    This class implements a dictionary key that preserves case, but
    compares case-insensitively. It works with unicode keys only (BTrees do not
    work if 8-bit and unicode are mixed).

    This is a bit of a heavyweight solution. It is nonetheless optimized for comparisons
    only with other objects of its same type.

    It must not be subclassed.

    .. versionadded:: 4.2.0
    """

    __slots__ = ('key',)

    def __init__(self, key):
        if not isinstance(key, str):
            raise TypeError(f'Expected a string, got a {key!r}')
        self.key = key

    @property
    def comp_key(self):
        """
        Returns the key to compare.
        """
        return self.key.casefold()

    def __str__(self):  # pragma: no cover
        return self.key

    def __repr__(self):  # pragma: no cover
        return "%s('%s')" % (self.__class__, self.key)

    # These should only ever be compared to themselves

    def __eq__(self, other):
        try:
            # pylint: disable=protected-access
            return other is self or other.comp_key == self.comp_key
        except AttributeError:  # pragma: no cover
            return NotImplemented

    def __hash__(self):
        return hash(self.comp_key)

    def __lt__(self, other):
        try:
            # pylint: disable=protected-access
            return self.comp_key < other.comp_key
        except AttributeError:  # pragma: no cover
            return NotImplemented


# These work best as plain functions so that the 'self'
# argument is not captured. The self argument is persistent
# and so that messes with caches
@lru_cache(10000)
def tx_key_insen(key):
    return CaseInsensitiveKey(key) if key is not None else None


class _CheckObjectOnSetMixin(object):
    """
    Works only with the standard BTree container.
    """

    def _setitemf(self, key, value):
        checkObject(self, key, value)
        super()._setitemf(key, value)


@implementer(ISublocations)
class CaseInsensitiveBTreeContainer(_CheckObjectOnSetMixin,
                                    BTreeContainer):
    """
    A BTreeContainer that only works with string (unicode) keys, and treats
    them in a case-insensitive fashion. The original case of the key entered is
    preserved.

    The underlying BTree is configured for large amounts of data.

    .. versionadded:: 4.2.0
    """

    # For speed, we generally implement all these functions directly in terms of the
    # underlying data; we know that's what the superclass does.

    # Note that the IContainer contract specifies keys that are strings. None
    # is not allowed.

    assert BTreeContainer._newContainerData
    def _newContainerData(self):
        from .btrees import family64LargeBuckets
        return family64LargeBuckets.OO.BTree() # pylint:disable=no-member


    def __contains__(self, key):
        return  key is not None \
            and tx_key_insen(key) in self._SampleContainer__data

    def __iter__(self):
        for k in self._SampleContainer__data:
            yield k.key

    def __getitem__(self, key):
        return self._SampleContainer__data[tx_key_insen(key)]

    def get(self, key, default=None):
        if key is None:
            return default
        return self._SampleContainer__data.get(tx_key_insen(key), default)

    def _setitemf(self, key, value):
        super()._setitemf(tx_key_insen(key), value)

    def __delitem__(self, key):
        # deleting is somewhat complicated by the need to broadcast
        # events with the original case
        l = self._BTreeContainer__len
        item = self[key]
        uncontained(item, self, item.__name__)
        del self._SampleContainer__data[tx_key_insen(key)]
        l.change(-1) # pylint: disable=no-member

    def items(self, key=None):
        key = tx_key_insen(key)
        return ((k.key, v) for k, v in self._SampleContainer__data.items(key))

    def keys(self, key=None):
        key = tx_key_insen(key)
        return (k.key for k in self._SampleContainer__data.keys(key))

    def values(self, key=None):
        key = tx_key_insen(key)
        return (v for v in self._SampleContainer__data.values(key))

    # pylint:disable=redefined-builtin
    def iterkeys(self, min=None, max=None, excludemin=False, excludemax=False):
        if max is None or min is None:
            return self.keys(min)
        min = tx_key_insen(min)
        max = tx_key_insen(max)
        container = self._SampleContainer__data
        return (k.key for k in container.keys(min, max, excludemin, excludemax))

    def sublocations(self):
        # We directly implement ISublocations instead of using the adapter for two reasons.
        # First, it's much more efficient as it saves the unwrapping
        # of all the keys only to rewrap them back up to access the data (the adapter
        # cannot assume the ``.values()`` method, so it has to ``for k in c: yield c[k]``)
        yield from self._SampleContainer__data.values()

    def clear(self):
        """
        Convenience method to clear the entire tree at one time.
        """
        if len(self) == 0:
            return
        for k in list(self.keys()):
            del self[k]

class CaseInsensitiveFolder(CaseInsensitiveBTreeContainer,
                            Folder):
    """
    A BTree folder that preserves case but otherwise ignores it.
    """
