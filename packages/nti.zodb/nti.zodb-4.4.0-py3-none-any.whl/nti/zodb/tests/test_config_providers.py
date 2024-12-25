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
        assert_that(named_db, has_properties(
            databases=is_(same_instance(default_db.databases))
        ))
        assert_that(named_db.databases, is_({
            '': default_db,
            'mtemp': named_db
        }))
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

    def test_provide_multi_identical(self):
        from zope import component
        from zope.processlifetime import DatabaseOpened

        from ZODB.interfaces import IDatabase

        from ..config_providers import provideDatabases


        events:list = []
        component.provideHandler(events.append, (None,))

        provideDatabases()
        # Because we detected that they were all identical,
        # we collapsed them to a single instance.
        default_db = component.getUtility(IDatabase)
        named_db = component.getUtility(IDatabase, "mtemp")
        named_db2 = component.getUtility(IDatabase, "mtemp2")

        assert_that(default_db, is_(same_instance(named_db)))
        assert_that(named_db, is_(same_instance(named_db2)))
        assert_that(named_db, has_properties(
            databases=is_(same_instance(named_db2.databases))
        ))
        assert_that(named_db.databases, is_({
            '': default_db,
            'mtemp': default_db,
            'mtemp2': default_db,
        }))

        # Still sent the db opened event this time.
        assert_that(events, has_length(4))
        assert_that([e for e in events if isinstance(e, DatabaseOpened)],
                    has_length(1))

    def test_provide_multi_distinct_with_root(self):
        from zope import component
        from zope.interface import implementer
        from zope.processlifetime import DatabaseOpened

        from ZODB.interfaces import IDatabase

        from ..interfaces import IZODBZConfigProvider
        from ..interfaces import IZODBConfigProvider
        from ..config_providers import provideDatabases


        events:list = []
        component.provideHandler(events.append, (None,))

        @implementer(IZODBZConfigProvider)
        class TempDBZConfigProvider:
            def getZConfigString(self):
                return """
                <zodb>
                    <mappingstorage />
                </zodb>
                """
            getDiscriminator = getZConfigString

        # We're not giving a name to this, so it becomes the default.
        component.provideUtility(TempDBZConfigProvider(), provides=IZODBConfigProvider)

        provideDatabases()
        # Because we detected that they were all identical,
        # we collapsed them to a single instance.
        default_db = component.getUtility(IDatabase)
        named_db = component.getUtility(IDatabase, "mtemp")
        named_db2 = component.getUtility(IDatabase, "mtemp2")

        assert_that(default_db, is_not(same_instance(named_db)))
        assert_that(named_db, is_(same_instance(named_db2)))
        assert_that(default_db, has_properties(
            databases=is_(same_instance(named_db2.databases))
        ))
        assert_that(named_db, has_properties(
            databases=is_(same_instance(named_db2.databases))
        ))
        assert_that(named_db.databases, is_({
            '': default_db,
            'mtemp': named_db,
            'mtemp2': named_db,
        }))

        # Still sent the db opened event this time.
        assert_that(events, has_length(4))
        assert_that([e for e in events if isinstance(e, DatabaseOpened)],
                    has_length(1))

    def test_provide_multi_distinct_no_root(self):
        from zope import component
        from zope.interface import implementer
        from zope.processlifetime import DatabaseOpened

        from ZODB.interfaces import IDatabase

        from ..interfaces import IZODBZConfigProvider
        from ..interfaces import IZODBConfigProvider
        from ..config_providers import provideDatabases


        events:list = []
        component.provideHandler(events.append, (None,))

        @implementer(IZODBZConfigProvider)
        class TempDBZConfigProvider:
            def getZConfigString(self):
                return """
                <zodb>
                    <mappingstorage />
                </zodb>
                """
            getDiscriminator = getZConfigString

        # We're ARE giving a name to this, so it DOES NOT become the default.
        component.provideUtility(TempDBZConfigProvider(),
                                 name="mapping",
                                 provides=IZODBConfigProvider)

        provideDatabases()
        # Because we detected that they were all identical,
        # we collapsed them to a single instance.
        default_db = component.queryUtility(IDatabase)
        named_db = component.getUtility(IDatabase, "mtemp")
        named_db2 = component.getUtility(IDatabase, "mtemp2")
        map_db = component.getUtility(IDatabase, "mapping")

        self.assertIsNone(default_db)

        assert_that(map_db, is_not(same_instance(named_db)))

        assert_that(named_db, is_(same_instance(named_db2)))
        assert_that(map_db, has_properties(
            databases=is_(same_instance(named_db2.databases))
        ))
        assert_that(named_db, has_properties(
            databases=is_(same_instance(named_db2.databases))
        ))
        assert_that(named_db.databases, is_({
            'mapping': map_db,
            'mtemp': named_db,
            'mtemp2': named_db,
        }))

        # No DatabaseOpened this time.
        assert_that(events, has_length(3))
        assert_that([e for e in events if isinstance(e, DatabaseOpened)],
                    has_length(0))


if __name__ == '__main__':
    unittest.main()
