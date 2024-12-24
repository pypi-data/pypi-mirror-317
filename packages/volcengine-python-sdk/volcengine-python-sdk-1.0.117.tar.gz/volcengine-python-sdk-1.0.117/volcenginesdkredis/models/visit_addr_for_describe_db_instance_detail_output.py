# coding: utf-8

"""
    redis

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class VisitAddrForDescribeDBInstanceDetailOutput(object):
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
        'addr_type': 'str',
        'address': 'str',
        'eip_id': 'str',
        'port': 'str',
        'vip': 'str',
        'vipv6': 'str'
    }

    attribute_map = {
        'addr_type': 'AddrType',
        'address': 'Address',
        'eip_id': 'EipId',
        'port': 'Port',
        'vip': 'VIP',
        'vipv6': 'VIPv6'
    }

    def __init__(self, addr_type=None, address=None, eip_id=None, port=None, vip=None, vipv6=None, _configuration=None):  # noqa: E501
        """VisitAddrForDescribeDBInstanceDetailOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._addr_type = None
        self._address = None
        self._eip_id = None
        self._port = None
        self._vip = None
        self._vipv6 = None
        self.discriminator = None

        if addr_type is not None:
            self.addr_type = addr_type
        if address is not None:
            self.address = address
        if eip_id is not None:
            self.eip_id = eip_id
        if port is not None:
            self.port = port
        if vip is not None:
            self.vip = vip
        if vipv6 is not None:
            self.vipv6 = vipv6

    @property
    def addr_type(self):
        """Gets the addr_type of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501


        :return: The addr_type of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :rtype: str
        """
        return self._addr_type

    @addr_type.setter
    def addr_type(self, addr_type):
        """Sets the addr_type of this VisitAddrForDescribeDBInstanceDetailOutput.


        :param addr_type: The addr_type of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :type: str
        """

        self._addr_type = addr_type

    @property
    def address(self):
        """Gets the address of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501


        :return: The address of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this VisitAddrForDescribeDBInstanceDetailOutput.


        :param address: The address of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def eip_id(self):
        """Gets the eip_id of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501


        :return: The eip_id of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :rtype: str
        """
        return self._eip_id

    @eip_id.setter
    def eip_id(self, eip_id):
        """Sets the eip_id of this VisitAddrForDescribeDBInstanceDetailOutput.


        :param eip_id: The eip_id of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :type: str
        """

        self._eip_id = eip_id

    @property
    def port(self):
        """Gets the port of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501


        :return: The port of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :rtype: str
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this VisitAddrForDescribeDBInstanceDetailOutput.


        :param port: The port of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :type: str
        """

        self._port = port

    @property
    def vip(self):
        """Gets the vip of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501


        :return: The vip of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :rtype: str
        """
        return self._vip

    @vip.setter
    def vip(self, vip):
        """Sets the vip of this VisitAddrForDescribeDBInstanceDetailOutput.


        :param vip: The vip of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :type: str
        """

        self._vip = vip

    @property
    def vipv6(self):
        """Gets the vipv6 of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501


        :return: The vipv6 of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :rtype: str
        """
        return self._vipv6

    @vipv6.setter
    def vipv6(self, vipv6):
        """Sets the vipv6 of this VisitAddrForDescribeDBInstanceDetailOutput.


        :param vipv6: The vipv6 of this VisitAddrForDescribeDBInstanceDetailOutput.  # noqa: E501
        :type: str
        """

        self._vipv6 = vipv6

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
        if issubclass(VisitAddrForDescribeDBInstanceDetailOutput, dict):
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
        if not isinstance(other, VisitAddrForDescribeDBInstanceDetailOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, VisitAddrForDescribeDBInstanceDetailOutput):
            return True

        return self.to_dict() != other.to_dict()
