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


class TrendForGetRiskStatOutput(object):
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
        'total': 'TotalForGetRiskStatOutput',
        'trend_infos': 'list[TrendInfoForGetRiskStatOutput]'
    }

    attribute_map = {
        'total': 'Total',
        'trend_infos': 'TrendInfos'
    }

    def __init__(self, total=None, trend_infos=None, _configuration=None):  # noqa: E501
        """TrendForGetRiskStatOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._total = None
        self._trend_infos = None
        self.discriminator = None

        if total is not None:
            self.total = total
        if trend_infos is not None:
            self.trend_infos = trend_infos

    @property
    def total(self):
        """Gets the total of this TrendForGetRiskStatOutput.  # noqa: E501


        :return: The total of this TrendForGetRiskStatOutput.  # noqa: E501
        :rtype: TotalForGetRiskStatOutput
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this TrendForGetRiskStatOutput.


        :param total: The total of this TrendForGetRiskStatOutput.  # noqa: E501
        :type: TotalForGetRiskStatOutput
        """

        self._total = total

    @property
    def trend_infos(self):
        """Gets the trend_infos of this TrendForGetRiskStatOutput.  # noqa: E501


        :return: The trend_infos of this TrendForGetRiskStatOutput.  # noqa: E501
        :rtype: list[TrendInfoForGetRiskStatOutput]
        """
        return self._trend_infos

    @trend_infos.setter
    def trend_infos(self, trend_infos):
        """Sets the trend_infos of this TrendForGetRiskStatOutput.


        :param trend_infos: The trend_infos of this TrendForGetRiskStatOutput.  # noqa: E501
        :type: list[TrendInfoForGetRiskStatOutput]
        """

        self._trend_infos = trend_infos

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
        if issubclass(TrendForGetRiskStatOutput, dict):
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
        if not isinstance(other, TrendForGetRiskStatOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TrendForGetRiskStatOutput):
            return True

        return self.to_dict() != other.to_dict()
