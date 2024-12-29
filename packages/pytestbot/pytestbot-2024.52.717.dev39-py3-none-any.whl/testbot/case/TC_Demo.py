#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

from testbot.case.decorator import case
from testbot.case.base import TestCaseBase


@case(priority=10, test_type="SystemSmoke")
class TC_ForceUpgrade(TestCaseBase):
    """
    强制升级
    """
    def setup(self):
        tv = self.resources.getTVDevice(tag="DUT")
        self.logger.debug("打印debug日志信息")
        self.settings
        self.reporter


    def test(self, test_data):
        rr = self.step_reporter
        with rr.root.start_node("整机-软件升级精简") as case:
            with case.start_node("从FTP服务器上下载升级包至U盘") as step:
                with case.start_node("解析脚本运行的命令参数") as sub_step:
                    if True:
                        sub_step.passed("成功解析脚本运行的命令参数")
                    else:
                        sub_step.failed("解析脚本运行的命令参数失败！")
                    try:
                        raise Exception("发生平台异常！")
                    except:
                        sub_step.errored("解析脚本运行的命令参数失败！")
                with case.start_node("切换USB-Port至PC端") as sub_step:
                    pass
                with case.start_node("获取PC端识别的U盘盘符") as sub_step:
                    pass
            with case.start_node("断开网络") as step:
                if True:
                    sub_step.passed("成功解析脚本运行的命令参数")
                else:
                    sub_step.failed("解析脚本运行的命令参数失败！")
                try:
                    raise Exception("发生平台异常！")
                except:
                    sub_step.errored("解析脚本运行的命令参数失败！")
            with case.start_node("获取项目配置的升级阶段的信息") as step:
                pass
            with case.start_node("切换USB端口至TV端") as step:
                pass
            with case.start_node("启动升级") as step:
                pass
            with case.start_node("检测强制升级过程以及升级结束后是否正常退出开机向导") as step:
                pass
            with case.start_node("开启串口并连接网络") as step:
                pass
            with case.start_node("检测升级版本") as step:
                pass
            with case.start_node("切换至TV信源") as step:
                pass

    def cleanup(self):
        pass
