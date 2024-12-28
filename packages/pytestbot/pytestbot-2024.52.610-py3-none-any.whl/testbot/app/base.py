#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
from enum import IntEnum
from abc import abstractmethod, ABCMeta

from testbot.result.logger import logger_manager
from testbot.config import RUNNER_LOGS_PATH
from testbot.plugin.plugin_base import PluginManager
from testbot.result.testreporter import StepReporter


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
           -                                                    系统冒烟测试                                              SMOKE_TEST__SYSTEM                                  0b00110001
           -                                                    中间件冒烟测试                                             SMOKE_TEST__MIDDLEWARE                              0b00110010
        系统测试                                                                                                        SYSTEM_TEST                                           0b01000000
        稳定性测试                                                                                                      STABILITY_TEST                                      0b01000000
        性能测试                                                                                                       PERFORMANCE_TEST                                    0b01100000
        点检测试                                                                                                       CHECK_TEST                                           0b01110000
        接口测试                                                                                                       INTERFACE_TEST                                     0b10000000
        专项测试                                                                                                       SPECIAL_TEST                                        0b10000000
           -                                                    媒资专项测试                                             SPECIAL_TEST__MEDIA                                   0b10000001
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
    SMOKE_TEST__SYSTEM = 0b00110001
    # 中间件冒烟测试
    SMOKE_TEST__MIDDLEWARE = 0b00110010
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
    SPECIAL_TEST__MEDIA = 0b10000001
    # 通用测试
    COMMON_TEST = 0b11111111


class CheckItem(IntEnum):
    """
    检查项
    """
    # 是否有指令串口
    COMM_SERIAL_PORT_CHECK__EXIST = 0b00000000
    # 是否可以通过指令串口获取TV IP地址
    COMM_SERIAL_PORT_CHECK__HAS_IP = 0b00000001
    # TV端是否可以正常访问公司网络，如Panda、AI服务
    COMM_SERIAL_PORT_CHECK__ACCESS_INTERNAL_NET = 0b00000010
    # TV端是否可以正常访问国内网络
    COMM_SERIAL_PORT_CHECK__ACCESS_DOMESTIC_NET = 0b00000011
    # TV端是否可以正常访问海外网络
    COMM_SERIAL_PORT_CHECK__ACCESS_OVERSEAS_NET = 0b00000100
    # TV端的WIFI打开关闭是否正常
    COMM_SERIAL_PORT_CHECK__WIFI_NORMAL = 0b00000101
    # TV端是否有信源HTMI/TV
    COMM_SERIAL_PORT_CHECK__HAS_HDMI_SOURCE = 0b00000110

    # 是否有红外串口
    INFRA_SERIAL_PORT_CHECK__EXIST = 0b00010000
    # 通过红外串口发送红外指令是否正常
    INFRA_SERIAL_PORT_CHECK__NORMAL = 0b00010001

    # 是否有采集卡串口
    CAP_SERIAL_PORT_CHECK__EXIST = 0b00100000
    # 是否能够通过采集卡串口采集图像正常
    CAP_SERIAL_PORT_CHECK__NORMAL = 0b00100001

    # 是否有音频口
    AUDIO_PORT_CHECK__EXIST = 0b01000000
    # 音频口是否检测有声音
    AUDIO_PORT_CHECK__HAS_SOUND = 0b01000001

    # 是否有电源通断口
    POWER_PORT_CHECK__EXIST = 0b01010000

    # 是否有ADB无线连接
    ADB_WIRELESS_PORT_CHECK__EXIST = 0b01100000
    # 是否可以通过指令串口获取TV IP地址
    ADB_WIRELESS_PORT_CHECK__HAS_IP = 0b01100001
    # TV端是否可以正常访问公司网络，如Panda、AI服务
    ADB_WIRELESS_PORT_CHECK__ACCESS_INTERNAL_NET = 0b01100010
    # TV端是否可以正常访问国内网络
    ADB_WIRELESS_PORT_CHECK__ACCESS_DOMESTIC_NET = 0b01100011
    # TV端是否可以正常访问海外网络
    ADB_WIRELESS_PORT_CHECK__ACCESS_OVERSEAS_NET = 0b01100100
    # TV端的WIFI打开关闭是否正常
    ADB_WIRELESS_PORT_CHECK__WIFI_NORMAL = 0b01100101
    # TV端是否有信源HTMI/TV
    ADB_WIRELESS_PORT_CHECK__HAS_HDMI_SOURCE = 0b01100110

    # 是否有ADB有线连接
    ADB_WIRE_PORT_CHECK__EXIST = 0b01110000

    # 是否有gRPC连接
    GRPC_PORT_CHECK__EXIST = 0b10000000

    # 是否有网卡通断口
    ETHER_PORT_CHECK__EXIST = 0b10010000
    # 是否能够从PC端访问TV端的IP地址
    ETHER_PORT_CHECK__ACCESS_IP = 0b10010001

    # 是否有U盘通断口
    UDISK_PORT_CHECK__EXIST = 0b10100000
    # 是否有U盘插入
    UDISK_PORT_CHECK__HAS_UDISK = 0b10100001


