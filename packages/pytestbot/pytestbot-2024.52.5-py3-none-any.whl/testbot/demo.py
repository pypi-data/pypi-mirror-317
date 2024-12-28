#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from typing import Optional


def Func1(a: int, b: Optional[str]) -> bool:
    """Func1 function.

    :param a: The first arg.
    :param b: The second arg.

    :returns: Something.
    """
    return False


def Func2(a: int, b: Optional[str]) -> bool:
    """Func1 function.

    :param a: The first arg.
    :param b: The second arg.

    :returns: Something.
    """
    return False


class Class1(object):
    """Class1 class.

    """
    def func1(self, a1: int) -> int:
        """func1 method.

        :param a1:
        :return:
        """
        return 0

    def func2(self, a1: int) -> int:
        """func2 method.

        :param a1:
        :return:
        """
        return 0

    @staticmethod
    def func3() -> bool:
        """ func3 method.

        :return:
        """
        return False
