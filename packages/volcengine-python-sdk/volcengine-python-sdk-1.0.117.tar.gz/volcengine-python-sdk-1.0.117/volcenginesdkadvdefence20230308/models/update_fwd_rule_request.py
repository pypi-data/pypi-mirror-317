# coding: utf-8

"""
    advdefence20230308

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class UpdateFwdRuleRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'fwd_port': 'int',
        'instance_ip': 'str',
        'proto': 'str',
        'src_ip_list': 'list[str]',
        'src_port': 'int',
        'time_out': 'int'
    }

    attribute_map = {
        'fwd_port': 'FwdPort',
        'instance_ip': 'InstanceIp',
        'proto': 'Proto',
        'src_ip_list': 'SrcIpList',
        'src_port': 'SrcPort',
        'time_out': 'TimeOut'
    }

    def __init__(self, fwd_port=None, instance_ip=None, proto=None, src_ip_list=None, src_port=None, time_out=None, _configuration=None):  # noqa: E501
        """UpdateFwdRuleRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._fwd_port = None
        self._instance_ip = None
        self._proto = None
        self._src_ip_list = None
        self._src_port = None
        self._time_out = None
        self.discriminator = None

        self.fwd_port = fwd_port
        self.instance_ip = instance_ip
        self.proto = proto
        if src_ip_list is not None:
            self.src_ip_list = src_ip_list
        self.src_port = src_port
        self.time_out = time_out

    @property
    def fwd_port(self):
        """Gets the fwd_port of this UpdateFwdRuleRequest.  # noqa: E501


        :return: The fwd_port of this UpdateFwdRuleRequest.  # noqa: E501
        :rtype: int
        """
        return self._fwd_port

    @fwd_port.setter
    def fwd_port(self, fwd_port):
        """Sets the fwd_port of this UpdateFwdRuleRequest.


        :param fwd_port: The fwd_port of this UpdateFwdRuleRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and fwd_port is None:
            raise ValueError("Invalid value for `fwd_port`, must not be `None`")  # noqa: E501

        self._fwd_port = fwd_port

    @property
    def instance_ip(self):
        """Gets the instance_ip of this UpdateFwdRuleRequest.  # noqa: E501


        :return: The instance_ip of this UpdateFwdRuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_ip

    @instance_ip.setter
    def instance_ip(self, instance_ip):
        """Sets the instance_ip of this UpdateFwdRuleRequest.


        :param instance_ip: The instance_ip of this UpdateFwdRuleRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and instance_ip is None:
            raise ValueError("Invalid value for `instance_ip`, must not be `None`")  # noqa: E501

        self._instance_ip = instance_ip

    @property
    def proto(self):
        """Gets the proto of this UpdateFwdRuleRequest.  # noqa: E501


        :return: The proto of this UpdateFwdRuleRequest.  # noqa: E501
        :rtype: str
        """
        return self._proto

    @proto.setter
    def proto(self, proto):
        """Sets the proto of this UpdateFwdRuleRequest.


        :param proto: The proto of this UpdateFwdRuleRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and proto is None:
            raise ValueError("Invalid value for `proto`, must not be `None`")  # noqa: E501

        self._proto = proto

    @property
    def src_ip_list(self):
        """Gets the src_ip_list of this UpdateFwdRuleRequest.  # noqa: E501


        :return: The src_ip_list of this UpdateFwdRuleRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._src_ip_list

    @src_ip_list.setter
    def src_ip_list(self, src_ip_list):
        """Sets the src_ip_list of this UpdateFwdRuleRequest.


        :param src_ip_list: The src_ip_list of this UpdateFwdRuleRequest.  # noqa: E501
        :type: list[str]
        """

        self._src_ip_list = src_ip_list

    @property
    def src_port(self):
        """Gets the src_port of this UpdateFwdRuleRequest.  # noqa: E501


        :return: The src_port of this UpdateFwdRuleRequest.  # noqa: E501
        :rtype: int
        """
        return self._src_port

    @src_port.setter
    def src_port(self, src_port):
        """Sets the src_port of this UpdateFwdRuleRequest.


        :param src_port: The src_port of this UpdateFwdRuleRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and src_port is None:
            raise ValueError("Invalid value for `src_port`, must not be `None`")  # noqa: E501

        self._src_port = src_port

    @property
    def time_out(self):
        """Gets the time_out of this UpdateFwdRuleRequest.  # noqa: E501


        :return: The time_out of this UpdateFwdRuleRequest.  # noqa: E501
        :rtype: int
        """
        return self._time_out

    @time_out.setter
    def time_out(self, time_out):
        """Sets the time_out of this UpdateFwdRuleRequest.


        :param time_out: The time_out of this UpdateFwdRuleRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and time_out is None:
            raise ValueError("Invalid value for `time_out`, must not be `None`")  # noqa: E501

        self._time_out = time_out

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(UpdateFwdRuleRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpdateFwdRuleRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateFwdRuleRequest):
            return True

        return self.to_dict() != other.to_dict()
