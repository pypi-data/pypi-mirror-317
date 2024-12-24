# coding: utf-8

"""
    ecs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class EipAddressForRunInstancesInput(object):
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
        'bandwidth_mbps': 'int',
        'bandwidth_package_id': 'str',
        'charge_type': 'str',
        'isp': 'str',
        'release_with_instance': 'bool',
        'security_protection_instance_id': 'int',
        'security_protection_types': 'list[str]'
    }

    attribute_map = {
        'bandwidth_mbps': 'BandwidthMbps',
        'bandwidth_package_id': 'BandwidthPackageId',
        'charge_type': 'ChargeType',
        'isp': 'ISP',
        'release_with_instance': 'ReleaseWithInstance',
        'security_protection_instance_id': 'SecurityProtectionInstanceId',
        'security_protection_types': 'SecurityProtectionTypes'
    }

    def __init__(self, bandwidth_mbps=None, bandwidth_package_id=None, charge_type=None, isp=None, release_with_instance=None, security_protection_instance_id=None, security_protection_types=None, _configuration=None):  # noqa: E501
        """EipAddressForRunInstancesInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._bandwidth_mbps = None
        self._bandwidth_package_id = None
        self._charge_type = None
        self._isp = None
        self._release_with_instance = None
        self._security_protection_instance_id = None
        self._security_protection_types = None
        self.discriminator = None

        if bandwidth_mbps is not None:
            self.bandwidth_mbps = bandwidth_mbps
        if bandwidth_package_id is not None:
            self.bandwidth_package_id = bandwidth_package_id
        if charge_type is not None:
            self.charge_type = charge_type
        if isp is not None:
            self.isp = isp
        if release_with_instance is not None:
            self.release_with_instance = release_with_instance
        if security_protection_instance_id is not None:
            self.security_protection_instance_id = security_protection_instance_id
        if security_protection_types is not None:
            self.security_protection_types = security_protection_types

    @property
    def bandwidth_mbps(self):
        """Gets the bandwidth_mbps of this EipAddressForRunInstancesInput.  # noqa: E501


        :return: The bandwidth_mbps of this EipAddressForRunInstancesInput.  # noqa: E501
        :rtype: int
        """
        return self._bandwidth_mbps

    @bandwidth_mbps.setter
    def bandwidth_mbps(self, bandwidth_mbps):
        """Sets the bandwidth_mbps of this EipAddressForRunInstancesInput.


        :param bandwidth_mbps: The bandwidth_mbps of this EipAddressForRunInstancesInput.  # noqa: E501
        :type: int
        """

        self._bandwidth_mbps = bandwidth_mbps

    @property
    def bandwidth_package_id(self):
        """Gets the bandwidth_package_id of this EipAddressForRunInstancesInput.  # noqa: E501


        :return: The bandwidth_package_id of this EipAddressForRunInstancesInput.  # noqa: E501
        :rtype: str
        """
        return self._bandwidth_package_id

    @bandwidth_package_id.setter
    def bandwidth_package_id(self, bandwidth_package_id):
        """Sets the bandwidth_package_id of this EipAddressForRunInstancesInput.


        :param bandwidth_package_id: The bandwidth_package_id of this EipAddressForRunInstancesInput.  # noqa: E501
        :type: str
        """

        self._bandwidth_package_id = bandwidth_package_id

    @property
    def charge_type(self):
        """Gets the charge_type of this EipAddressForRunInstancesInput.  # noqa: E501


        :return: The charge_type of this EipAddressForRunInstancesInput.  # noqa: E501
        :rtype: str
        """
        return self._charge_type

    @charge_type.setter
    def charge_type(self, charge_type):
        """Sets the charge_type of this EipAddressForRunInstancesInput.


        :param charge_type: The charge_type of this EipAddressForRunInstancesInput.  # noqa: E501
        :type: str
        """

        self._charge_type = charge_type

    @property
    def isp(self):
        """Gets the isp of this EipAddressForRunInstancesInput.  # noqa: E501


        :return: The isp of this EipAddressForRunInstancesInput.  # noqa: E501
        :rtype: str
        """
        return self._isp

    @isp.setter
    def isp(self, isp):
        """Sets the isp of this EipAddressForRunInstancesInput.


        :param isp: The isp of this EipAddressForRunInstancesInput.  # noqa: E501
        :type: str
        """

        self._isp = isp

    @property
    def release_with_instance(self):
        """Gets the release_with_instance of this EipAddressForRunInstancesInput.  # noqa: E501


        :return: The release_with_instance of this EipAddressForRunInstancesInput.  # noqa: E501
        :rtype: bool
        """
        return self._release_with_instance

    @release_with_instance.setter
    def release_with_instance(self, release_with_instance):
        """Sets the release_with_instance of this EipAddressForRunInstancesInput.


        :param release_with_instance: The release_with_instance of this EipAddressForRunInstancesInput.  # noqa: E501
        :type: bool
        """

        self._release_with_instance = release_with_instance

    @property
    def security_protection_instance_id(self):
        """Gets the security_protection_instance_id of this EipAddressForRunInstancesInput.  # noqa: E501


        :return: The security_protection_instance_id of this EipAddressForRunInstancesInput.  # noqa: E501
        :rtype: int
        """
        return self._security_protection_instance_id

    @security_protection_instance_id.setter
    def security_protection_instance_id(self, security_protection_instance_id):
        """Sets the security_protection_instance_id of this EipAddressForRunInstancesInput.


        :param security_protection_instance_id: The security_protection_instance_id of this EipAddressForRunInstancesInput.  # noqa: E501
        :type: int
        """

        self._security_protection_instance_id = security_protection_instance_id

    @property
    def security_protection_types(self):
        """Gets the security_protection_types of this EipAddressForRunInstancesInput.  # noqa: E501


        :return: The security_protection_types of this EipAddressForRunInstancesInput.  # noqa: E501
        :rtype: list[str]
        """
        return self._security_protection_types

    @security_protection_types.setter
    def security_protection_types(self, security_protection_types):
        """Sets the security_protection_types of this EipAddressForRunInstancesInput.


        :param security_protection_types: The security_protection_types of this EipAddressForRunInstancesInput.  # noqa: E501
        :type: list[str]
        """

        self._security_protection_types = security_protection_types

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
        if issubclass(EipAddressForRunInstancesInput, dict):
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
        if not isinstance(other, EipAddressForRunInstancesInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EipAddressForRunInstancesInput):
            return True

        return self.to_dict() != other.to_dict()
