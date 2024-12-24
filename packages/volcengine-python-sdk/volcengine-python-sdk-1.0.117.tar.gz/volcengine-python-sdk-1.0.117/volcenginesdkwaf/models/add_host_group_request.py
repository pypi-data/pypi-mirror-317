# coding: utf-8

"""
    waf

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class AddHostGroupRequest(object):
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
        'description': 'str',
        'host_list': 'list[str]',
        'name': 'str'
    }

    attribute_map = {
        'description': 'Description',
        'host_list': 'HostList',
        'name': 'Name'
    }

    def __init__(self, description=None, host_list=None, name=None, _configuration=None):  # noqa: E501
        """AddHostGroupRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._description = None
        self._host_list = None
        self._name = None
        self.discriminator = None

        if description is not None:
            self.description = description
        if host_list is not None:
            self.host_list = host_list
        self.name = name

    @property
    def description(self):
        """Gets the description of this AddHostGroupRequest.  # noqa: E501


        :return: The description of this AddHostGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AddHostGroupRequest.


        :param description: The description of this AddHostGroupRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def host_list(self):
        """Gets the host_list of this AddHostGroupRequest.  # noqa: E501


        :return: The host_list of this AddHostGroupRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._host_list

    @host_list.setter
    def host_list(self, host_list):
        """Sets the host_list of this AddHostGroupRequest.


        :param host_list: The host_list of this AddHostGroupRequest.  # noqa: E501
        :type: list[str]
        """

        self._host_list = host_list

    @property
    def name(self):
        """Gets the name of this AddHostGroupRequest.  # noqa: E501


        :return: The name of this AddHostGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AddHostGroupRequest.


        :param name: The name of this AddHostGroupRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

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
        if issubclass(AddHostGroupRequest, dict):
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
        if not isinstance(other, AddHostGroupRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AddHostGroupRequest):
            return True

        return self.to_dict() != other.to_dict()
