# coding: utf-8

"""
    advdefence20230308

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class NewConnFlowForDescribeBizFlowAndConnCountOutput(object):
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
        'avg_flows': 'list[AvgFlowForDescribeBizFlowAndConnCountOutput]',
        'max_avg_value': 'int',
        'peak_flows': 'list[PeakFlowForDescribeBizFlowAndConnCountOutput]',
        'peak_value': 'int'
    }

    attribute_map = {
        'avg_flows': 'AvgFlows',
        'max_avg_value': 'MaxAvgValue',
        'peak_flows': 'PeakFlows',
        'peak_value': 'PeakValue'
    }

    def __init__(self, avg_flows=None, max_avg_value=None, peak_flows=None, peak_value=None, _configuration=None):  # noqa: E501
        """NewConnFlowForDescribeBizFlowAndConnCountOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._avg_flows = None
        self._max_avg_value = None
        self._peak_flows = None
        self._peak_value = None
        self.discriminator = None

        if avg_flows is not None:
            self.avg_flows = avg_flows
        if max_avg_value is not None:
            self.max_avg_value = max_avg_value
        if peak_flows is not None:
            self.peak_flows = peak_flows
        if peak_value is not None:
            self.peak_value = peak_value

    @property
    def avg_flows(self):
        """Gets the avg_flows of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501


        :return: The avg_flows of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501
        :rtype: list[AvgFlowForDescribeBizFlowAndConnCountOutput]
        """
        return self._avg_flows

    @avg_flows.setter
    def avg_flows(self, avg_flows):
        """Sets the avg_flows of this NewConnFlowForDescribeBizFlowAndConnCountOutput.


        :param avg_flows: The avg_flows of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501
        :type: list[AvgFlowForDescribeBizFlowAndConnCountOutput]
        """

        self._avg_flows = avg_flows

    @property
    def max_avg_value(self):
        """Gets the max_avg_value of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501


        :return: The max_avg_value of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501
        :rtype: int
        """
        return self._max_avg_value

    @max_avg_value.setter
    def max_avg_value(self, max_avg_value):
        """Sets the max_avg_value of this NewConnFlowForDescribeBizFlowAndConnCountOutput.


        :param max_avg_value: The max_avg_value of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501
        :type: int
        """

        self._max_avg_value = max_avg_value

    @property
    def peak_flows(self):
        """Gets the peak_flows of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501


        :return: The peak_flows of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501
        :rtype: list[PeakFlowForDescribeBizFlowAndConnCountOutput]
        """
        return self._peak_flows

    @peak_flows.setter
    def peak_flows(self, peak_flows):
        """Sets the peak_flows of this NewConnFlowForDescribeBizFlowAndConnCountOutput.


        :param peak_flows: The peak_flows of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501
        :type: list[PeakFlowForDescribeBizFlowAndConnCountOutput]
        """

        self._peak_flows = peak_flows

    @property
    def peak_value(self):
        """Gets the peak_value of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501


        :return: The peak_value of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501
        :rtype: int
        """
        return self._peak_value

    @peak_value.setter
    def peak_value(self, peak_value):
        """Sets the peak_value of this NewConnFlowForDescribeBizFlowAndConnCountOutput.


        :param peak_value: The peak_value of this NewConnFlowForDescribeBizFlowAndConnCountOutput.  # noqa: E501
        :type: int
        """

        self._peak_value = peak_value

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
        if issubclass(NewConnFlowForDescribeBizFlowAndConnCountOutput, dict):
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
        if not isinstance(other, NewConnFlowForDescribeBizFlowAndConnCountOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NewConnFlowForDescribeBizFlowAndConnCountOutput):
            return True

        return self.to_dict() != other.to_dict()
