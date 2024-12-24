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


class PostApiV1AlarmDescribeOverviewRequest(object):
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
        'cloud_account_list': 'list[CloudAccountListForPostApiV1AlarmDescribeOverviewInput]',
        'resource_cloud_vendor_list': 'list[str]'
    }

    attribute_map = {
        'cloud_account_list': 'cloud_account_list',
        'resource_cloud_vendor_list': 'resource_cloud_vendor_list'
    }

    def __init__(self, cloud_account_list=None, resource_cloud_vendor_list=None, _configuration=None):  # noqa: E501
        """PostApiV1AlarmDescribeOverviewRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cloud_account_list = None
        self._resource_cloud_vendor_list = None
        self.discriminator = None

        if cloud_account_list is not None:
            self.cloud_account_list = cloud_account_list
        if resource_cloud_vendor_list is not None:
            self.resource_cloud_vendor_list = resource_cloud_vendor_list

    @property
    def cloud_account_list(self):
        """Gets the cloud_account_list of this PostApiV1AlarmDescribeOverviewRequest.  # noqa: E501


        :return: The cloud_account_list of this PostApiV1AlarmDescribeOverviewRequest.  # noqa: E501
        :rtype: list[CloudAccountListForPostApiV1AlarmDescribeOverviewInput]
        """
        return self._cloud_account_list

    @cloud_account_list.setter
    def cloud_account_list(self, cloud_account_list):
        """Sets the cloud_account_list of this PostApiV1AlarmDescribeOverviewRequest.


        :param cloud_account_list: The cloud_account_list of this PostApiV1AlarmDescribeOverviewRequest.  # noqa: E501
        :type: list[CloudAccountListForPostApiV1AlarmDescribeOverviewInput]
        """

        self._cloud_account_list = cloud_account_list

    @property
    def resource_cloud_vendor_list(self):
        """Gets the resource_cloud_vendor_list of this PostApiV1AlarmDescribeOverviewRequest.  # noqa: E501


        :return: The resource_cloud_vendor_list of this PostApiV1AlarmDescribeOverviewRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._resource_cloud_vendor_list

    @resource_cloud_vendor_list.setter
    def resource_cloud_vendor_list(self, resource_cloud_vendor_list):
        """Sets the resource_cloud_vendor_list of this PostApiV1AlarmDescribeOverviewRequest.


        :param resource_cloud_vendor_list: The resource_cloud_vendor_list of this PostApiV1AlarmDescribeOverviewRequest.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["volcengine", "aliyun", "huaweicloud", "tencent"]  # noqa: E501
        if (self._configuration.client_side_validation and
                not set(resource_cloud_vendor_list).issubset(set(allowed_values))):  # noqa: E501
            raise ValueError(
                "Invalid values for `resource_cloud_vendor_list` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(resource_cloud_vendor_list) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._resource_cloud_vendor_list = resource_cloud_vendor_list

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
        if issubclass(PostApiV1AlarmDescribeOverviewRequest, dict):
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
        if not isinstance(other, PostApiV1AlarmDescribeOverviewRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PostApiV1AlarmDescribeOverviewRequest):
            return True

        return self.to_dict() != other.to_dict()
