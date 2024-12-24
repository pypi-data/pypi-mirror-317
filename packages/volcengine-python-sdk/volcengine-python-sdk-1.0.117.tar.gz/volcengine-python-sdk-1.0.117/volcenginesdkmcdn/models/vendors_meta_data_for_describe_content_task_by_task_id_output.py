# coding: utf-8

"""
    mcdn

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class VendorsMetaDataForDescribeContentTaskByTaskIdOutput(object):
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
        'cloud_account_id': 'str',
        'cost': 'float',
        'error': 'ErrorForDescribeContentTaskByTaskIdOutput',
        'product_type': 'str',
        'request_id': 'str',
        'vendor': 'str'
    }

    attribute_map = {
        'cloud_account_id': 'CloudAccountId',
        'cost': 'Cost',
        'error': 'Error',
        'product_type': 'ProductType',
        'request_id': 'RequestId',
        'vendor': 'Vendor'
    }

    def __init__(self, cloud_account_id=None, cost=None, error=None, product_type=None, request_id=None, vendor=None, _configuration=None):  # noqa: E501
        """VendorsMetaDataForDescribeContentTaskByTaskIdOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cloud_account_id = None
        self._cost = None
        self._error = None
        self._product_type = None
        self._request_id = None
        self._vendor = None
        self.discriminator = None

        if cloud_account_id is not None:
            self.cloud_account_id = cloud_account_id
        if cost is not None:
            self.cost = cost
        if error is not None:
            self.error = error
        if product_type is not None:
            self.product_type = product_type
        if request_id is not None:
            self.request_id = request_id
        if vendor is not None:
            self.vendor = vendor

    @property
    def cloud_account_id(self):
        """Gets the cloud_account_id of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501


        :return: The cloud_account_id of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :rtype: str
        """
        return self._cloud_account_id

    @cloud_account_id.setter
    def cloud_account_id(self, cloud_account_id):
        """Sets the cloud_account_id of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.


        :param cloud_account_id: The cloud_account_id of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :type: str
        """

        self._cloud_account_id = cloud_account_id

    @property
    def cost(self):
        """Gets the cost of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501


        :return: The cost of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :rtype: float
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """Sets the cost of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.


        :param cost: The cost of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :type: float
        """

        self._cost = cost

    @property
    def error(self):
        """Gets the error of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501


        :return: The error of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :rtype: ErrorForDescribeContentTaskByTaskIdOutput
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.


        :param error: The error of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :type: ErrorForDescribeContentTaskByTaskIdOutput
        """

        self._error = error

    @property
    def product_type(self):
        """Gets the product_type of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501


        :return: The product_type of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :rtype: str
        """
        return self._product_type

    @product_type.setter
    def product_type(self, product_type):
        """Sets the product_type of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.


        :param product_type: The product_type of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :type: str
        """

        self._product_type = product_type

    @property
    def request_id(self):
        """Gets the request_id of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501


        :return: The request_id of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.


        :param request_id: The request_id of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :type: str
        """

        self._request_id = request_id

    @property
    def vendor(self):
        """Gets the vendor of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501


        :return: The vendor of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :rtype: str
        """
        return self._vendor

    @vendor.setter
    def vendor(self, vendor):
        """Sets the vendor of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.


        :param vendor: The vendor of this VendorsMetaDataForDescribeContentTaskByTaskIdOutput.  # noqa: E501
        :type: str
        """

        self._vendor = vendor

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
        if issubclass(VendorsMetaDataForDescribeContentTaskByTaskIdOutput, dict):
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
        if not isinstance(other, VendorsMetaDataForDescribeContentTaskByTaskIdOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, VendorsMetaDataForDescribeContentTaskByTaskIdOutput):
            return True

        return self.to_dict() != other.to_dict()
