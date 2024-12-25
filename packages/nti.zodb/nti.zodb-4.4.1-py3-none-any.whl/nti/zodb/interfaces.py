#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interfaces for objects defined in the ZODB package.

"""


__docformat__ = "restructuredtext en"

from zope import schema
from zope import interface

from zope.minmax.interfaces import IAbstractValue
from ZODB.POSException import StorageError

from nti.schema.field import Number

# pylint:disable=inherit-non-class,no-self-argument,no-method-argument
# pylint:disable=unexpected-special-method-signature
# mypy: ignore-errors

class ITokenBucket(interface.Interface):
    """
    A token bucket is used in rate limiting applications.
    It has a maximum capacity and a rate at which tokens are regenerated
    (typically this is in terms of absolute time).

    Clients attempt to consume tokens and are either allowed
    or denied based on whether there are enough tokens in the bucket.
    """

    fill_rate = schema.Float(title="The rate in tokens per second at which new tokens arrive.",
                             default=1.0,
                             min=0.0)
    capacity = schema.Float(title="The maximum capacity of the token bucket.",
                            min=0.0)

    tokens = schema.Float(title="The current number of tokens in the bucket at this instant.",
                          min=0.0)

    def consume(tokens=1):
        """
        Consume tokens from the bucket.

        :keyword tokens: The fractional number of tokens to consume. The default
                is to consume one whole token, which is probably what you want.

        :return: True if there were sufficient tokens, otherwise False.
                If True, then the value of `tokens` will have been reduced.
        """

    def wait_for_token():
        """
        Consume a single whole token from the bucket, blocking until one is available
        if need be. This is not meant to be used from multiple threads.
        """


class INumericValue(IAbstractValue):
    """
    A persistent numeric value with conflict resolution.
    """
    value = Number(title="The numeric value of this object.")

    def set(value):
        """
        Change the value of this object to the given value.

        If the number is immutable, and the value is not the current value,
        this may raise :exc:`NotImplementedError`.
        """

    def __eq__(other):
        """
        Is this object holding a value numerically equal to the other?
        """

    def __hash__():
        """
        This object hashes like its value.

        .. caution::
           Do not place this object in a hash container and then mutate the value.
        """

    def __lt__(other):
        """
        These objects are ordered like their values.
        """

    def __gt__(other):
        """
        These values are ordered like their values.
        """

    def increment(amount=1):
        """
        Increment the value by the specified amount (which should be non-negative).

        :return: The counter with the incremented value (this object).
        """

class INumericCounter(INumericValue):
    """
    A counter that can be incremented. Conflicts are resolved by
    merging the numeric value of the difference in magnitude of
    changes. Intended to be used for monotonically increasing
    counters, typically integers.
    """


class UnableToAcquireCommitLock(StorageError):
    """
    A ZODB storage (typically RelStorage) was unable
    to acquire the required commit lock.

    This class is only used if RelStorage is not available; otherwise
    it is an alias for
    ``relstorage.adapters.interfaces.UnableToAcquireCommitLock``.
    """

try:
    from relstorage.adapters import interfaces
except ImportError: # pragma: no cover
    pass
else:
    UnableToAcquireCommitLock = interfaces.UnableToAcquireCommitLockError  # alias pragma: no cover

ZODBUnableToAcquireCommitLock = UnableToAcquireCommitLock # BWC


###
# NOTE: For flexibility, it is possible to imagine defining an
# IZODBProvider object that returns a sequence of named IDatabase
# directly. We could then have an implementation of this that
# implements the "find the config providers"

class IZODBProvider(interface.Interface):
    """
    Provides zero or more ZODB :class:`ZODB.interfaces.IDatabase`
    objects to be registered as global components.

    This is a low-level interface that most people won't implement.
    Instead, see :class:`IZODBConfigProvider`.

    When this is implemented, it is intended to be registered as a
    global named utility. Some startup process is invoked to find all
    such utilities, invoke them, and register the resulting databases
    as global components. The API
    :func:`nti.zodb.config_providers.provideDatabases` is provided for
    this purpose.

    .. versionadded:: 4.3.0
    """

    def getDatabases():
        """
        Return a mapping of ``{name: (database, discriminator)}`` objects.

        Each *database* is meant to be registered as a global component
        with the given *name*.

        Equal *discriminator* values imply equal *database* values, and
        such equal values may be collapsed into a single *database* value.
        If you cannot determine discriminators, you may use
        a simple ``object``, but this will defeat the ability to detect
        multiples.
        """


class IZODBConfigProvider(interface.Interface):
    """
    Provides a ZODB configuration suitable for creating ZODB database
    object.

    The format of this configuration, and how it is accessed, is not
    defined. You are expected to provide an adapter from (a
    sub-interface of) this interface to
    :class:`ZODB.interfaces.IDatabase`.

    This package provides an implementation of :class:`IZODBProvider`
    that looks for named utilities of this interface, and
    adapts them to the databases to be returned from ``getDatabases``.

    .. important::
       For these utilities to be found, you must be sure to register
       them to provide exactly this interface, not the sub-interface
       they actually implement.

    This package provides one sub-interface, and the appropriate adapter;
    see :class:`IZODBZConfigProvider`

    .. versionadded:: 4.3.0
    """

    def getDiscriminator():
        """
        Return a hashable object that uniquely represents
        the database configuration this object holds.

        The intent is that equivalent databases can be detected this way and
        collapsed into a single entry. In this way we can support aliases.

        The return value is typically a string. If you are unable to
        create a unique discriminator, you may return an arbitrary
        hashable object.

        .. versionadded:: 4.4.0
        """


class IZODBZConfigProvider(IZODBConfigProvider):
    """
    This package provides an implementation of this interface for a
    temporary (in-memory) database in :mod:`.config_providers` as well
    as an implementation of the registration step in :func:`~.`.

    By default, the temporary database config provider is registered
    in the ``configure_configprovider.zcml`` file with the name
    \"mtemp\". No functionality in this package requires this, and you
    can use zope.configuration overrides to cancel this registration.

    The discriminator should typically be the same as the ZConfig string,
    assuming that it is produced deterministically.
    """

    def getZConfigString():
        """
        Return the ZConfig string to be passed to
        :func:`ZODB.config.databaseFromString`.
        """
