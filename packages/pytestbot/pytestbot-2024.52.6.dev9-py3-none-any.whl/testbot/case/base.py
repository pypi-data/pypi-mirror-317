#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import json
import traceback
from enum import IntEnum
from abc import abstractmethod, ABCMeta

from testbot.resource.pool import ResourcePool
from testbot.result.logger import logger_manager
from testbot.result.testreporter import StepReporter
from testbot.result.testreporter import CaseEntry
from testbot.config import RUNNER_LOGS_PATH
from testbot.resource.error import ResourceNotMeetConstraintError


class TestType(IntEnum):
    """
    测试类型分类

    * 类型编码规则

    每个类型对应一个8位的二进制编码，前4位二进制表示主类，后4位二进制表示次类。如单元测试类型为0b00010000，0001为主类编码，0000为次类编码

    * 主类类型及编码

    测试类型的主类有：单元测试（0000）、沙盒测试（0001）、集成测试（0010）、冒烟测试（0011）、系统测试（0100）、稳定性测试（0101）、性能测试（0110）、点检测试（0111）、接口测试（1000）、专项测试（1001）、通用测试（1111）等

    * 次类类型及编码

    测试类型的次类，是主类类型的进一步分类，如系统冒烟测试，属于大类冒烟测试（0011），是其次类的一种类型，其测试类型编码为00110001

    * 测试类型列表

        ================================================   ================================================   ================================================   ================================================
        测试类型名称(主类型)                                    测试类型名称(次类型)                                                测试类型代码                                      测试类型编码
        ================================================   ================================================   ================================================   ================================================
        单元测试                                                                                                        UNIT_TEST                                              0b00000000
        沙盒测试                                                                                                       SANITY_TEST                                          0b00010000
        集成测试                                                                                                       INTEGRATION_TEST                                     0b00100000
        冒烟测试                                                                                                       SMOKE_TEST                                          0b00110000
           -                                                    系统冒烟测试                                              SMOKE_TEST_SYSTEM                                  0b00110001
           -                                                    中间件冒烟测试                                             SMOKE_TEST_MIDDLEWARE                              0b00110010
        系统测试                                                                                                        SYSTEM_TEST                                           0b01000000
        稳定性测试                                                                                                      STABILITY_TEST                                      0b01000000
        性能测试                                                                                                       PERFORMANCE_TEST                                    0b01100000
        点检测试                                                                                                       CHECK_TEST                                           0b01110000
        接口测试                                                                                                       INTERFACE_TEST                                     0b10000000
        专项测试                                                                                                       SPECIAL_TEST                                        0b10000000
           -                                                    媒资专项测试                                             SPECIAL_TEST_MEDIA                                   0b10000001
        通用测试                                                                                                       COMMON_TEST                                         0b11111111
        ================================================   ================================================   ================================================   ================================================
    """

    # 单元测试
    UNIT_TEST = 0b00000000
    # 沙盒测试
    SANITY_TEST = 0b00010000
    # 集成测试
    INTEGRATION_TEST = 0b00100000
    # 冒烟测试
    SMOKE_TEST = 0b00110000
    # 系统冒烟测试
    SMOKE_TEST_SYSTEM = 0b00110001
    # 中间件冒烟测试
    SMOKE_TEST_MIDDLEWARE = 0b00110010
    # 系统测试
    SYSTEM_TEST = 0b01000000
    # 稳定性测试
    STABILITY_TEST = 0b01010000
    # 性能测试
    PERFORMANCE_TEST = 0b01100000
    # 点检测试
    CHECK_TEST = 0b01110000
    # 接口测试
    INTERFACE_TEST = 0b10000000
    # 专项测试
    SPECIAL_TEST = 0b10000000
    # 媒资专项测试
    SPECIAL_TEST_MEDIA = 0b10000001
    # 通用测试
    COMMON_TEST = 0b11111111


