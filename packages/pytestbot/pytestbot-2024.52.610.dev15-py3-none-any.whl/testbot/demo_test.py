#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


# coding: utf-8
import unittest
from testbot import demo


class SillyTest(unittest.TestCase):
    """SillyTest tests fun_to_test

    """

    def test_Func1(self):
        """Tests whether `Func1` is working properly

        """
        self.assertEqual(demo.Func1(1, 2), False)
