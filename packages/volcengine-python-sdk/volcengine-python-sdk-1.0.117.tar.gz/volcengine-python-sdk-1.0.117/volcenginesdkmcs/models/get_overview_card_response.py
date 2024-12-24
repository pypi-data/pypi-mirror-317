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


class GetOverviewCardResponse(object):
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
        'mc_strategy_risk_cnt': 'int',
        'mc_strategy_risk_list': 'list[MCStrategyRiskListForGetOverviewCardOutput]',
        'mc_strategy_risk_stat': 'list[MCStrategyRiskStatForGetOverviewCardOutput]',
        'risky_resource_cnt': 'int',
        'security_score': 'float',
        'style_type': 'int'
    }

    attribute_map = {
        'mc_strategy_risk_cnt': 'MCStrategyRiskCnt',
        'mc_strategy_risk_list': 'MCStrategyRiskList',
        'mc_strategy_risk_stat': 'MCStrategyRiskStat',
        'risky_resource_cnt': 'RiskyResourceCnt',
        'security_score': 'SecurityScore',
        'style_type': 'StyleType'
    }

    def __init__(self, mc_strategy_risk_cnt=None, mc_strategy_risk_list=None, mc_strategy_risk_stat=None, risky_resource_cnt=None, security_score=None, style_type=None, _configuration=None):  # noqa: E501
        """GetOverviewCardResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._mc_strategy_risk_cnt = None
        self._mc_strategy_risk_list = None
        self._mc_strategy_risk_stat = None
        self._risky_resource_cnt = None
        self._security_score = None
        self._style_type = None
        self.discriminator = None

        if mc_strategy_risk_cnt is not None:
            self.mc_strategy_risk_cnt = mc_strategy_risk_cnt
        if mc_strategy_risk_list is not None:
            self.mc_strategy_risk_list = mc_strategy_risk_list
        if mc_strategy_risk_stat is not None:
            self.mc_strategy_risk_stat = mc_strategy_risk_stat
        if risky_resource_cnt is not None:
            self.risky_resource_cnt = risky_resource_cnt
        if security_score is not None:
            self.security_score = security_score
        if style_type is not None:
            self.style_type = style_type

    @property
    def mc_strategy_risk_cnt(self):
        """Gets the mc_strategy_risk_cnt of this GetOverviewCardResponse.  # noqa: E501


        :return: The mc_strategy_risk_cnt of this GetOverviewCardResponse.  # noqa: E501
        :rtype: int
        """
        return self._mc_strategy_risk_cnt

    @mc_strategy_risk_cnt.setter
    def mc_strategy_risk_cnt(self, mc_strategy_risk_cnt):
        """Sets the mc_strategy_risk_cnt of this GetOverviewCardResponse.


        :param mc_strategy_risk_cnt: The mc_strategy_risk_cnt of this GetOverviewCardResponse.  # noqa: E501
        :type: int
        """

        self._mc_strategy_risk_cnt = mc_strategy_risk_cnt

    @property
    def mc_strategy_risk_list(self):
        """Gets the mc_strategy_risk_list of this GetOverviewCardResponse.  # noqa: E501


        :return: The mc_strategy_risk_list of this GetOverviewCardResponse.  # noqa: E501
        :rtype: list[MCStrategyRiskListForGetOverviewCardOutput]
        """
        return self._mc_strategy_risk_list

    @mc_strategy_risk_list.setter
    def mc_strategy_risk_list(self, mc_strategy_risk_list):
        """Sets the mc_strategy_risk_list of this GetOverviewCardResponse.


        :param mc_strategy_risk_list: The mc_strategy_risk_list of this GetOverviewCardResponse.  # noqa: E501
        :type: list[MCStrategyRiskListForGetOverviewCardOutput]
        """

        self._mc_strategy_risk_list = mc_strategy_risk_list

    @property
    def mc_strategy_risk_stat(self):
        """Gets the mc_strategy_risk_stat of this GetOverviewCardResponse.  # noqa: E501


        :return: The mc_strategy_risk_stat of this GetOverviewCardResponse.  # noqa: E501
        :rtype: list[MCStrategyRiskStatForGetOverviewCardOutput]
        """
        return self._mc_strategy_risk_stat

    @mc_strategy_risk_stat.setter
    def mc_strategy_risk_stat(self, mc_strategy_risk_stat):
        """Sets the mc_strategy_risk_stat of this GetOverviewCardResponse.


        :param mc_strategy_risk_stat: The mc_strategy_risk_stat of this GetOverviewCardResponse.  # noqa: E501
        :type: list[MCStrategyRiskStatForGetOverviewCardOutput]
        """

        self._mc_strategy_risk_stat = mc_strategy_risk_stat

    @property
    def risky_resource_cnt(self):
        """Gets the risky_resource_cnt of this GetOverviewCardResponse.  # noqa: E501


        :return: The risky_resource_cnt of this GetOverviewCardResponse.  # noqa: E501
        :rtype: int
        """
        return self._risky_resource_cnt

    @risky_resource_cnt.setter
    def risky_resource_cnt(self, risky_resource_cnt):
        """Sets the risky_resource_cnt of this GetOverviewCardResponse.


        :param risky_resource_cnt: The risky_resource_cnt of this GetOverviewCardResponse.  # noqa: E501
        :type: int
        """

        self._risky_resource_cnt = risky_resource_cnt

    @property
    def security_score(self):
        """Gets the security_score of this GetOverviewCardResponse.  # noqa: E501


        :return: The security_score of this GetOverviewCardResponse.  # noqa: E501
        :rtype: float
        """
        return self._security_score

    @security_score.setter
    def security_score(self, security_score):
        """Sets the security_score of this GetOverviewCardResponse.


        :param security_score: The security_score of this GetOverviewCardResponse.  # noqa: E501
        :type: float
        """

        self._security_score = security_score

    @property
    def style_type(self):
        """Gets the style_type of this GetOverviewCardResponse.  # noqa: E501


        :return: The style_type of this GetOverviewCardResponse.  # noqa: E501
        :rtype: int
        """
        return self._style_type

    @style_type.setter
    def style_type(self, style_type):
        """Sets the style_type of this GetOverviewCardResponse.


        :param style_type: The style_type of this GetOverviewCardResponse.  # noqa: E501
        :type: int
        """

        self._style_type = style_type

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
        if issubclass(GetOverviewCardResponse, dict):
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
        if not isinstance(other, GetOverviewCardResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GetOverviewCardResponse):
            return True

        return self.to_dict() != other.to_dict()
