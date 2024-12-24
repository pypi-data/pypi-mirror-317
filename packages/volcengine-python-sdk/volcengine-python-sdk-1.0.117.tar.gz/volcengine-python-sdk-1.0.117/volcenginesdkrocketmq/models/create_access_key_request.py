# coding: utf-8

"""
    rocketmq

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class CreateAccessKeyRequest(object):
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
        'all_authority': 'str',
        'description': 'str',
        'instance_id': 'str'
    }

    attribute_map = {
        'all_authority': 'AllAuthority',
        'description': 'Description',
        'instance_id': 'InstanceId'
    }

    def __init__(self, all_authority=None, description=None, instance_id=None, _configuration=None):  # noqa: E501
        """CreateAccessKeyRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._all_authority = None
        self._description = None
        self._instance_id = None
        self.discriminator = None

        self.all_authority = all_authority
        if description is not None:
            self.description = description
        self.instance_id = instance_id

    @property
    def all_authority(self):
        """Gets the all_authority of this CreateAccessKeyRequest.  # noqa: E501


        :return: The all_authority of this CreateAccessKeyRequest.  # noqa: E501
        :rtype: str
        """
        return self._all_authority

    @all_authority.setter
    def all_authority(self, all_authority):
        """Sets the all_authority of this CreateAccessKeyRequest.


        :param all_authority: The all_authority of this CreateAccessKeyRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and all_authority is None:
            raise ValueError("Invalid value for `all_authority`, must not be `None`")  # noqa: E501

        self._all_authority = all_authority

    @property
    def description(self):
        """Gets the description of this CreateAccessKeyRequest.  # noqa: E501


        :return: The description of this CreateAccessKeyRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateAccessKeyRequest.


        :param description: The description of this CreateAccessKeyRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def instance_id(self):
        """Gets the instance_id of this CreateAccessKeyRequest.  # noqa: E501


        :return: The instance_id of this CreateAccessKeyRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this CreateAccessKeyRequest.


        :param instance_id: The instance_id of this CreateAccessKeyRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and instance_id is None:
            raise ValueError("Invalid value for `instance_id`, must not be `None`")  # noqa: E501

        self._instance_id = instance_id

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
        if issubclass(CreateAccessKeyRequest, dict):
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
        if not isinstance(other, CreateAccessKeyRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateAccessKeyRequest):
            return True

        return self.to_dict() != other.to_dict()
