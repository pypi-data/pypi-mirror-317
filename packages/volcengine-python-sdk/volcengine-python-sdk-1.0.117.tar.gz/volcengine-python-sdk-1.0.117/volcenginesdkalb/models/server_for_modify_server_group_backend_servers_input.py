# coding: utf-8

"""
    alb

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ServerForModifyServerGroupBackendServersInput(object):
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
        'port': 'int',
        'server_id': 'str',
        'weight': 'int'
    }

    attribute_map = {
        'description': 'Description',
        'port': 'Port',
        'server_id': 'ServerId',
        'weight': 'Weight'
    }

    def __init__(self, description=None, port=None, server_id=None, weight=None, _configuration=None):  # noqa: E501
        """ServerForModifyServerGroupBackendServersInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._description = None
        self._port = None
        self._server_id = None
        self._weight = None
        self.discriminator = None

        if description is not None:
            self.description = description
        self.port = port
        self.server_id = server_id
        self.weight = weight

    @property
    def description(self):
        """Gets the description of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501


        :return: The description of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ServerForModifyServerGroupBackendServersInput.


        :param description: The description of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def port(self):
        """Gets the port of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501


        :return: The port of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this ServerForModifyServerGroupBackendServersInput.


        :param port: The port of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and port is None:
            raise ValueError("Invalid value for `port`, must not be `None`")  # noqa: E501

        self._port = port

    @property
    def server_id(self):
        """Gets the server_id of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501


        :return: The server_id of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501
        :rtype: str
        """
        return self._server_id

    @server_id.setter
    def server_id(self, server_id):
        """Sets the server_id of this ServerForModifyServerGroupBackendServersInput.


        :param server_id: The server_id of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and server_id is None:
            raise ValueError("Invalid value for `server_id`, must not be `None`")  # noqa: E501

        self._server_id = server_id

    @property
    def weight(self):
        """Gets the weight of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501


        :return: The weight of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501
        :rtype: int
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """Sets the weight of this ServerForModifyServerGroupBackendServersInput.


        :param weight: The weight of this ServerForModifyServerGroupBackendServersInput.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and weight is None:
            raise ValueError("Invalid value for `weight`, must not be `None`")  # noqa: E501

        self._weight = weight

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
        if issubclass(ServerForModifyServerGroupBackendServersInput, dict):
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
        if not isinstance(other, ServerForModifyServerGroupBackendServersInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ServerForModifyServerGroupBackendServersInput):
            return True

        return self.to_dict() != other.to_dict()
