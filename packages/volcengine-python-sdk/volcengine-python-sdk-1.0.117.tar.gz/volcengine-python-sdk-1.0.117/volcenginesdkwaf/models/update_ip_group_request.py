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


class UpdateIpGroupRequest(object):
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
        'add_type': 'str',
        'ip_group_id': 'int',
        'ip_list': 'list[str]',
        'name': 'str',
        'project_name': 'str'
    }

    attribute_map = {
        'add_type': 'AddType',
        'ip_group_id': 'IpGroupId',
        'ip_list': 'IpList',
        'name': 'Name',
        'project_name': 'ProjectName'
    }

    def __init__(self, add_type=None, ip_group_id=None, ip_list=None, name=None, project_name=None, _configuration=None):  # noqa: E501
        """UpdateIpGroupRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._add_type = None
        self._ip_group_id = None
        self._ip_list = None
        self._name = None
        self._project_name = None
        self.discriminator = None

        self.add_type = add_type
        self.ip_group_id = ip_group_id
        if ip_list is not None:
            self.ip_list = ip_list
        self.name = name
        if project_name is not None:
            self.project_name = project_name

    @property
    def add_type(self):
        """Gets the add_type of this UpdateIpGroupRequest.  # noqa: E501


        :return: The add_type of this UpdateIpGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._add_type

    @add_type.setter
    def add_type(self, add_type):
        """Sets the add_type of this UpdateIpGroupRequest.


        :param add_type: The add_type of this UpdateIpGroupRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and add_type is None:
            raise ValueError("Invalid value for `add_type`, must not be `None`")  # noqa: E501

        self._add_type = add_type

    @property
    def ip_group_id(self):
        """Gets the ip_group_id of this UpdateIpGroupRequest.  # noqa: E501


        :return: The ip_group_id of this UpdateIpGroupRequest.  # noqa: E501
        :rtype: int
        """
        return self._ip_group_id

    @ip_group_id.setter
    def ip_group_id(self, ip_group_id):
        """Sets the ip_group_id of this UpdateIpGroupRequest.


        :param ip_group_id: The ip_group_id of this UpdateIpGroupRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and ip_group_id is None:
            raise ValueError("Invalid value for `ip_group_id`, must not be `None`")  # noqa: E501

        self._ip_group_id = ip_group_id

    @property
    def ip_list(self):
        """Gets the ip_list of this UpdateIpGroupRequest.  # noqa: E501


        :return: The ip_list of this UpdateIpGroupRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._ip_list

    @ip_list.setter
    def ip_list(self, ip_list):
        """Sets the ip_list of this UpdateIpGroupRequest.


        :param ip_list: The ip_list of this UpdateIpGroupRequest.  # noqa: E501
        :type: list[str]
        """

        self._ip_list = ip_list

    @property
    def name(self):
        """Gets the name of this UpdateIpGroupRequest.  # noqa: E501


        :return: The name of this UpdateIpGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateIpGroupRequest.


        :param name: The name of this UpdateIpGroupRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def project_name(self):
        """Gets the project_name of this UpdateIpGroupRequest.  # noqa: E501


        :return: The project_name of this UpdateIpGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this UpdateIpGroupRequest.


        :param project_name: The project_name of this UpdateIpGroupRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

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
        if issubclass(UpdateIpGroupRequest, dict):
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
        if not isinstance(other, UpdateIpGroupRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateIpGroupRequest):
            return True

        return self.to_dict() != other.to_dict()
