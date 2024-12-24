# coding: utf-8

"""
    privatelink

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class CreateVpcEndpointResponse(object):
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
        'endpoint_id': 'str',
        'pre_order_numbers': 'list[str]',
        'request_id': 'str'
    }

    attribute_map = {
        'endpoint_id': 'EndpointId',
        'pre_order_numbers': 'PreOrderNumbers',
        'request_id': 'RequestId'
    }

    def __init__(self, endpoint_id=None, pre_order_numbers=None, request_id=None, _configuration=None):  # noqa: E501
        """CreateVpcEndpointResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._endpoint_id = None
        self._pre_order_numbers = None
        self._request_id = None
        self.discriminator = None

        if endpoint_id is not None:
            self.endpoint_id = endpoint_id
        if pre_order_numbers is not None:
            self.pre_order_numbers = pre_order_numbers
        if request_id is not None:
            self.request_id = request_id

    @property
    def endpoint_id(self):
        """Gets the endpoint_id of this CreateVpcEndpointResponse.  # noqa: E501


        :return: The endpoint_id of this CreateVpcEndpointResponse.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_id

    @endpoint_id.setter
    def endpoint_id(self, endpoint_id):
        """Sets the endpoint_id of this CreateVpcEndpointResponse.


        :param endpoint_id: The endpoint_id of this CreateVpcEndpointResponse.  # noqa: E501
        :type: str
        """

        self._endpoint_id = endpoint_id

    @property
    def pre_order_numbers(self):
        """Gets the pre_order_numbers of this CreateVpcEndpointResponse.  # noqa: E501


        :return: The pre_order_numbers of this CreateVpcEndpointResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._pre_order_numbers

    @pre_order_numbers.setter
    def pre_order_numbers(self, pre_order_numbers):
        """Sets the pre_order_numbers of this CreateVpcEndpointResponse.


        :param pre_order_numbers: The pre_order_numbers of this CreateVpcEndpointResponse.  # noqa: E501
        :type: list[str]
        """

        self._pre_order_numbers = pre_order_numbers

    @property
    def request_id(self):
        """Gets the request_id of this CreateVpcEndpointResponse.  # noqa: E501


        :return: The request_id of this CreateVpcEndpointResponse.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this CreateVpcEndpointResponse.


        :param request_id: The request_id of this CreateVpcEndpointResponse.  # noqa: E501
        :type: str
        """

        self._request_id = request_id

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
        if issubclass(CreateVpcEndpointResponse, dict):
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
        if not isinstance(other, CreateVpcEndpointResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateVpcEndpointResponse):
            return True

        return self.to_dict() != other.to_dict()
