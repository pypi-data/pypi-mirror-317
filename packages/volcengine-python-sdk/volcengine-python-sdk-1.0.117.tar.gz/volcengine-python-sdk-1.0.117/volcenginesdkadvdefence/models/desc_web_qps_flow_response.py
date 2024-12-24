# coding: utf-8

"""
    advdefence

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescWebQpsFlowResponse(object):
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
        'attack_qps_flow': 'list[AttackQpsFlowForDescWebQpsFlowOutput]',
        'back_src_qps_flow': 'list[BackSrcQpsFlowForDescWebQpsFlowOutput]',
        'in_qps_flow': 'list[InQpsFlowForDescWebQpsFlowOutput]',
        'peak_attack_qps': 'float',
        'peak_attack_qps_flow': 'list[PeakAttackQpsFlowForDescWebQpsFlowOutput]',
        'peak_back_src_qps_flow': 'list[PeakBackSrcQpsFlowForDescWebQpsFlowOutput]',
        'peak_in_qps_flow': 'list[PeakInQpsFlowForDescWebQpsFlowOutput]'
    }

    attribute_map = {
        'attack_qps_flow': 'AttackQpsFlow',
        'back_src_qps_flow': 'BackSrcQpsFlow',
        'in_qps_flow': 'InQpsFlow',
        'peak_attack_qps': 'PeakAttackQps',
        'peak_attack_qps_flow': 'PeakAttackQpsFlow',
        'peak_back_src_qps_flow': 'PeakBackSrcQpsFlow',
        'peak_in_qps_flow': 'PeakInQpsFlow'
    }

    def __init__(self, attack_qps_flow=None, back_src_qps_flow=None, in_qps_flow=None, peak_attack_qps=None, peak_attack_qps_flow=None, peak_back_src_qps_flow=None, peak_in_qps_flow=None, _configuration=None):  # noqa: E501
        """DescWebQpsFlowResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._attack_qps_flow = None
        self._back_src_qps_flow = None
        self._in_qps_flow = None
        self._peak_attack_qps = None
        self._peak_attack_qps_flow = None
        self._peak_back_src_qps_flow = None
        self._peak_in_qps_flow = None
        self.discriminator = None

        if attack_qps_flow is not None:
            self.attack_qps_flow = attack_qps_flow
        if back_src_qps_flow is not None:
            self.back_src_qps_flow = back_src_qps_flow
        if in_qps_flow is not None:
            self.in_qps_flow = in_qps_flow
        if peak_attack_qps is not None:
            self.peak_attack_qps = peak_attack_qps
        if peak_attack_qps_flow is not None:
            self.peak_attack_qps_flow = peak_attack_qps_flow
        if peak_back_src_qps_flow is not None:
            self.peak_back_src_qps_flow = peak_back_src_qps_flow
        if peak_in_qps_flow is not None:
            self.peak_in_qps_flow = peak_in_qps_flow

    @property
    def attack_qps_flow(self):
        """Gets the attack_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501


        :return: The attack_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :rtype: list[AttackQpsFlowForDescWebQpsFlowOutput]
        """
        return self._attack_qps_flow

    @attack_qps_flow.setter
    def attack_qps_flow(self, attack_qps_flow):
        """Sets the attack_qps_flow of this DescWebQpsFlowResponse.


        :param attack_qps_flow: The attack_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :type: list[AttackQpsFlowForDescWebQpsFlowOutput]
        """

        self._attack_qps_flow = attack_qps_flow

    @property
    def back_src_qps_flow(self):
        """Gets the back_src_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501


        :return: The back_src_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :rtype: list[BackSrcQpsFlowForDescWebQpsFlowOutput]
        """
        return self._back_src_qps_flow

    @back_src_qps_flow.setter
    def back_src_qps_flow(self, back_src_qps_flow):
        """Sets the back_src_qps_flow of this DescWebQpsFlowResponse.


        :param back_src_qps_flow: The back_src_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :type: list[BackSrcQpsFlowForDescWebQpsFlowOutput]
        """

        self._back_src_qps_flow = back_src_qps_flow

    @property
    def in_qps_flow(self):
        """Gets the in_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501


        :return: The in_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :rtype: list[InQpsFlowForDescWebQpsFlowOutput]
        """
        return self._in_qps_flow

    @in_qps_flow.setter
    def in_qps_flow(self, in_qps_flow):
        """Sets the in_qps_flow of this DescWebQpsFlowResponse.


        :param in_qps_flow: The in_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :type: list[InQpsFlowForDescWebQpsFlowOutput]
        """

        self._in_qps_flow = in_qps_flow

    @property
    def peak_attack_qps(self):
        """Gets the peak_attack_qps of this DescWebQpsFlowResponse.  # noqa: E501


        :return: The peak_attack_qps of this DescWebQpsFlowResponse.  # noqa: E501
        :rtype: float
        """
        return self._peak_attack_qps

    @peak_attack_qps.setter
    def peak_attack_qps(self, peak_attack_qps):
        """Sets the peak_attack_qps of this DescWebQpsFlowResponse.


        :param peak_attack_qps: The peak_attack_qps of this DescWebQpsFlowResponse.  # noqa: E501
        :type: float
        """

        self._peak_attack_qps = peak_attack_qps

    @property
    def peak_attack_qps_flow(self):
        """Gets the peak_attack_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501


        :return: The peak_attack_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :rtype: list[PeakAttackQpsFlowForDescWebQpsFlowOutput]
        """
        return self._peak_attack_qps_flow

    @peak_attack_qps_flow.setter
    def peak_attack_qps_flow(self, peak_attack_qps_flow):
        """Sets the peak_attack_qps_flow of this DescWebQpsFlowResponse.


        :param peak_attack_qps_flow: The peak_attack_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :type: list[PeakAttackQpsFlowForDescWebQpsFlowOutput]
        """

        self._peak_attack_qps_flow = peak_attack_qps_flow

    @property
    def peak_back_src_qps_flow(self):
        """Gets the peak_back_src_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501


        :return: The peak_back_src_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :rtype: list[PeakBackSrcQpsFlowForDescWebQpsFlowOutput]
        """
        return self._peak_back_src_qps_flow

    @peak_back_src_qps_flow.setter
    def peak_back_src_qps_flow(self, peak_back_src_qps_flow):
        """Sets the peak_back_src_qps_flow of this DescWebQpsFlowResponse.


        :param peak_back_src_qps_flow: The peak_back_src_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :type: list[PeakBackSrcQpsFlowForDescWebQpsFlowOutput]
        """

        self._peak_back_src_qps_flow = peak_back_src_qps_flow

    @property
    def peak_in_qps_flow(self):
        """Gets the peak_in_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501


        :return: The peak_in_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :rtype: list[PeakInQpsFlowForDescWebQpsFlowOutput]
        """
        return self._peak_in_qps_flow

    @peak_in_qps_flow.setter
    def peak_in_qps_flow(self, peak_in_qps_flow):
        """Sets the peak_in_qps_flow of this DescWebQpsFlowResponse.


        :param peak_in_qps_flow: The peak_in_qps_flow of this DescWebQpsFlowResponse.  # noqa: E501
        :type: list[PeakInQpsFlowForDescWebQpsFlowOutput]
        """

        self._peak_in_qps_flow = peak_in_qps_flow

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
        if issubclass(DescWebQpsFlowResponse, dict):
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
        if not isinstance(other, DescWebQpsFlowResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescWebQpsFlowResponse):
            return True

        return self.to_dict() != other.to_dict()
