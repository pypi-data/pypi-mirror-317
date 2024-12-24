# coding: utf-8

"""
    rds_mysql_v2

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class GrantDBAccountPrivilegeRequest(object):
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
        'account_name': 'str',
        'account_privileges': 'list[AccountPrivilegeForGrantDBAccountPrivilegeInput]',
        'host': 'str',
        'instance_id': 'str'
    }

    attribute_map = {
        'account_name': 'AccountName',
        'account_privileges': 'AccountPrivileges',
        'host': 'Host',
        'instance_id': 'InstanceId'
    }

    def __init__(self, account_name=None, account_privileges=None, host=None, instance_id=None, _configuration=None):  # noqa: E501
        """GrantDBAccountPrivilegeRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._account_name = None
        self._account_privileges = None
        self._host = None
        self._instance_id = None
        self.discriminator = None

        self.account_name = account_name
        if account_privileges is not None:
            self.account_privileges = account_privileges
        if host is not None:
            self.host = host
        self.instance_id = instance_id

    @property
    def account_name(self):
        """Gets the account_name of this GrantDBAccountPrivilegeRequest.  # noqa: E501


        :return: The account_name of this GrantDBAccountPrivilegeRequest.  # noqa: E501
        :rtype: str
        """
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        """Sets the account_name of this GrantDBAccountPrivilegeRequest.


        :param account_name: The account_name of this GrantDBAccountPrivilegeRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and account_name is None:
            raise ValueError("Invalid value for `account_name`, must not be `None`")  # noqa: E501

        self._account_name = account_name

    @property
    def account_privileges(self):
        """Gets the account_privileges of this GrantDBAccountPrivilegeRequest.  # noqa: E501


        :return: The account_privileges of this GrantDBAccountPrivilegeRequest.  # noqa: E501
        :rtype: list[AccountPrivilegeForGrantDBAccountPrivilegeInput]
        """
        return self._account_privileges

    @account_privileges.setter
    def account_privileges(self, account_privileges):
        """Sets the account_privileges of this GrantDBAccountPrivilegeRequest.


        :param account_privileges: The account_privileges of this GrantDBAccountPrivilegeRequest.  # noqa: E501
        :type: list[AccountPrivilegeForGrantDBAccountPrivilegeInput]
        """

        self._account_privileges = account_privileges

    @property
    def host(self):
        """Gets the host of this GrantDBAccountPrivilegeRequest.  # noqa: E501


        :return: The host of this GrantDBAccountPrivilegeRequest.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this GrantDBAccountPrivilegeRequest.


        :param host: The host of this GrantDBAccountPrivilegeRequest.  # noqa: E501
        :type: str
        """

        self._host = host

    @property
    def instance_id(self):
        """Gets the instance_id of this GrantDBAccountPrivilegeRequest.  # noqa: E501


        :return: The instance_id of this GrantDBAccountPrivilegeRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this GrantDBAccountPrivilegeRequest.


        :param instance_id: The instance_id of this GrantDBAccountPrivilegeRequest.  # noqa: E501
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
        if issubclass(GrantDBAccountPrivilegeRequest, dict):
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
        if not isinstance(other, GrantDBAccountPrivilegeRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GrantDBAccountPrivilegeRequest):
            return True

        return self.to_dict() != other.to_dict()
