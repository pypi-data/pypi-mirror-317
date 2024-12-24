# coding: utf-8

"""
    mcs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class RiskTopForPostApiV1OverviewDescribeAssetInfoOutput(object):
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
        'resource_cloud_account_id': 'str',
        'resource_id': 'str',
        'resource_name': 'str',
        'resource_type': 'str',
        'resource_vendor': 'str',
        'risk_strategy': 'int',
        'total_strategy': 'int'
    }

    attribute_map = {
        'resource_cloud_account_id': 'resource_cloud_account_id',
        'resource_id': 'resource_id',
        'resource_name': 'resource_name',
        'resource_type': 'resource_type',
        'resource_vendor': 'resource_vendor',
        'risk_strategy': 'risk_strategy',
        'total_strategy': 'total_strategy'
    }

    def __init__(self, resource_cloud_account_id=None, resource_id=None, resource_name=None, resource_type=None, resource_vendor=None, risk_strategy=None, total_strategy=None, _configuration=None):  # noqa: E501
        """RiskTopForPostApiV1OverviewDescribeAssetInfoOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._resource_cloud_account_id = None
        self._resource_id = None
        self._resource_name = None
        self._resource_type = None
        self._resource_vendor = None
        self._risk_strategy = None
        self._total_strategy = None
        self.discriminator = None

        if resource_cloud_account_id is not None:
            self.resource_cloud_account_id = resource_cloud_account_id
        if resource_id is not None:
            self.resource_id = resource_id
        if resource_name is not None:
            self.resource_name = resource_name
        if resource_type is not None:
            self.resource_type = resource_type
        if resource_vendor is not None:
            self.resource_vendor = resource_vendor
        if risk_strategy is not None:
            self.risk_strategy = risk_strategy
        if total_strategy is not None:
            self.total_strategy = total_strategy

    @property
    def resource_cloud_account_id(self):
        """Gets the resource_cloud_account_id of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501


        :return: The resource_cloud_account_id of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :rtype: str
        """
        return self._resource_cloud_account_id

    @resource_cloud_account_id.setter
    def resource_cloud_account_id(self, resource_cloud_account_id):
        """Sets the resource_cloud_account_id of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.


        :param resource_cloud_account_id: The resource_cloud_account_id of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :type: str
        """

        self._resource_cloud_account_id = resource_cloud_account_id

    @property
    def resource_id(self):
        """Gets the resource_id of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501


        :return: The resource_id of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :rtype: str
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        """Sets the resource_id of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.


        :param resource_id: The resource_id of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :type: str
        """

        self._resource_id = resource_id

    @property
    def resource_name(self):
        """Gets the resource_name of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501


        :return: The resource_name of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :rtype: str
        """
        return self._resource_name

    @resource_name.setter
    def resource_name(self, resource_name):
        """Sets the resource_name of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.


        :param resource_name: The resource_name of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :type: str
        """

        self._resource_name = resource_name

    @property
    def resource_type(self):
        """Gets the resource_type of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501


        :return: The resource_type of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """Sets the resource_type of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.


        :param resource_type: The resource_type of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :type: str
        """

        self._resource_type = resource_type

    @property
    def resource_vendor(self):
        """Gets the resource_vendor of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501


        :return: The resource_vendor of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :rtype: str
        """
        return self._resource_vendor

    @resource_vendor.setter
    def resource_vendor(self, resource_vendor):
        """Sets the resource_vendor of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.


        :param resource_vendor: The resource_vendor of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :type: str
        """

        self._resource_vendor = resource_vendor

    @property
    def risk_strategy(self):
        """Gets the risk_strategy of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501


        :return: The risk_strategy of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :rtype: int
        """
        return self._risk_strategy

    @risk_strategy.setter
    def risk_strategy(self, risk_strategy):
        """Sets the risk_strategy of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.


        :param risk_strategy: The risk_strategy of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :type: int
        """

        self._risk_strategy = risk_strategy

    @property
    def total_strategy(self):
        """Gets the total_strategy of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501


        :return: The total_strategy of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :rtype: int
        """
        return self._total_strategy

    @total_strategy.setter
    def total_strategy(self, total_strategy):
        """Sets the total_strategy of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.


        :param total_strategy: The total_strategy of this RiskTopForPostApiV1OverviewDescribeAssetInfoOutput.  # noqa: E501
        :type: int
        """

        self._total_strategy = total_strategy

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
        if issubclass(RiskTopForPostApiV1OverviewDescribeAssetInfoOutput, dict):
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
        if not isinstance(other, RiskTopForPostApiV1OverviewDescribeAssetInfoOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RiskTopForPostApiV1OverviewDescribeAssetInfoOutput):
            return True

        return self.to_dict() != other.to_dict()
