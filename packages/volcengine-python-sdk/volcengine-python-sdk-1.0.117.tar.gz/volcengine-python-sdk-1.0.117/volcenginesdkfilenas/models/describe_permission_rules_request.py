# coding: utf-8

"""
    filenas

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribePermissionRulesRequest(object):
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
        'file_system_type': 'str',
        'permission_group_id': 'str'
    }

    attribute_map = {
        'file_system_type': 'FileSystemType',
        'permission_group_id': 'PermissionGroupId'
    }

    def __init__(self, file_system_type=None, permission_group_id=None, _configuration=None):  # noqa: E501
        """DescribePermissionRulesRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._file_system_type = None
        self._permission_group_id = None
        self.discriminator = None

        if file_system_type is not None:
            self.file_system_type = file_system_type
        self.permission_group_id = permission_group_id

    @property
    def file_system_type(self):
        """Gets the file_system_type of this DescribePermissionRulesRequest.  # noqa: E501


        :return: The file_system_type of this DescribePermissionRulesRequest.  # noqa: E501
        :rtype: str
        """
        return self._file_system_type

    @file_system_type.setter
    def file_system_type(self, file_system_type):
        """Sets the file_system_type of this DescribePermissionRulesRequest.


        :param file_system_type: The file_system_type of this DescribePermissionRulesRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["Extreme", "Capacity", "Cache"]  # noqa: E501
        if (self._configuration.client_side_validation and
                file_system_type not in allowed_values):
            raise ValueError(
                "Invalid value for `file_system_type` ({0}), must be one of {1}"  # noqa: E501
                .format(file_system_type, allowed_values)
            )

        self._file_system_type = file_system_type

    @property
    def permission_group_id(self):
        """Gets the permission_group_id of this DescribePermissionRulesRequest.  # noqa: E501


        :return: The permission_group_id of this DescribePermissionRulesRequest.  # noqa: E501
        :rtype: str
        """
        return self._permission_group_id

    @permission_group_id.setter
    def permission_group_id(self, permission_group_id):
        """Sets the permission_group_id of this DescribePermissionRulesRequest.


        :param permission_group_id: The permission_group_id of this DescribePermissionRulesRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and permission_group_id is None:
            raise ValueError("Invalid value for `permission_group_id`, must not be `None`")  # noqa: E501

        self._permission_group_id = permission_group_id

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
        if issubclass(DescribePermissionRulesRequest, dict):
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
        if not isinstance(other, DescribePermissionRulesRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribePermissionRulesRequest):
            return True

        return self.to_dict() != other.to_dict()
