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


class ModifyDBInstanceSubnetRequest(object):
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
        'client_token': 'str',
        'instance_id': 'str',
        'retention_days': 'int',
        'subnet_id': 'str',
        'vpc_id': 'str'
    }

    attribute_map = {
        'client_token': 'ClientToken',
        'instance_id': 'InstanceId',
        'retention_days': 'RetentionDays',
        'subnet_id': 'SubnetId',
        'vpc_id': 'VpcId'
    }

    def __init__(self, client_token=None, instance_id=None, retention_days=None, subnet_id=None, vpc_id=None, _configuration=None):  # noqa: E501
        """ModifyDBInstanceSubnetRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._client_token = None
        self._instance_id = None
        self._retention_days = None
        self._subnet_id = None
        self._vpc_id = None
        self.discriminator = None

        if client_token is not None:
            self.client_token = client_token
        self.instance_id = instance_id
        if retention_days is not None:
            self.retention_days = retention_days
        self.subnet_id = subnet_id
        self.vpc_id = vpc_id

    @property
    def client_token(self):
        """Gets the client_token of this ModifyDBInstanceSubnetRequest.  # noqa: E501


        :return: The client_token of this ModifyDBInstanceSubnetRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_token

    @client_token.setter
    def client_token(self, client_token):
        """Sets the client_token of this ModifyDBInstanceSubnetRequest.


        :param client_token: The client_token of this ModifyDBInstanceSubnetRequest.  # noqa: E501
        :type: str
        """

        self._client_token = client_token

    @property
    def instance_id(self):
        """Gets the instance_id of this ModifyDBInstanceSubnetRequest.  # noqa: E501


        :return: The instance_id of this ModifyDBInstanceSubnetRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ModifyDBInstanceSubnetRequest.


        :param instance_id: The instance_id of this ModifyDBInstanceSubnetRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and instance_id is None:
            raise ValueError("Invalid value for `instance_id`, must not be `None`")  # noqa: E501

        self._instance_id = instance_id

    @property
    def retention_days(self):
        """Gets the retention_days of this ModifyDBInstanceSubnetRequest.  # noqa: E501


        :return: The retention_days of this ModifyDBInstanceSubnetRequest.  # noqa: E501
        :rtype: int
        """
        return self._retention_days

    @retention_days.setter
    def retention_days(self, retention_days):
        """Sets the retention_days of this ModifyDBInstanceSubnetRequest.


        :param retention_days: The retention_days of this ModifyDBInstanceSubnetRequest.  # noqa: E501
        :type: int
        """

        self._retention_days = retention_days

    @property
    def subnet_id(self):
        """Gets the subnet_id of this ModifyDBInstanceSubnetRequest.  # noqa: E501


        :return: The subnet_id of this ModifyDBInstanceSubnetRequest.  # noqa: E501
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """Sets the subnet_id of this ModifyDBInstanceSubnetRequest.


        :param subnet_id: The subnet_id of this ModifyDBInstanceSubnetRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and subnet_id is None:
            raise ValueError("Invalid value for `subnet_id`, must not be `None`")  # noqa: E501

        self._subnet_id = subnet_id

    @property
    def vpc_id(self):
        """Gets the vpc_id of this ModifyDBInstanceSubnetRequest.  # noqa: E501


        :return: The vpc_id of this ModifyDBInstanceSubnetRequest.  # noqa: E501
        :rtype: str
        """
        return self._vpc_id

    @vpc_id.setter
    def vpc_id(self, vpc_id):
        """Sets the vpc_id of this ModifyDBInstanceSubnetRequest.


        :param vpc_id: The vpc_id of this ModifyDBInstanceSubnetRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and vpc_id is None:
            raise ValueError("Invalid value for `vpc_id`, must not be `None`")  # noqa: E501

        self._vpc_id = vpc_id

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
        if issubclass(ModifyDBInstanceSubnetRequest, dict):
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
        if not isinstance(other, ModifyDBInstanceSubnetRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModifyDBInstanceSubnetRequest):
            return True

        return self.to_dict() != other.to_dict()
