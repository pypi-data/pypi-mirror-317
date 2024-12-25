# -*- coding: utf-8 -*-
"""
Implementations of, and helpers for, :class:`~.interfaces.IZODBZConfigProvider`

.. versionadded:: 4.3.0

"""
import logging
from typing import Any

import transaction

from zope.component import adapter
from zope.component import getGlobalSiteManager
from zope.interface import implementer
from zope.processlifetime import DatabaseOpened
from zope.event import notify

from ZODB.config import databaseFromString
from ZODB.interfaces import IDatabase

from nti.property.tunables import Tunable

from .interfaces import IZODBProvider
from .interfaces import IZODBConfigProvider
from .interfaces import IZODBZConfigProvider

logger = logging.getLogger(__name__)

@implementer(IZODBProvider)
class DatabaseProvider:
    """
    An aggregate IZODBProvider implementation based on all registered
    ``IZODBProvider`` objects.

    .. important::

        This object should not be registered in a component
        registry. Instead, use the module-level `provideDatabases`
        function.

    If we find only a single database, then it is registered both
    under its own name and as the global default database, unless the
    value of `REGISTER_SINGLE_AS_DEFAULT`` is set to false (through an
    environment variable often).

    If we register a database with the default name, whether because
    we were configured that way or because we copied a single named
    registration, the event
    :class:`zope.processlifetime.DatabaseOpened` event will be sent
    for that database.

    All databases found are registered with each other as a single
    multi-database. This includes existing databases.

    :raises ValueError: If a database name is duplicated, either by
        providers or with existing databases.

    .. rubric:: Simple Usage

    The typical use will look something like this. You'll need:

            - One or more named registered ``IZODBConfigProvider``
              utilities. It is important it is registered for exactly
              this interface. If you can express your configuration in
              ZConfig (most configuration can be expressed that way),
              implement ``IZODBZConfigProvider``.

            - A registered ``IZODBConfigProvider`` to
              ``IDatabase`` adapter. If you implement
              ``IZODBZConfigProvider``, this is already given.

            - To call :func:`provideDatabases` during your process
              startup, after component registration.

    You may also choose to just register one or more direct
    implementations of ``IZODBProvider`` if you cannot express
    your database any other way.
    """

    REGISTER_SINGLE_AS_DEFAULT = Tunable(
        True,
        env_name="NTI_ZODB_REGISTER_SINGLE_AS_DEFAULT",
        getter="boolean",
    )

    def _check_and_update_existing_databases(self, dbs):
        # Refuse to overwrite existing databases
        gsm = getGlobalSiteManager()
        existing_databases = dict(gsm.getUtilitiesFor(IDatabase))
        for name, db in existing_databases.items():
            if name in dbs:
                if name == '' and len(dbs) == 2 and len({id(v) for v in dbs.values()}) == 1:
                    # There is a default Db registered. We only found
                    # one component registration, and it was for a
                    # named DB that we're trying to make the default.
                    # Well, we have a default, so don't do that.
                    dbs.pop('')
                    continue
                raise ValueError("Database name %r already registered." % (name,))

        dbs.update(existing_databases)
        # Update them to be sure they also have the right name and databases.
        for name, db in existing_databases.items():
            db.database_name = name
            db.databases = dbs

        return existing_databases

    def _collect_provided_dbs(self) -> dict[str,tuple[IDatabase,object]]:
        gsm = getGlobalSiteManager()
        # Collect non-overlapping databases.
        dbs:dict[str,tuple[IDatabase,object]] = {}
        for _name, db_provider in gsm.getUtilitiesFor(IZODBProvider):
            provider_dbs = db_provider.getDatabases()
            for k in provider_dbs:
                if k in dbs: # pragma: no cover
                    raise ValueError("Database name %r already provided" % (k,))
            dbs |= provider_dbs
        return dbs

    def getDatabases(self):
        """
        See the documentation for :class:`DatabaseProvider`.

        .. versionchanged:: 4.4.0
           Return the mapping of databases as expected.
        """
        discr_dbs = self._collect_provided_dbs()
        # Now we implicitly discard duplicates based on discriminator
        by_discriminator = {
            discr: db
            for db, discr
            in discr_dbs.values()
        }
        dbs:dict[str,Any] = {
            name: by_discriminator[discr]
            for name, (_db, discr)
            in discr_dbs.items()
        }


        if len(by_discriminator) == 1 and self.REGISTER_SINGLE_AS_DEFAULT:
            # Only one distinct database connection, but we will register
            # under multiple aliases
            name = next(iter(dbs))
            db = dbs[name]
            db.database_name = ''
            db.databases = dbs
            dbs[''] = db
        else:
            # These all constitute a multi-database; be sure they all know their own
            # names.
            for name, db in dbs.items():
                db.database_name = name
                db.databases = dbs

        # Add the existing to the multi-db, and confirm no name
        # overlaps.
        existing_databases = self._check_and_update_existing_databases(dbs)
        assert all(d.databases is dbs for d in existing_databases.values())

        # Register the new ones. Don't also re-register existing ones
        # because that will send a bunch of notifications we don't want to
        # process twice.
        gsm = getGlobalSiteManager()
        for name, db in dbs.items():
            if name in existing_databases:
                continue
            gsm.registerUtility(db, provided=IDatabase, name=name)

        if '' in dbs and '' not in existing_databases:
            root_db = dbs['']
            notify(DatabaseOpened(root_db))

        return dbs


