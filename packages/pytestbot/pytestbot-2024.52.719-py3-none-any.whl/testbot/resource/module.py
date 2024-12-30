#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模块基类列表
"""

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
from abc import ABCMeta

from testbot.result.logger import logger_manager
from testbot.config import MODULE_LOGS_PATH


class ModuleBase(metaclass=ABCMeta):
    """
    模块基类
    """

    def __init__(self, resource, *args: tuple, **kwargs: dict):
        self.resource = resource
        self.logger = kwargs.get("logger", self.resource.logger if self.resource and getattr(self.resource, "logger", None) else logger_manager.register(logger_name="Module", filename=os.path.join(MODULE_LOGS_PATH, "Module.log"), for_test=True))


class DeviceAtomModuleBase(ModuleBase):
    """
    测试设备资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(DeviceAtomModuleBase, self).__init__(resource, *args, **kwargs)


class DeviceWrapperModuleBase(DeviceAtomModuleBase):
    """
    测试设备资源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(DeviceWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class PCDeviceAtomModuleBase(DeviceAtomModuleBase):
    """
    PC测试设备源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(PCDeviceAtomModuleBase, self).__init__(resource, *args, **kwargs)


class PCDeviceWrapperModuleBase(PCDeviceAtomModuleBase):
    """
    PC测试设备源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(PCDeviceWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class AndroidDeviceAtomModuleBase(DeviceAtomModuleBase):
    """
    Android测试设备源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(AndroidDeviceAtomModuleBase, self).__init__(resource, *args, **kwargs)


class AndroidDeviceWrapperModuleBase(AndroidDeviceAtomModuleBase):
    """
    Android测试设备源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(AndroidDeviceWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class TCLTVDeviceAtomModuleBase(AndroidDeviceAtomModuleBase):
    """
    TCLTV测试设备源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TCLTVDeviceAtomModuleBase, self).__init__(resource, *args, **kwargs)


class TCLTVDeviceWrapperModuleBase(TCLTVDeviceAtomModuleBase):
    """
    TCLTV测试设备源封装接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TCLTVDeviceWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class SoftwareAtomModuleBase(ModuleBase):
    """
    测试软件资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(SoftwareAtomModuleBase, self).__init__(resource, *args, **kwargs)


class SoftwareWrapperModuleBase(SoftwareAtomModuleBase):
    """
    测试软件资源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(SoftwareWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class TATFSoftwareAtomModuleBase(SoftwareAtomModuleBase):
    """
    TATF测试软件资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TATFSoftwareAtomModuleBase, self).__init__(resource, *args, **kwargs)


class TATFSoftwareWrapperModuleBase(TATFSoftwareAtomModuleBase):
    """
    TATF测试软件资源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(TATFSoftwareWrapperModuleBase, self).__init__(resource, *args, **kwargs)


class ServiceAtomModuleBase(ModuleBase):
    """
    测试服务资源原子接口模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(ServiceAtomModuleBase, self).__init__(resource, *args, **kwargs)


class ServiceWrapperModuleBase(ServiceAtomModuleBase):
    """
    测试服务资源模块基类
    """
    def __init__(self, resource, *args: tuple, **kwargs: dict):
        super(ServiceWrapperModuleBase, self).__init__(resource, *args, **kwargs)
