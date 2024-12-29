#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"

import os

import cv2
import grpc
import serial
import importlib
import adbutils
from abc import ABCMeta, abstractmethod

from testbot.result.logger import logger_manager
from testbot.resource.module import ModuleBase
from testbot.config import MODULE_LOGS_PATH
from testbot.app.base import TESTTYPE_CHECKLIST, CheckItem, TestType

# 存放用户注册的配置接口对象类型
_resource_device_mapping = dict()
_resource_port_mapping = dict()


class ResourceError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def register_resource(category, resource_type, comm_callback):
    """
    注册配置接口实例化的方法或者类。
    """
    if category == "device":
        _resource_device_mapping[resource_type] = comm_callback
    elif category == "port":
        _resource_port_mapping[resource_type] = comm_callback


class Resource(metaclass=ABCMeta):
    """
    代表所有测试资源设备的配置类，字段动态定义
    """
    name: str
    type: str
    description: str

    # 接口模块类列表
    MODULES = []

    @classmethod
    def register_module(cls, module: str):
        """
        注册接口模块类

        :param module: 接口模块类包路径
        :type module: str
        :return:
        :rtype:
        """
        if module not in cls.MODULES:
            cls.MODULES.append(module)

    def __init__(self, name: str, *args, **kwargs):
        self.logger = kwargs.get("logger", logger_manager.register(logger_name="Resource",
                                                                   filename=os.path.join(MODULE_LOGS_PATH,
                                                                                         "Resource.log"),
                                                                   for_test=True))
        self.ports = dict()
        self.logger.info(f"加载{self.__class__}接口模块类{self.__class__.MODULES}")
        for mod in tuple(self.__class__.MODULES):
            mod_pkg = ".".join(mod.split(".")[0:-1])
            mod_clazz = mod.split(".")[-1]
            mod_cls = getattr(importlib.import_module(mod_pkg), mod_clazz)
            if not issubclass(mod_cls, ModuleBase):
                raise Exception(
                    f"{mod_cls.__name__}类不是接口模块类ModuleBase的子类！请检查资源类{self.__class__.__name__}的MODULES模块类列表！！")
            setattr(self, mod_cls.__name__, mod_cls(resource=self, logger=self.logger))

        self.name = name
        self.type = kwargs.get("type", None)
        self.description = kwargs.get("description", None)
        self.pre_connect = False
        self.client_attributes = dict()
        self.shared_attributes = dict()
        self.server_attributes = dict()
        self.reserved = False

    def __del__(self):
        instance = getattr(self, "_instance", None)
        if instance:
            try:
                if instance.isOpen():
                    instance.close()
            except:
                pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        预留序列化接口，即将Resource对象序列化为字典对象

        :return: 序列化后的字典对象
        :rtype: dict
        """
        return dict()

    @classmethod
    def from_dict(cls, dict_obj):
        """
        预留反序列化接口，即从字典对象反序列化为Resource对象

        :return: 反序列化后的Resource对象
        :rtype: Resource
        """
        return None

    def get_port(self, type):
        self.logger.info(f"self={self.ports}")
        for name, port in self.ports.items():
            self.logger.info(f"name, port={name}, {port}")
            if port.type == type:
                for _port in port.remote_ports:
                    self.logger.info(f"_port={_port}")
                    if _port.type == type:
                        return _port
        return None

    def init_resource(self, test_type: TestType):
        """
        初始化测试资源

        :return:
        :rtype:
        """
        self.logger.info(f"初始化测试资源:{self.__class__.__name__}(name={self.name},type={self.type}).init_resource")
        checklist = TESTTYPE_CHECKLIST.get(test_type, [])
        self.logger.info(f"检查项列表：{checklist}，测试类型：{test_type}")
        for checkitem in checklist:
            self.logger.info(f"检查项：{checkitem.name}")
            # 是否有指令串口
            if checkitem == CheckItem.COMM_SERIAL_PORT_CHECK__EXIST:
                if self.type == "PCDevice":
                    for name, port in self.ports.items():
                        if port.type == "CommSerialPort":
                            self.logger.info(f"测试端口{name}:{port.type}的端口对象{port.to_dict()}进行初始化")
                            port.init_resource(test_type=test_type)
                if self.type == "CommSerialPort":
                    self.logger.info(f"端口信息：{self.to_dict()}")
                    self.logger.info(f"波特率：{self.baud_rate}")
                    self._instance = serial.Serial(port=self.name, baudrate=self.baud_rate, timeout=1)

            # 是否可以通过指令串口获取TV IP地址
            if checkitem == CheckItem.COMM_SERIAL_PORT_CHECK__HAS_IP:
                pass
            # TV端是否可以正常访问公司网络，如Panda、AI服务
            if checkitem == CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_INTERNAL_NET:
                pass
            # TV端是否可以正常访问国内网络
            if checkitem == CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_DOMESTIC_NET:
                pass
            # TV端是否可以正常访问海外网络
            if checkitem == CheckItem.COMM_SERIAL_PORT_CHECK__ACCESS_OVERSEAS_NET:
                pass

            # 是否有红外串口
            if checkitem == CheckItem.INFRA_SERIAL_PORT_CHECK__EXIST:
                if self.type == "PCDevice":
                    for name, port in self.ports.items():
                        if port.type == "InfraredSerialPort":
                            self.logger.info(f"测试端口{name}:{port.type}的端口对象{port.to_dict()}进行初始化")
                            port.init_resource(test_type=test_type)
                if self.type == "InfraredSerialPort":
                    self.logger.info(f"端口信息：{self.to_dict()}")
                    self._instance = serial.Serial(port=self.name, baudrate=self.baud_rate, timeout=1)

            # 通过红外串口发送红外指令是否正常
            if checkitem == CheckItem.INFRA_SERIAL_PORT_CHECK__NORMAL:
                pass

            # 是否有采集卡串口
            if checkitem == CheckItem.CAP_SERIAL_PORT_CHECK__EXIST:
                if self.type == "PCDevice":
                    for name, port in self.ports.items():
                        if port.type == "VideoStreamSerialPort":
                            self.logger.info(f"测试端口{name}:{port.type}的端口对象{port.to_dict()}进行初始化")
                            port.init_resource(test_type=test_type)
                if self.type == "VideoStreamSerialPort":
                    self.logger.info(f"端口信息：{self.to_dict()}")
                    self._instance = cv2.VideoCapture(int(self.name))
                    self._instance.set(cv2.CAP_PROP_FRAME_WIDTH, 1920.0)  # 画面帧宽度
                    self._instance.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080.0)  # 画面帧高度
                    self._instance.set(cv2.CAP_PROP_FPS, getattr(self, "fps", 30.0))  # 帧率
                    self._instance.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 缓存帧数，返回False不支持缓冲区设置
                    self._instance.isOpened()
                    self._instance.grab()
                    if not self._instance.isOpened() or not self._instance.grab():
                        raise Exception("Capture enable failed！")

            # 是否能够通过采集卡串口采集图像正常
            if checkitem == CheckItem.CAP_SERIAL_PORT_CHECK__NORMAL:
                pass

            # 是否有音频口
            if checkitem == CheckItem.AUDIO_PORT_CHECK__EXIST:
                pass
            # 音频口是否检测有声音
            if checkitem == CheckItem.AUDIO_PORT_CHECK__HAS_SOUND:
                pass

            # 是否有电源通断口
            if checkitem == CheckItem.POWER_PORT_CHECK__EXIST:
                pass

            # 是否有ADB无线连接
            if checkitem == CheckItem.ADB_WIRELESS_PORT_CHECK__EXIST:
                if self.type == "PCDevice":
                    for name, port in self.ports.items():
                        if port.type == "AdbPort":
                            self.logger.info(f"测试端口{name}:{port.type}的端口对象{port.to_dict()}进行初始化")
                            port.init_resource(test_type=test_type)
                if self.type == "AdbPort":
                    self.logger.info(f"端口信息：{self.to_dict()}")
                    # 建立adb connect连接
                    self.logger.info(f"IP={self.name}")
                    adbutils.adb.connect(addr=self.name, timeout=5)
                    # 获取adb客户端对象
                    self._instance = adbutils.AdbClient(host="127.0.0.1", port=5037)

            # 是否有ADB有线连接
            if checkitem == CheckItem.ADB_WIRE_PORT_CHECK__EXIST:
                pass

            # 是否有gRPC连接
            if checkitem == CheckItem.GRPC_PORT_CHECK__EXIST:
                if self.type == "PCDevice":
                    for name, port in self.ports.items():
                        if port.type == "GRPCPort":
                            self.logger.info(f"测试端口{name}:{port.type}的端口对象{port.to_dict()}进行初始化")
                            self.logger.info(f"ports={self.ports}")
                            port.init_resource(test_type=test_type)
                if self.type == "GRPCPort":
                    self.logger.info(f"端口信息：{self.to_dict()}")
                    self._instance = grpc.insecure_channel(self.name)
                    self.logger.info(f"port_obj={self}")

            # 是否有网卡通断口
            if checkitem == CheckItem.ETHER_PORT_CHECK__EXIST:
                pass
            # 是否能够从PC端访问TV端的IP地址
            if checkitem == CheckItem.ETHER_PORT_CHECK__ACCESS_IP:
                pass

            # 是否有U盘通断口
            if checkitem == CheckItem.UDISK_PORT_CHECK__EXIST:
                pass
            # 是否有U盘插入
            if checkitem == CheckItem.UDISK_PORT_CHECK__HAS_UDISK:
                pass
        pass


class Device(Resource):
    """
    代表所有测试设备类
    """
    # 接口模块类列表
    MODULES = []

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)
        self.logger.info("Initialize Device...")
        self._instance = None

    def add_port(self, name: str, *args: tuple, **kwargs: dict):
        """
        添加端口

        :param name: 端口名称
        :type name: str
        :param args: 元祖参数
        :type args: tuple
        :param kwargs: 键值对参数
        :type kwargs: dict
        :return: None
        :rtype: NoneType
        """
        self.logger.info(f"Entering {self.__class__.__name__}.add_port...")
        if name in self.ports:
            raise ResourceError(f"Port Name {name} already exists")
        self.ports[f"{name}"] = Port(parent_device=self, name=name, *args, **kwargs)
        self.logger.info(f"Exiting {self.__class__.__name__}.add_port...")

    def get_port_count(self, **kwargs: dict):
        """
        获取端口数量

        :param kwargs: 键值对参数
        :type kwargs: dict
        :return: 端口数量
        :rtype: int
        """
        return len(self.ports)

    def to_dict(self):
        ret = dict()
        for key, value in self.__dict__.items():
            if key in ["__instance", "logger"]:
                continue
            if key == "ports":
                ret[key] = dict()
                for port_name, port in value.items():
                    ret[key][port_name] = port.to_dict()
            else:
                ret[key] = value
        return ret

    def get_comm_instance(self, new=False):
        if self.type not in _resource_device_mapping:
            raise ResourceError(f"type {self.type} is not registered")
        if not new and self._instance:
            return self._instance
        else:
            self._instance = _resource_device_mapping[self.type](self)
        return self._instance

    @staticmethod
    def from_dict(dict_obj):
        ret = Device()
        for key, value in dict_obj.items():
            if key == "ports":
                ports = dict()
                for port_name, port in value.items():
                    ports[port_name] = Port.from_dict(port, ret)
                setattr(ret, "ports", ports)
            else:
                setattr(ret, key, value)
        return ret


class Port(Resource):
    """
    代表所有端口类
    """

    def __init__(self, parent_device: Device = None, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)
        self.parent = parent_device
        self.remote_ports = list()
        self._instance = None

    def get_comm_instance(self, new=False):
        if self.type not in _resource_port_mapping:
            raise ResourceError(f"type {self.type} is not registered")
        if not new and self._instance:
            return self._instance
        else:
            self._instance = _resource_port_mapping[self.type](self)
        return self._instance

    def to_dict(self):
        ret = dict()
        for key, value in self.__dict__.items():
            if key in ["__instance", "logger"]:
                continue
            if key == "parent":
                ret[key] = value.name
            elif key == "remote_ports":
                ret[key] = list()
                for remote_port in value:
                    # 使用device的名称和port的名称来表示远端的端口
                    # 在反序列化的时候可以方便地找到相应的对象实例
                    ret[key].append(
                        {
                            "device": remote_port.parent.name,
                            "port": remote_port.name
                        }
                    )
            else:
                ret[key] = value
        return ret

    @staticmethod
    def from_dict(dict_obj, parent):
        ret = Port(parent)
        for key, value in dict_obj.items():
            if key == "remote_ports" or key == "parent":
                continue
            setattr(ret, key, value)
        return ret


class Software(Resource):
    """
    代表所有测试软件类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)


class Service(Resource):
    """
    代表所有测试服务类
    """

    def __init__(self, name: str = "", *args: tuple, **kwargs: dict):
        super().__init__(name=name, *args, **kwargs)
