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


class ValForDescribeAttackFlowOutput(object):
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
        'drop_k_bps_flow': 'list[DropKBpsFlowForDescribeAttackFlowOutput]',
        'drop_pkts_flow': 'list[DropPktsFlowForDescribeAttackFlowOutput]',
        'in_k_bps_flow': 'list[InKBpsFlowForDescribeAttackFlowOutput]',
        'in_pkts_flow': 'list[InPktsFlowForDescribeAttackFlowOutput]',
        'peak_drop_k_bps': 'int',
        'peak_drop_pps': 'int',
        'peak_in_k_bps': 'int',
        'peak_in_pps': 'int'
    }

    attribute_map = {
        'drop_k_bps_flow': 'DropKBpsFlow',
        'drop_pkts_flow': 'DropPktsFlow',
        'in_k_bps_flow': 'InKBpsFlow',
        'in_pkts_flow': 'InPktsFlow',
        'peak_drop_k_bps': 'PeakDropKBps',
        'peak_drop_pps': 'PeakDropPps',
        'peak_in_k_bps': 'PeakInKBps',
        'peak_in_pps': 'PeakInPps'
    }

    def __init__(self, drop_k_bps_flow=None, drop_pkts_flow=None, in_k_bps_flow=None, in_pkts_flow=None, peak_drop_k_bps=None, peak_drop_pps=None, peak_in_k_bps=None, peak_in_pps=None, _configuration=None):  # noqa: E501
        """ValForDescribeAttackFlowOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._drop_k_bps_flow = None
        self._drop_pkts_flow = None
        self._in_k_bps_flow = None
        self._in_pkts_flow = None
        self._peak_drop_k_bps = None
        self._peak_drop_pps = None
        self._peak_in_k_bps = None
        self._peak_in_pps = None
        self.discriminator = None

        if drop_k_bps_flow is not None:
            self.drop_k_bps_flow = drop_k_bps_flow
        if drop_pkts_flow is not None:
            self.drop_pkts_flow = drop_pkts_flow
        if in_k_bps_flow is not None:
            self.in_k_bps_flow = in_k_bps_flow
        if in_pkts_flow is not None:
            self.in_pkts_flow = in_pkts_flow
        if peak_drop_k_bps is not None:
            self.peak_drop_k_bps = peak_drop_k_bps
        if peak_drop_pps is not None:
            self.peak_drop_pps = peak_drop_pps
        if peak_in_k_bps is not None:
            self.peak_in_k_bps = peak_in_k_bps
        if peak_in_pps is not None:
            self.peak_in_pps = peak_in_pps

    @property
    def drop_k_bps_flow(self):
        """Gets the drop_k_bps_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501


        :return: The drop_k_bps_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :rtype: list[DropKBpsFlowForDescribeAttackFlowOutput]
        """
        return self._drop_k_bps_flow

    @drop_k_bps_flow.setter
    def drop_k_bps_flow(self, drop_k_bps_flow):
        """Sets the drop_k_bps_flow of this ValForDescribeAttackFlowOutput.


        :param drop_k_bps_flow: The drop_k_bps_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :type: list[DropKBpsFlowForDescribeAttackFlowOutput]
        """

        self._drop_k_bps_flow = drop_k_bps_flow

    @property
    def drop_pkts_flow(self):
        """Gets the drop_pkts_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501


        :return: The drop_pkts_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :rtype: list[DropPktsFlowForDescribeAttackFlowOutput]
        """
        return self._drop_pkts_flow

    @drop_pkts_flow.setter
    def drop_pkts_flow(self, drop_pkts_flow):
        """Sets the drop_pkts_flow of this ValForDescribeAttackFlowOutput.


        :param drop_pkts_flow: The drop_pkts_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :type: list[DropPktsFlowForDescribeAttackFlowOutput]
        """

        self._drop_pkts_flow = drop_pkts_flow

    @property
    def in_k_bps_flow(self):
        """Gets the in_k_bps_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501


        :return: The in_k_bps_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :rtype: list[InKBpsFlowForDescribeAttackFlowOutput]
        """
        return self._in_k_bps_flow

    @in_k_bps_flow.setter
    def in_k_bps_flow(self, in_k_bps_flow):
        """Sets the in_k_bps_flow of this ValForDescribeAttackFlowOutput.


        :param in_k_bps_flow: The in_k_bps_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :type: list[InKBpsFlowForDescribeAttackFlowOutput]
        """

        self._in_k_bps_flow = in_k_bps_flow

    @property
    def in_pkts_flow(self):
        """Gets the in_pkts_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501


        :return: The in_pkts_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :rtype: list[InPktsFlowForDescribeAttackFlowOutput]
        """
        return self._in_pkts_flow

    @in_pkts_flow.setter
    def in_pkts_flow(self, in_pkts_flow):
        """Sets the in_pkts_flow of this ValForDescribeAttackFlowOutput.


        :param in_pkts_flow: The in_pkts_flow of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :type: list[InPktsFlowForDescribeAttackFlowOutput]
        """

        self._in_pkts_flow = in_pkts_flow

    @property
    def peak_drop_k_bps(self):
        """Gets the peak_drop_k_bps of this ValForDescribeAttackFlowOutput.  # noqa: E501


        :return: The peak_drop_k_bps of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :rtype: int
        """
        return self._peak_drop_k_bps

    @peak_drop_k_bps.setter
    def peak_drop_k_bps(self, peak_drop_k_bps):
        """Sets the peak_drop_k_bps of this ValForDescribeAttackFlowOutput.


        :param peak_drop_k_bps: The peak_drop_k_bps of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :type: int
        """

        self._peak_drop_k_bps = peak_drop_k_bps

    @property
    def peak_drop_pps(self):
        """Gets the peak_drop_pps of this ValForDescribeAttackFlowOutput.  # noqa: E501


        :return: The peak_drop_pps of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :rtype: int
        """
        return self._peak_drop_pps

    @peak_drop_pps.setter
    def peak_drop_pps(self, peak_drop_pps):
        """Sets the peak_drop_pps of this ValForDescribeAttackFlowOutput.


        :param peak_drop_pps: The peak_drop_pps of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :type: int
        """

        self._peak_drop_pps = peak_drop_pps

    @property
    def peak_in_k_bps(self):
        """Gets the peak_in_k_bps of this ValForDescribeAttackFlowOutput.  # noqa: E501


        :return: The peak_in_k_bps of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :rtype: int
        """
        return self._peak_in_k_bps

    @peak_in_k_bps.setter
    def peak_in_k_bps(self, peak_in_k_bps):
        """Sets the peak_in_k_bps of this ValForDescribeAttackFlowOutput.


        :param peak_in_k_bps: The peak_in_k_bps of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :type: int
        """

        self._peak_in_k_bps = peak_in_k_bps

    @property
    def peak_in_pps(self):
        """Gets the peak_in_pps of this ValForDescribeAttackFlowOutput.  # noqa: E501


        :return: The peak_in_pps of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :rtype: int
        """
        return self._peak_in_pps

    @peak_in_pps.setter
    def peak_in_pps(self, peak_in_pps):
        """Sets the peak_in_pps of this ValForDescribeAttackFlowOutput.


        :param peak_in_pps: The peak_in_pps of this ValForDescribeAttackFlowOutput.  # noqa: E501
        :type: int
        """

        self._peak_in_pps = peak_in_pps

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
        if issubclass(ValForDescribeAttackFlowOutput, dict):
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
        if not isinstance(other, ValForDescribeAttackFlowOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ValForDescribeAttackFlowOutput):
            return True

        return self.to_dict() != other.to_dict()
