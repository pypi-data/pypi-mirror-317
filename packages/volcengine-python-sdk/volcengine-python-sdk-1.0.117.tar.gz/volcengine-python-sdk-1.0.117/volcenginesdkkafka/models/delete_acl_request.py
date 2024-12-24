# coding: utf-8

"""
    kafka

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DeleteAclRequest(object):
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
        'access_policy': 'str',
        'instance_id': 'str',
        'ip': 'str',
        'pattern_type': 'str',
        'resource': 'str',
        'resource_type': 'str',
        'user_name': 'str'
    }

    attribute_map = {
        'access_policy': 'AccessPolicy',
        'instance_id': 'InstanceId',
        'ip': 'Ip',
        'pattern_type': 'PatternType',
        'resource': 'Resource',
        'resource_type': 'ResourceType',
        'user_name': 'UserName'
    }

    def __init__(self, access_policy=None, instance_id=None, ip=None, pattern_type=None, resource=None, resource_type=None, user_name=None, _configuration=None):  # noqa: E501
        """DeleteAclRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._access_policy = None
        self._instance_id = None
        self._ip = None
        self._pattern_type = None
        self._resource = None
        self._resource_type = None
        self._user_name = None
        self.discriminator = None

        self.access_policy = access_policy
        self.instance_id = instance_id
        self.ip = ip
        self.pattern_type = pattern_type
        self.resource = resource
        self.resource_type = resource_type
        self.user_name = user_name

    @property
    def access_policy(self):
        """Gets the access_policy of this DeleteAclRequest.  # noqa: E501


        :return: The access_policy of this DeleteAclRequest.  # noqa: E501
        :rtype: str
        """
        return self._access_policy

    @access_policy.setter
    def access_policy(self, access_policy):
        """Sets the access_policy of this DeleteAclRequest.


        :param access_policy: The access_policy of this DeleteAclRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and access_policy is None:
            raise ValueError("Invalid value for `access_policy`, must not be `None`")  # noqa: E501

        self._access_policy = access_policy

    @property
    def instance_id(self):
        """Gets the instance_id of this DeleteAclRequest.  # noqa: E501


        :return: The instance_id of this DeleteAclRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this DeleteAclRequest.


        :param instance_id: The instance_id of this DeleteAclRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and instance_id is None:
            raise ValueError("Invalid value for `instance_id`, must not be `None`")  # noqa: E501

        self._instance_id = instance_id

    @property
    def ip(self):
        """Gets the ip of this DeleteAclRequest.  # noqa: E501


        :return: The ip of this DeleteAclRequest.  # noqa: E501
        :rtype: str
        """
        return self._ip

    @ip.setter
    def ip(self, ip):
        """Sets the ip of this DeleteAclRequest.


        :param ip: The ip of this DeleteAclRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and ip is None:
            raise ValueError("Invalid value for `ip`, must not be `None`")  # noqa: E501

        self._ip = ip

    @property
    def pattern_type(self):
        """Gets the pattern_type of this DeleteAclRequest.  # noqa: E501


        :return: The pattern_type of this DeleteAclRequest.  # noqa: E501
        :rtype: str
        """
        return self._pattern_type

    @pattern_type.setter
    def pattern_type(self, pattern_type):
        """Sets the pattern_type of this DeleteAclRequest.


        :param pattern_type: The pattern_type of this DeleteAclRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and pattern_type is None:
            raise ValueError("Invalid value for `pattern_type`, must not be `None`")  # noqa: E501

        self._pattern_type = pattern_type

    @property
    def resource(self):
        """Gets the resource of this DeleteAclRequest.  # noqa: E501


        :return: The resource of this DeleteAclRequest.  # noqa: E501
        :rtype: str
        """
        return self._resource

    @resource.setter
    def resource(self, resource):
        """Sets the resource of this DeleteAclRequest.


        :param resource: The resource of this DeleteAclRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and resource is None:
            raise ValueError("Invalid value for `resource`, must not be `None`")  # noqa: E501

        self._resource = resource

    @property
    def resource_type(self):
        """Gets the resource_type of this DeleteAclRequest.  # noqa: E501


        :return: The resource_type of this DeleteAclRequest.  # noqa: E501
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this DeleteAclRequest.


        :param resource_type: The resource_type of this DeleteAclRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and resource_type is None:
            raise ValueError("Invalid value for `resource_type`, must not be `None`")  # noqa: E501

        self._resource_type = resource_type

    @property
    def user_name(self):
        """Gets the user_name of this DeleteAclRequest.  # noqa: E501


        :return: The user_name of this DeleteAclRequest.  # noqa: E501
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """Sets the user_name of this DeleteAclRequest.


        :param user_name: The user_name of this DeleteAclRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and user_name is None:
            raise ValueError("Invalid value for `user_name`, must not be `None`")  # noqa: E501

        self._user_name = user_name

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
        if issubclass(DeleteAclRequest, dict):
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
        if not isinstance(other, DeleteAclRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeleteAclRequest):
            return True

        return self.to_dict() != other.to_dict()
