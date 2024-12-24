# coding: utf-8

"""
    vpc

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class CreateVpcResponse(object):
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
        'request_id': 'str',
        'route_table_id': 'str',
        'vpc_id': 'str'
    }

    attribute_map = {
        'request_id': 'RequestId',
        'route_table_id': 'RouteTableId',
        'vpc_id': 'VpcId'
    }

    def __init__(self, request_id=None, route_table_id=None, vpc_id=None, _configuration=None):  # noqa: E501
        """CreateVpcResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._request_id = None
        self._route_table_id = None
        self._vpc_id = None
        self.discriminator = None

        if request_id is not None:
            self.request_id = request_id
        if route_table_id is not None:
            self.route_table_id = route_table_id
        if vpc_id is not None:
            self.vpc_id = vpc_id

    @property
    def request_id(self):
        """Gets the request_id of this CreateVpcResponse.  # noqa: E501


        :return: The request_id of this CreateVpcResponse.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this CreateVpcResponse.


        :param request_id: The request_id of this CreateVpcResponse.  # noqa: E501
        :type: str
        """

        self._request_id = request_id

    @property
    def route_table_id(self):
        """Gets the route_table_id of this CreateVpcResponse.  # noqa: E501


        :return: The route_table_id of this CreateVpcResponse.  # noqa: E501
        :rtype: str
        """
        return self._route_table_id

    @route_table_id.setter
    def route_table_id(self, route_table_id):
        """Sets the route_table_id of this CreateVpcResponse.


        :param route_table_id: The route_table_id of this CreateVpcResponse.  # noqa: E501
        :type: str
        """

        self._route_table_id = route_table_id

    @property
    def vpc_id(self):
        """Gets the vpc_id of this CreateVpcResponse.  # noqa: E501


        :return: The vpc_id of this CreateVpcResponse.  # noqa: E501
        :rtype: str
        """
        return self._vpc_id

    @vpc_id.setter
    def vpc_id(self, vpc_id):
        """Sets the vpc_id of this CreateVpcResponse.


        :param vpc_id: The vpc_id of this CreateVpcResponse.  # noqa: E501
        :type: str
        """

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
        if issubclass(CreateVpcResponse, dict):
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
        if not isinstance(other, CreateVpcResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateVpcResponse):
            return True

        return self.to_dict() != other.to_dict()
