#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) TCL DIGITAL TECHNOLOGY (SHENZHEN) CO., LTD."
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@tcl.com"


import os
import sys

package_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(package_path, ".."))

import argparse

from testbot.config import CONFIG_PATH
from testbot.controller.manager import run_test, init_engine, load_settings, load_resource, load_test_list


def init_test():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--testlist", type=str, dest="testlist",
                        help="Test list file", required=True)
    parser.add_argument("-r", "--resource", type=str, dest="resource",
                        help="Test Resource file", required=True)
    parser.add_argument("-u", "--user", type=str, dest="user",
                        help="User Name", required=False)

    args = parser.parse_args()

    load_settings(CONFIG_PATH)
    init_engine()
    load_resource(args.resource, args.user)
    load_test_list(args.testlist)


def main():
    init_test()
    run_test()


if __name__ == '__main__':
    main()
