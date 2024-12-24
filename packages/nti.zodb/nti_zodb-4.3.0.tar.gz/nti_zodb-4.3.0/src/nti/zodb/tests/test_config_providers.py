# -*- coding: utf-8 -*-
"""
Tests for config_providers.py

"""

import unittest

from nti.testing.base import ConfiguringTestBase
from nti.testing.matchers import verifiably_provides

from hamcrest import assert_that
from hamcrest import has_length
from hamcrest import has_properties
from hamcrest import is_
from hamcrest import is_not
from hamcrest import same_instance


class TestInMemoryDemoStorageZConfigProvider(unittest.TestCase):

    def _getFUT(self):
        from ..config_providers import InMemoryDemoStorageZConfigProvider as FUT
        return FUT

    def _makeOne(self):
        return self._getFUT()()

    def test_provides(self):
        from ..interfaces import IZODBZConfigProvider
        inst = self._makeOne()
        assert_that(inst, verifiably_provides(IZODBZConfigProvider))


class TestZConfigProviderToDatabase(ConfiguringTestBase):
    set_up_packages = (__name__,)

    def test_adapts(self):
        from ZODB.interfaces import IDatabase
        from ZODB.interfaces import IStorage

        from ..config_providers import InMemoryDemoStorageZConfigProvider as ZCP

        db = IDatabase(ZCP())
        # The DB itself doesn't validly provide IDatabase :(
        assert_that(db.storage, verifiably_provides(IStorage))



class TestProvideDatabases(ConfiguringTestBase):
    set_up_packages = (__name__,)

    def test_provide_temp_database(self):
        from zope import component
        from zope.processlifetime import DatabaseOpened
        from ZODB.interfaces import IDatabase

        from ..config_providers import provideDatabases

        events:list = []
        component.provideHandler(events.append, (None,))

        provideDatabases()
        # Because it's the only database provided, it
        # is registered both under its choosen name, and the
        # default name.
        default_db = component.getUtility(IDatabase)
        named_db = component.getUtility(IDatabase, "mtemp")

        assert_that(named_db, is_(same_instance(default_db)))
        # We sent an event
        # registered mtemp, registered '', DatabaseOpened
        assert_that(events, has_length(3))
        assert_that(events[-1], is_(DatabaseOpened))

        # Doing it again refuses to change anything, all names are duplicated
        with self.assertRaisesRegex(ValueError, 'already registered'):
            provideDatabases()

    def test_with_existing(self):
        from zope import component
        from ZODB.interfaces import IDatabase
        from ..config_providers import InMemoryDemoStorageZConfigProvider as ZCP
        from ..config_providers import provideDatabases

        db = IDatabase(ZCP())

        component.provideUtility(db, IDatabase)
        provideDatabases()

class TestProvideMultiDatabase(ConfiguringTestBase):
    set_up_packages = (('prov_multi.zcml', __name__),)

    def test_provide_multi(self):
        from zope import component
        from zope.processlifetime import DatabaseOpened

        from ZODB.interfaces import IDatabase

        from ..config_providers import provideDatabases


        events:list = []
        component.provideHandler(events.append, (None,))

        provideDatabases()
        # This time, no default is provided
        default_db = component.queryUtility(IDatabase)
        named_db = component.getUtility(IDatabase, "mtemp")
        named_db2 = component.getUtility(IDatabase, "mtemp2")

        self.assertIsNone(default_db)
        assert_that(named_db, is_not(same_instance(named_db2)))
        assert_that(named_db, has_properties(
            databases=is_(same_instance(named_db2.databases))
        ))

        # No databaseOpened event this time.
        assert_that(events, has_length(2))
        assert_that([e for e in events if isinstance(e, DatabaseOpened)],
                    has_length(0))

if __name__ == '__main__':
    unittest.main()