# 测试类型检查清单
TESTTYPE_CHECKLIST = {
    # 点检测试类型
    TestType.CHECK_TEST.name: [
        # 是否有指令串口
        # CheckItem.COMM_SERIAL_PORT_CHECK__EXIST,
        # 是否可以通过指令串口获取TV IP地址
        CheckItem.COMM_SERIAL_PORT_CHECK__HAS_IP,
        # TV端是否可以正常访问公司网络，如Panda、AI服务
        CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_INTERNAL_NET,
        # TV端是否可以正常访问国内网络
        CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_DOMESTIC_NET,
        # TV端是否可以正常访问海外网络
        CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_OVERSEAS_NET,

        # 是否有红外串口
        # CheckItem.INFRA_SERIAL_PORT_CHECK__EXIST,
        # 通过红外串口发送红外指令是否正常
        CheckItem.INFRA_SERIAL_PORT_CHECK__NORMAL,

        # 是否有采集卡串口
        # CheckItem.CAP_SERIAL_PORT_CHECK__EXIST,
        # 是否能够通过采集卡串口采集图像正常
        CheckItem.CAP_SERIAL_PORT_CHECK__NORMAL,

        # 是否有ADB无线连接
        # CheckItem.ADB_WIRELESS_PORT_CHECK__EXIST,

        # 是否有gRPC连接
        # CheckItem.GRPC_PORT_CHECK__EXIST,
    ],
    # 系统冒烟测试类型
    TestType.SMOKE_TEST__SYSTEM.name: [
        # 是否有指令串口
        CheckItem.COMM_SERIAL_PORT_CHECK__EXIST,
        # 是否可以通过指令串口获取TV IP地址
        CheckItem.COMM_SERIAL_PORT_CHECK__HAS_IP,
        # TV端是否可以正常访问公司网络，如Panda、AI服务
        CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_INTERNAL_NET,
        # TV端是否可以正常访问国内网络
        CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_DOMESTIC_NET,
        # TV端是否可以正常访问海外网络
        CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_OVERSEAS_NET,

        # 是否有红外串口
        CheckItem.INFRA_SERIAL_PORT_CHECK__EXIST,
        # 通过红外串口发送红外指令是否正常
        CheckItem.INFRA_SERIAL_PORT_CHECK__NORMAL,

        # 是否有采集卡串口
        CheckItem.CAP_SERIAL_PORT_CHECK__EXIST,
        # 是否能够通过采集卡串口采集图像正常
        CheckItem.CAP_SERIAL_PORT_CHECK__NORMAL,

        # 是否有电源通断口
        CheckItem.POWER_PORT_CHECK__EXIST,

        # 是否有U盘通断口
        CheckItem.UDISK_PORT_CHECK__EXIST,
        # 是否有U盘插入
        CheckItem.UDISK_PORT_CHECK__HAS_UDISK,
    ]
}