class TestCaseBase(metaclass=ABCMeta):
    """
    测试用例基类

    用户应该实现以下3个方法：
        * collect_resource: 初始化资源对象
        * setup: 测试执行之前的初始化工作
        * test: 测试执行体
        * cleanup: 测试执行之后的清理工作
    """
    def __init__(self, **kwargs):
        self.reporter = kwargs.get("reporter", StepReporter.get_instance(logger=logger_manager.register("CaseRunner", filename=os.path.join(RUNNER_LOGS_PATH, "CaseRunner.log"), default_level="INFO", for_test=True)))
        self.logger = self.reporter.logger
        self._output_var = dict()
        self.setting = None
        self.test_data_var = dict()
        self.result = None

    @abstractmethod
    def collect_resource(self, node: CaseEntry, pool: ResourcePool):
        """
        初始化资源对象

        :param pool: 资源池
        :type pool: ResourcePool
        :return:
        :rtype:
        """
        pass

    def setup_class(self, node: CaseEntry, **kwargs):
        """
        执行测试之前的初始化工作

        :param args:
        :return:
        """
        pass

    @abstractmethod
    def setup(self, node: CaseEntry, **kwargs):
        """
        执行测试的每个循环之前的初始化工作

        :param args:
        :return:
        """
        pass

    @abstractmethod
    def test(self, node: CaseEntry, **kwargs):
        """
        测试执行体

        :param args:
        :return:
        """
        pass

    @abstractmethod
    def cleanup(self, node: CaseEntry, **kwargs):
        """
        执行每个循环之后的清理工作

        :param args:
        :return:
        """
        pass

    def cleanup_class(self, node: CaseEntry, **kwargs):
        """
        执行测试之后的清理工作

        :param args:
        :return:
        """
        pass

    @property
    def output_var(self):
        """
        The test case output variable
        Can be collected by Test Engine
        :return:
        """
        return self._output_var

    def get_setting(self, setting_path, filename):
        """
        获取测试用例配置文件实例

        """
        for k,v in self.__class__.__dict__.items():
            if hasattr(v, "__base__") and v.__base__.__name__ == "TestSettingBase":
                self.setting = v(setting_path=setting_path, filename=filename)
                self.setting.load()

    def _run_case(self, pool: ResourcePool, node: CaseEntry):
        """
        测试用例执行线程
        """
        node.info(message=self.__class__.__name__)
        _continue = True
        with node.start(headline="收集测试资源", message="", prefix="COLLECT_RESOURCE") as node2:
            pass
            try:
                self.logger.info(f"self.resource_pool={pool.topology}")
                self.collect_resource(node=node2, pool=pool)
            except ResourceNotMeetConstraintError as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                node2.info(message=f"测试资源不满足条件: {traceinfo}")
                _continue = False
            except Exception as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.logger.error(traceinfo)
                node2.info(message=f"捕获异常: {traceinfo}")
                _continue = False
            finally:
                pass

        if not _continue:
            return

        with node.start(headline="初始化前置条件", message="", prefix="SETUP") as node2:
            try:
                self.setup(node=node2)
            except Exception as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.logger.error(traceinfo)
                node2.info(message=f"捕获异常: {traceinfo}")
                self.__call_cleanup(node=node)
                return

        with node.start(headline="执行测试主体", message="", prefix="TEST") as node2:
            try:
                iterations = getattr(self.setting, "iterations", 1)
                self.logger.info(f"执行次数：{iterations}")
                for iteration in range(iterations):
                    with node2.start(headline=f"执行测试主体第{iteration}次", message="", prefix=f"TEST-{iteration}") as node3:
                        self.test(node=node3)
            except Exception as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.logger.error(traceinfo)
                node2.info(message=f"捕获异常: {traceinfo}")
                self.__call_cleanup(node=node)
                return

        self.__call_cleanup(node=node)

    def __call_cleanup(self, node: CaseEntry):
        """
        执行清除操作
        """
        with node.start(headline="清理后置条件", message="", prefix="CLEANUP") as node2:
            try:
                self.cleanup(node=node2)
            except Exception as ex:
                traceinfo = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
                self.logger.error(traceinfo)
                node2.info(message=f"捕获异常: {traceinfo}")
            finally:
                pass

    def start(self):
        pool = ResourcePool()
        reporter = StepReporter.get_instance(logger=self.logger)
        with reporter.root.start_node(headline="执行测试节点", message="").start_case(headline="执行测试用例") as node:
            self._run_case(pool=pool, node=node)
        self.logger.info(reporter.root.get_friend_print())
        self.logger.info(json.dumps(reporter.root.to_dict()))
