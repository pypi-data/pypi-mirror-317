#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os
import time
import json

from testbot.result.logger import logger_manager
from testbot.resource.resource import ResourceError
from testbot.config import MODULE_LOGS_PATH
from testbot.config.static_setting import ResourceSetting
from testbot.resource.device.device import PCDevice, TVDevice
from testbot.resource.device.device import Device
from testbot.resource.constraint import ConnectionConstraint, ResourceNotMeetConstraint


class ResourcePool(object):
    """
    资源池类，负责资源的序列化和反序列化以及储存和读取
    """
    def __init__(self, *args, **kwargs):
        self.logger = kwargs.get("logger", logger_manager.register(logger_name="Resource", filename=os.path.join(MODULE_LOGS_PATH, "Resource.log"), for_test=True))
        self.topology = dict()
        self.reserved = None
        self.information = dict()
        self.file_name = None
        self.owner = None

    def add_device(self, device_name: str, **kwargs):
        """
        添加设备到资源池

        :param device_name: 设备名称
        :type device_name: str
        :param kwargs: 键值对参数
        :type kwargs: dict
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.add_device...")
        if device_name in self.topology:
            raise ResourceError(f"device {device_name} already exists")
        self.topology[device_name] = Device(device_name, **kwargs)
        self.logger.info(f"Exiting {self.__class__.__name__}.add_device...")

    def reserve(self):
        """
        占用当前资源

        :return:
        :rtype:
        """
        self.logger.info(f"Entering {self.__class__.__name__}.reserve...")
        if self.file_name is None:
            raise ResourceError("load a resource file first")
        self.load(self.file_name, self.owner)
        self.reserved = {"owner": self.owner, "date": time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())}
        self.save(self.file_name)
        self.logger.info(f"Exiting {self.__class__.__name__}.reserve...")

    def release(self):
        """
        释放当前资源

        :return:
        :rtype:
        """
        self.logger.info(f"Entering {self.__class__.__name__}.release...")
        if self.file_name is None:
            raise ResourceError("load a resource file first")
        self.load(self.file_name)
        self.reserved = None
        self.save(self.file_name)
        self.logger.info(f"Exiting {self.__class__.__name__}.release...")

    def collect_device(self, device_type, count, constraints=list()):
        ret = list()
        for key, value in self.topology.items():
            if value.type == device_type:
                for constraint in constraints:
                    if not constraint.is_meet(value):
                        break
                else:
                    ret.append(value)
            if len(ret) >= count:
                return ret
        else:
            return list()

    def collect_all_device(self, device_type, constraints=list()):
        ret = list()
        for key, value in self.topology.items():
            if value.type == device_type:
                for constraint in constraints:
                    if not constraint.is_meet(value):
                        break
                else:
                    ret.append(value)
        return ret

    def collect_connection_route(self, resource: str, constraints: list=list()) -> list:
        """
        获取资源连接路由

        :param resource:
        :type resource:
        :param constraints:
        :type constraints:
        :return: 链接路由
        :rtype: list
        """
        # 限制类必须是连接限制ConnectionConstraint
        for constraint in constraints:
            if not isinstance(constraint, ConnectionConstraint):
                raise ResourceError(
                    "collect_connection_route only accept ConnectionConstraints type")
        ret = list()
        for constraint in constraints:
            conns = constraint.get_connection(resource)
            if not any(conns):
                raise ResourceNotMeetConstraint([constraint])
            for conn in conns:
                ret.append(conn)
        return ret

    def load(self, filename: str, owner: str):
        """
        加载文件

        :param filename: 文件路径
        :type filename: str
        :param owner: 资源所有人
        :type owner: str
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.load...")
        # 检查文件是否存在
        if not os.path.exists(filename):
            # raise ResourceError(f"Cannot find file {filename}")
            self.save(filename=filename)
        self.file_name = filename

        # 初始化
        self.topology.clear()
        self.reserved = False
        self.information = dict()

        #读取资源配置的json字符串
        with open(filename) as file:
            json_object = json.load(file)

        #判断是否被占用
        # if "reserved" in json_object and json_object['reserved'] is not None and json_object['reserved']['owner'] != owner:
        #     raise ResourceError(f"Resource is reserved by {json_object['reserved']['owner']}")

        self.owner = owner

        if "info" in json_object:
            self.information = json_object['info']
        for key, value in json_object['devices'].items():
            res_obj = None
            resource_type = value.get("type", None)
            if resource_type == "PCDevice":
                res_obj = PCDevice.from_dict(dict_obj=value)
            if resource_type == "TVDevice":
                res_obj = TVDevice.from_dict(dict_obj=value)
            self.topology[key] = res_obj

        # 映射所有设备的连接关系
        for key, device in json_object['devices'].items():
            for port_name, port in device['ports'].items():
                for remote_port in port['remote_ports']:
                    remote_port_obj = self.topology[remote_port["device"]].ports[remote_port["port"]]
                    self.topology[key].ports[port_name].remote_ports.append(remote_port_obj)
        self.logger.info(f"topology={self.topology}")
        self.logger.info(f"Exiting {self.__class__.__name__}.load...")

    def save(self, filename: str):
        """
        保存文件

        :param filename: 文件路径
        :type filename: str
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.save...")
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, mode="w") as file:
            root_object = dict()
            root_object['devices'] = dict()
            root_object['info'] = self.information
            root_object['reserved'] = self.reserved
            for device_key, device in self.topology.items():
                root_object['devices'][device_key] = device.to_dict()
            json.dump(root_object, file, indent=4)
        self.logger.info(f"Exiting {self.__class__.__name__}.save...")

    def discover_resources(self):
        pass


def get_resource_pool(filename: str, owner: str) -> ResourcePool:
    """
    获取资源池，加载本地json文件以获取资源池，并设置该资源池的owner所有者

    :param filename: 资源池json文件路径
    :type filename: str
    :param owner: 资源所有者
    :type owner: str
    :return: 资源池对象
    :rtype: ResourcePool
    """
    ResourceSetting.load()
    full_name = os.path.join(ResourceSetting.resource_path, filename)
    rv = ResourcePool()
    rv.load(full_name, owner)
    return rv


if __name__ == "__main__":
    from testbot.resource.device import PCDevice, TVDevice
    pc = PCDevice(name="M70JP90W")
    tc = TVDevice(name="5C0AD0760BB0C50AD")