provideDatabases = DatabaseProvider().getDatabases


@implementer(IZODBProvider)
class ZODBConfigProviderDBProvider:
    """
    Uses registered :class:`IZODBConfigProvider` utilities
    to implement :class:`IZODBProvider`.
    """

    def getDatabases(self):
        gsm = getGlobalSiteManager()

        providers = dict(gsm.getUtilitiesFor(IZODBConfigProvider))

        # Because we only pick up exact registartions for that type --- not
        # sub-interfaces --- we are guaranteed that names will never be duplicated.

        # NOTE: We need to do this (instead of a simple call to
        # ``IDatabase()``) so that we can use transaction retries
        # around creating the database --- doing so accesses the
        # storage and tries to create the root object, but if multiple
        # processes do so against a shared database (RelStorage) we
        # may get conflicts that need retried.
        #
        # The database uses its own isolated transaction manager to handle
        # the initial root creation, but it's OK that we use an attempts() mechanism
        # from the outer manager -- we just need the loop and retry logic.
        def make_one(provider):
            for attempt in transaction.attempts():
                with attempt:
                    return IDatabase(provider)

        dbs = {
            name: (make_one(provider), provider.getDiscriminator())
            for name, provider
            in providers.items()
        }
        return dbs




@implementer(IZODBZConfigProvider)
class InMemoryDemoStorageZConfigProvider:
    """
    Provides the ZConfig for a temporary database.

    This database will be a ``DemoStorage`` on top of
    an in-memory storage. It *does not* support blobs.
    """
    # Explicitly named in-memory because we can imagine a
    # temporary database based on a FileStorage/RelStorage sqlite
    # in a temporary directory somewhere. That would allow
    # supporting blobs. Uses of this config provider should
    # be sure to include something about "memory" in their name,
    # e.g., IDatabase() named mtemp.

    # We implement this through ZConfig instead of directly as a
    # ZODBProvider for two reasons: First, to allow disabling it
    # or easily using it with a different name than the default
    # registration (IZODBProvider doesn't let the ZCML file dictate
    # the name of the generated databases).
    # Second, doing it this way provides a full end-to-end test
    # of the ``provideDatabases -> ZODBConfigProviderDBProvider``
    # pipeline.

    # TODO: This could easily be configured to provide blobs
    # by wrapping a ``<blobstorage>`` around the demo storage.
    def getZConfigString(self):
        return """
        <zodb>
            <demostorage />
        </zodb>
        """

    getDiscriminator = getZConfigString


@implementer(IDatabase)
@adapter(IZODBZConfigProvider)
def zconfig_provider_to_database(config_provider):
    return databaseFromString(config_provider.getZConfigString())
