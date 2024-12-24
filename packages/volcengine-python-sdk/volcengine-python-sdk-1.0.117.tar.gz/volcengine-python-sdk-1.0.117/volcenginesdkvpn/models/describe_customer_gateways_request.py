# coding: utf-8

"""
    vpn

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeCustomerGatewaysRequest(object):
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
        'customer_gateway_ids': 'list[str]',
        'customer_gateway_name': 'str',
        'ip_address': 'str',
        'page_number': 'int',
        'page_size': 'int',
        'project_name': 'str',
        'status': 'str'
    }

    attribute_map = {
        'customer_gateway_ids': 'CustomerGatewayIds',
        'customer_gateway_name': 'CustomerGatewayName',
        'ip_address': 'IpAddress',
        'page_number': 'PageNumber',
        'page_size': 'PageSize',
        'project_name': 'ProjectName',
        'status': 'Status'
    }

    def __init__(self, customer_gateway_ids=None, customer_gateway_name=None, ip_address=None, page_number=None, page_size=None, project_name=None, status=None, _configuration=None):  # noqa: E501
        """DescribeCustomerGatewaysRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._customer_gateway_ids = None
        self._customer_gateway_name = None
        self._ip_address = None
        self._page_number = None
        self._page_size = None
        self._project_name = None
        self._status = None
        self.discriminator = None

        if customer_gateway_ids is not None:
            self.customer_gateway_ids = customer_gateway_ids
        if customer_gateway_name is not None:
            self.customer_gateway_name = customer_gateway_name
        if ip_address is not None:
            self.ip_address = ip_address
        if page_number is not None:
            self.page_number = page_number
        if page_size is not None:
            self.page_size = page_size
        if project_name is not None:
            self.project_name = project_name
        if status is not None:
            self.status = status

    @property
    def customer_gateway_ids(self):
        """Gets the customer_gateway_ids of this DescribeCustomerGatewaysRequest.  # noqa: E501


        :return: The customer_gateway_ids of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._customer_gateway_ids

    @customer_gateway_ids.setter
    def customer_gateway_ids(self, customer_gateway_ids):
        """Sets the customer_gateway_ids of this DescribeCustomerGatewaysRequest.


        :param customer_gateway_ids: The customer_gateway_ids of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :type: list[str]
        """

        self._customer_gateway_ids = customer_gateway_ids

    @property
    def customer_gateway_name(self):
        """Gets the customer_gateway_name of this DescribeCustomerGatewaysRequest.  # noqa: E501


        :return: The customer_gateway_name of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :rtype: str
        """
        return self._customer_gateway_name

    @customer_gateway_name.setter
    def customer_gateway_name(self, customer_gateway_name):
        """Sets the customer_gateway_name of this DescribeCustomerGatewaysRequest.


        :param customer_gateway_name: The customer_gateway_name of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :type: str
        """

        self._customer_gateway_name = customer_gateway_name

    @property
    def ip_address(self):
        """Gets the ip_address of this DescribeCustomerGatewaysRequest.  # noqa: E501


        :return: The ip_address of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :rtype: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        """Sets the ip_address of this DescribeCustomerGatewaysRequest.


        :param ip_address: The ip_address of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :type: str
        """

        self._ip_address = ip_address

    @property
    def page_number(self):
        """Gets the page_number of this DescribeCustomerGatewaysRequest.  # noqa: E501


        :return: The page_number of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this DescribeCustomerGatewaysRequest.


        :param page_number: The page_number of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :type: int
        """

        self._page_number = page_number

    @property
    def page_size(self):
        """Gets the page_size of this DescribeCustomerGatewaysRequest.  # noqa: E501


        :return: The page_size of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this DescribeCustomerGatewaysRequest.


        :param page_size: The page_size of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

    @property
    def project_name(self):
        """Gets the project_name of this DescribeCustomerGatewaysRequest.  # noqa: E501


        :return: The project_name of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this DescribeCustomerGatewaysRequest.


        :param project_name: The project_name of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def status(self):
        """Gets the status of this DescribeCustomerGatewaysRequest.  # noqa: E501


        :return: The status of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DescribeCustomerGatewaysRequest.


        :param status: The status of this DescribeCustomerGatewaysRequest.  # noqa: E501
        :type: str
        """

        self._status = status

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
        if issubclass(DescribeCustomerGatewaysRequest, dict):
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
        if not isinstance(other, DescribeCustomerGatewaysRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeCustomerGatewaysRequest):
            return True

        return self.to_dict() != other.to_dict()