class TestApplicationBase(metaclass=ABCMeta):
    """
    测试应用基类

    所有的测试应用必须继承该基类，需重写start方法
    """
    def __init__(self, **kwargs):
        self.reporter = kwargs.get("reporter", StepReporter.get_instance(logger=logger_manager.register("CaseRunner", filename=os.path.join(RUNNER_LOGS_PATH, "CaseRunner.log"), default_level="INFO", for_test=True)))
        self.__check_case, self.__tc_case = None, None
        with self.reporter.root.start_node(headline="执行测试", message="") as node:
            with node.start_case(headline="执行环境检查") as self.__check_case:
                pass
            with node.start_case(headline="执行测试用例") as self.__tc_case:
                pass
        self.pool = kwargs.get("pool", None)
        self.setting = None
        self.result = None
        # 执行环境检查
        self.check_env()
        # 初始化测试资源
        self.init_resource_pool()
        self.plugin_manager = PluginManager(step=self.__tc_case, pool=self.pool)
        self.plugin_manager.load()

    @property
    def _tc_case(self):
        return self.__tc_case

    @property
    def logger(self):
        return self.reporter.logger

    def init_resource_pool(self):
        """
        初始化测试资源池
        :return:
        :rtype:
        """
        self.logger.info(f"pool.topology = {self.pool.topology}")
        test_type = getattr(self, "test_type", None)
        self.logger.info(f"test_type = {test_type}")
        with self.__check_case.start(headline="执行资源初始化", message="", prefix="RUN_INIT") as step:
            for name, res_obj in self.pool.topology.items():
                if res_obj.type == "PCDevice":
                    res_obj.init_resource(test_type=test_type)
                if res_obj.type == "TVDevice":
                    res_obj.init_resource(test_type=test_type)

    def check_env(self):
        """
        检查测试环境

        :return:
        :rtype:
        """
        self.logger.info(f"pool.topology = {self.pool.topology}")
        test_type = getattr(self, "test_type", None)
        self.logger.info(f"test_type = {test_type}")
        checklist = TESTTYPE_CHECKLIST.get(test_type, [])
        with self.__check_case.start(headline="执行检查项", message="", prefix="RUN_CHECK") as step:
            pcs, tvs = list(), list()
            pcs = self.pool.collect_device(device_type="PCDevice", count=1)
            tvs = self.pool.collect_device(device_type="TVDevice", count=1)
            for checkitem in checklist:
                # 是否有指令串口
                if checkitem==CheckItem.COMM_SERIAL_PORT_CHECK__EXIST:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有指令串口")
                        step2.info(message="执行检查项：是否有指令串口")
                # 是否可以通过指令串口获取TV IP地址
                if checkitem==CheckItem.COMM_SERIAL_PORT_CHECK__HAS_IP:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否可以通过指令串口获取TV IP地址")
                        step2.info(message="执行检查项：是否可以通过指令串口获取TV IP地址")
                # TV端是否可以正常访问公司网络，如Panda、AI服务
                if checkitem==CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_INTERNAL_NET:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：TV端是否可以正常访问公司网络，如Panda、AI服务")
                        step2.info(message="执行检查项：TV端是否可以正常访问公司网络，如Panda、AI服务")
                # TV端是否可以正常访问国内网络
                if checkitem==CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_DOMESTIC_NET:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：TV端是否可以正常访问国内网络")
                        step2.info(message="执行检查项：TV端是否可以正常访问国内网络")
                # TV端是否可以正常访问海外网络
                if checkitem==CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_OVERSEAS_NET:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：TV端是否可以正常访问海外网络")
                        step2.info(message="执行检查项：TV端是否可以正常访问海外网络")

                # 是否有红外串口
                if checkitem==CheckItem.INFRA_SERIAL_PORT_CHECK__EXIST:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有红外串口")
                        step2.info(message="执行检查项：是否有红外串口")
                # 通过红外串口发送红外指令是否正常
                if checkitem==CheckItem.INFRA_SERIAL_PORT_CHECK__NORMAL:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：通过红外串口发送红外指令是否正常")
                        step2.info(message="执行检查项：通过红外串口发送红外指令是否正常")

                # 是否有采集卡串口
                if checkitem==CheckItem.CAP_SERIAL_PORT_CHECK__EXIST:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有采集卡串口")
                        step2.info(message="执行检查项：是否有采集卡串口")
                # 是否能够通过采集卡串口采集图像正常
                if checkitem==CheckItem.CAP_SERIAL_PORT_CHECK__NORMAL:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否能够通过采集卡串口采集图像正常")
                        step2.info(message="执行检查项：是否能够通过采集卡串口采集图像正常")

                # 是否有音频口
                if checkitem==CheckItem.AUDIO_PORT_CHECK__EXIST:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有音频口")
                        step2.info(message="执行检查项：是否有音频口")
                # 音频口是否检测有声音
                if checkitem==CheckItem.AUDIO_PORT_CHECK__HAS_SOUND:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：音频口是否检测有声音")
                        step2.info(message="执行检查项：音频口是否检测有声音")

                # 是否有电源通断口
                if checkitem==CheckItem.POWER_PORT_CHECK__EXIST:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有电源通断口")
                        step2.info(message="执行检查项：是否有电源通断口")

                # 是否有ADB无线连接
                if checkitem==CheckItem.ADB_WIRELESS_PORT_CHECK__EXIST:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有ADB无线连接")
                        step2.info(message="执行检查项：是否有ADB无线连接")

                # 是否有ADB有线连接
                if checkitem==CheckItem.ADB_WIRE_PORT_CHECK__EXIST:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有ADB有线连接")
                        step2.info(message="执行检查项：是否有ADB有线连接")

                # 是否有gRPC连接
                if checkitem==CheckItem.GRPC_PORT_CHECK__EXIST:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有gRPC连接")
                        step2.info(message="执行检查项：是否有gRPC连接")

                # 是否有网卡通断口
                if checkitem==CheckItem.ETHER_PORT_CHECK__EXIST:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有网卡通断口")
                        step2.info(message="执行检查项：是否有网卡通断口")
                # 是否能够从PC端访问TV端的IP地址
                if checkitem==CheckItem.ETHER_PORT_CHECK__ACCESS_IP:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否能够从PC端访问TV端的IP地址")
                        step2.info(message="执行检查项：是否能够从PC端访问TV端的IP地址")

                # 是否有U盘通断口
                if checkitem==CheckItem.UDISK_PORT_CHECK__EXIST:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有U盘通断口")
                        step2.info(message="执行检查项：是否有U盘通断口")
                # 是否有U盘插入
                if checkitem==CheckItem.UDISK_PORT_CHECK__HAS_UDISK:
                    with step.start(headline="", message="") as step2:
                        self.logger.info("执行检查项：是否有U盘插入")
                        step2.info(message="执行检查项：是否有U盘插入")
        pass

    def get_setting(self, setting_path, filename):
        """
        获取测试用例配置文件实例

        """
        for k,v in self.__class__.__dict__.items():
            if hasattr(v, "__base__") and v.__base__.__name__ == "TestSettingBase":
                self.setting = v(setting_path=setting_path, filename=filename)
                self.setting.load()

    @abstractmethod
    def start(self):
        pass
