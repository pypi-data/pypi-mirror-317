#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_entry
from hamcrest import assert_that
from hamcrest import greater_than
from hamcrest import has_property
from hamcrest import none
from hamcrest import has_length

import struct
import unittest

import BTrees

from nti.zodb.containers import time_to_64bit_int

from nti.zodb.tests import SharedConfiguringTestLayer

from nti.testing.matchers import is_true
from nti.testing.matchers import is_false
from nti.testing.matchers import validly_provides

family = BTrees.family64

# pylint:disable=unnecessary-dunder-call

class TestContainer(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_negative_values_in_btree(self):
        bt = family.IO.BTree()

        for i in range(-1, -10000, -5):
            bt[time_to_64bit_int(i)] = str(i)

        for i in range(-1, -10000, -5):
            assert_that(bt, has_entry(time_to_64bit_int(i), str(i)))

    def test_positive_values_in_btree(self):
        bt = family.IO.BTree()

        for i in range(1, 10000, 10):
            bt[time_to_64bit_int(i)] = str(i)

        for i in range(1, 10000, 10):
            assert_that(bt, has_entry(time_to_64bit_int(i), str(i)))

    def test_increasing(self):

        prev = 0
        i = 1
        while i < 10000:

            ti = time_to_64bit_int(i)
            nti = time_to_64bit_int(-i)

            assert_that(ti, greater_than(time_to_64bit_int(prev)))
            assert_that(ti, greater_than(nti))

            prev = i
            i += 1.5

    def test_legacy_unsigned_pack_equivalent(self):
        # We used to pack with Q, now we pack with q.
        # Q was invalid for negative numbers, but we need to be
        # sure that q unpacks everything the same as it used to

        for i in range(1, 10000, 5):
            ti = struct.pack(b'!q', i)
            qti = struct.pack(b'!Q', i)

            assert_that(ti, is_(qti))

            uti = struct.unpack(b'!q', ti)[0]
            uqti = struct.unpack(b'!Q', qti)[0]

            assert_that(uti, is_(i))
            assert_that(uti, is_(uqti))

            assert_that(struct.unpack(b'!q', qti)[0],
                        is_(i))

class TestCaseInsensitiveBTreeContainer(unittest.TestCase):
    def _getFUT(self):
        from ..containers import CaseInsensitiveBTreeContainer as FUT
        return FUT

    def _makeOne(self):
        return self._getFUT()()

    def test_provides(self):
        from zope.container.interfaces import IContainer
        c = self._makeOne()
        assert_that(c, validly_provides(IContainer))

    @classmethod
    def checkCaseContainer(cls, c):
        from zope.container.contained import Contained as ZContained
        from zope.location.interfaces import ISublocations
        child = ZContained()
        c['UPPER'] = child
        assert_that(child, has_property('__name__', 'UPPER'))

        assert_that(c.__contains__(None), is_false())
        assert_that(c.__contains__('UPPER'), is_true())
        assert_that(c.__contains__('upper'), is_true())

        assert_that(c.__getitem__('UPPER'), is_(child))
        assert_that(c.__getitem__('upper'), is_(child))

        assert_that(list(iter(c)), is_(['UPPER']))
        assert_that(list(c.keys()), is_(['UPPER']))
        assert_that(list(c.keys('a')), is_(['UPPER']))
        assert_that(list(c.keys('A')), is_(['UPPER']))
        assert_that(list(c.iterkeys()), is_(['UPPER']))

        assert_that(list(c.items()), is_([('UPPER', child)]))
        assert_that(list(c.items('a')), is_([('UPPER', child)]))
        assert_that(list(c.items('A')), is_([('UPPER', child)]))


        assert_that(list(c.values()), is_([child]))
        assert_that(list(c.values('a')), is_([child]))
        assert_that(list(c.values('A')), is_([child]))


        del c['upper']
        assert_that(c.get(None), is_(none()))

        c['mykey'] = child
        assert_that(c, has_length(1))
        del c['MYKEY']
        assert_that(c, has_length(0))

        c.clear()
        assert_that(c, has_length(0))
        c['mykey'] = child
        assert_that(list(c.iterkeys()), has_length(1))
        assert_that(list(c.iterkeys('a', 'a')), has_length(0))

        c['otherkey'] = 2 # Some older versions excluded ints from sublocations
        assert_that(list(c.sublocations()), has_length(2))
        assert_that(list(ISublocations(c)), has_length(2))
        c.clear()
        assert_that(c, has_length(0))

    def test_case_insensitive_container(self):
        c = self._makeOne()
        self.checkCaseContainer(c)

    def test_key(self):
        from ..containers import CaseInsensitiveKey
        key = CaseInsensitiveKey('UPPER')
        assert_that(hash(key), is_(hash('upper')))

        assert_that(key.__gt__(CaseInsensitiveKey('z')),
                    is_(False))

    def test_case_insensitive_container_invalid_keys(self):
        c = self._makeOne()
        with self.assertRaises(TypeError):
            c.get({})
        with self.assertRaises(TypeError):
            c.get(1)

class TestCaseInsensitiveFolder(unittest.TestCase):
    def _getFUT(self):
        from ..containers import CaseInsensitiveFolder as FUT
        return FUT

    def _makeOne(self):
        return self._getFUT()()

    def test_provides(self):
        from zope.site.interfaces import IFolder
        assert_that(self._makeOne(), validly_provides(IFolder))

    def test_case_insensitive(self):
        TestCaseInsensitiveBTreeContainer.checkCaseContainer(self._makeOne())
