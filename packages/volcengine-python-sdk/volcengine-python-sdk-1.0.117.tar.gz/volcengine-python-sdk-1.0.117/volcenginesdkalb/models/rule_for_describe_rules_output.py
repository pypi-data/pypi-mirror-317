# coding: utf-8

"""
    alb

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class RuleForDescribeRulesOutput(object):
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
        'description': 'str',
        'domain': 'str',
        'forward_group_config': 'ForwardGroupConfigForDescribeRulesOutput',
        'redirect_config': 'RedirectConfigForDescribeRulesOutput',
        'rewrite_config': 'RewriteConfigForDescribeRulesOutput',
        'rewrite_enabled': 'str',
        'rule_action': 'str',
        'rule_id': 'str',
        'server_group_id': 'str',
        'traffic_limit_enabled': 'str',
        'traffic_limit_qps': 'int',
        'url': 'str'
    }

    attribute_map = {
        'description': 'Description',
        'domain': 'Domain',
        'forward_group_config': 'ForwardGroupConfig',
        'redirect_config': 'RedirectConfig',
        'rewrite_config': 'RewriteConfig',
        'rewrite_enabled': 'RewriteEnabled',
        'rule_action': 'RuleAction',
        'rule_id': 'RuleId',
        'server_group_id': 'ServerGroupId',
        'traffic_limit_enabled': 'TrafficLimitEnabled',
        'traffic_limit_qps': 'TrafficLimitQPS',
        'url': 'Url'
    }

    def __init__(self, description=None, domain=None, forward_group_config=None, redirect_config=None, rewrite_config=None, rewrite_enabled=None, rule_action=None, rule_id=None, server_group_id=None, traffic_limit_enabled=None, traffic_limit_qps=None, url=None, _configuration=None):  # noqa: E501
        """RuleForDescribeRulesOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._description = None
        self._domain = None
        self._forward_group_config = None
        self._redirect_config = None
        self._rewrite_config = None
        self._rewrite_enabled = None
        self._rule_action = None
        self._rule_id = None
        self._server_group_id = None
        self._traffic_limit_enabled = None
        self._traffic_limit_qps = None
        self._url = None
        self.discriminator = None

        if description is not None:
            self.description = description
        if domain is not None:
            self.domain = domain
        if forward_group_config is not None:
            self.forward_group_config = forward_group_config
        if redirect_config is not None:
            self.redirect_config = redirect_config
        if rewrite_config is not None:
            self.rewrite_config = rewrite_config
        if rewrite_enabled is not None:
            self.rewrite_enabled = rewrite_enabled
        if rule_action is not None:
            self.rule_action = rule_action
        if rule_id is not None:
            self.rule_id = rule_id
        if server_group_id is not None:
            self.server_group_id = server_group_id
        if traffic_limit_enabled is not None:
            self.traffic_limit_enabled = traffic_limit_enabled
        if traffic_limit_qps is not None:
            self.traffic_limit_qps = traffic_limit_qps
        if url is not None:
            self.url = url

    @property
    def description(self):
        """Gets the description of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The description of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this RuleForDescribeRulesOutput.


        :param description: The description of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def domain(self):
        """Gets the domain of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The domain of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this RuleForDescribeRulesOutput.


        :param domain: The domain of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: str
        """

        self._domain = domain

    @property
    def forward_group_config(self):
        """Gets the forward_group_config of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The forward_group_config of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: ForwardGroupConfigForDescribeRulesOutput
        """
        return self._forward_group_config

    @forward_group_config.setter
    def forward_group_config(self, forward_group_config):
        """Sets the forward_group_config of this RuleForDescribeRulesOutput.


        :param forward_group_config: The forward_group_config of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: ForwardGroupConfigForDescribeRulesOutput
        """

        self._forward_group_config = forward_group_config

    @property
    def redirect_config(self):
        """Gets the redirect_config of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The redirect_config of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: RedirectConfigForDescribeRulesOutput
        """
        return self._redirect_config

    @redirect_config.setter
    def redirect_config(self, redirect_config):
        """Sets the redirect_config of this RuleForDescribeRulesOutput.


        :param redirect_config: The redirect_config of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: RedirectConfigForDescribeRulesOutput
        """

        self._redirect_config = redirect_config

    @property
    def rewrite_config(self):
        """Gets the rewrite_config of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The rewrite_config of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: RewriteConfigForDescribeRulesOutput
        """
        return self._rewrite_config

    @rewrite_config.setter
    def rewrite_config(self, rewrite_config):
        """Sets the rewrite_config of this RuleForDescribeRulesOutput.


        :param rewrite_config: The rewrite_config of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: RewriteConfigForDescribeRulesOutput
        """

        self._rewrite_config = rewrite_config

    @property
    def rewrite_enabled(self):
        """Gets the rewrite_enabled of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The rewrite_enabled of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: str
        """
        return self._rewrite_enabled

    @rewrite_enabled.setter
    def rewrite_enabled(self, rewrite_enabled):
        """Sets the rewrite_enabled of this RuleForDescribeRulesOutput.


        :param rewrite_enabled: The rewrite_enabled of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: str
        """

        self._rewrite_enabled = rewrite_enabled

    @property
    def rule_action(self):
        """Gets the rule_action of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The rule_action of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: str
        """
        return self._rule_action

    @rule_action.setter
    def rule_action(self, rule_action):
        """Sets the rule_action of this RuleForDescribeRulesOutput.


        :param rule_action: The rule_action of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: str
        """

        self._rule_action = rule_action

    @property
    def rule_id(self):
        """Gets the rule_id of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The rule_id of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: str
        """
        return self._rule_id

    @rule_id.setter
    def rule_id(self, rule_id):
        """Sets the rule_id of this RuleForDescribeRulesOutput.


        :param rule_id: The rule_id of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: str
        """

        self._rule_id = rule_id

    @property
    def server_group_id(self):
        """Gets the server_group_id of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The server_group_id of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: str
        """
        return self._server_group_id

    @server_group_id.setter
    def server_group_id(self, server_group_id):
        """Sets the server_group_id of this RuleForDescribeRulesOutput.


        :param server_group_id: The server_group_id of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: str
        """

        self._server_group_id = server_group_id

    @property
    def traffic_limit_enabled(self):
        """Gets the traffic_limit_enabled of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The traffic_limit_enabled of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: str
        """
        return self._traffic_limit_enabled

    @traffic_limit_enabled.setter
    def traffic_limit_enabled(self, traffic_limit_enabled):
        """Sets the traffic_limit_enabled of this RuleForDescribeRulesOutput.


        :param traffic_limit_enabled: The traffic_limit_enabled of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: str
        """

        self._traffic_limit_enabled = traffic_limit_enabled

    @property
    def traffic_limit_qps(self):
        """Gets the traffic_limit_qps of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The traffic_limit_qps of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: int
        """
        return self._traffic_limit_qps

    @traffic_limit_qps.setter
    def traffic_limit_qps(self, traffic_limit_qps):
        """Sets the traffic_limit_qps of this RuleForDescribeRulesOutput.


        :param traffic_limit_qps: The traffic_limit_qps of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: int
        """

        self._traffic_limit_qps = traffic_limit_qps

    @property
    def url(self):
        """Gets the url of this RuleForDescribeRulesOutput.  # noqa: E501


        :return: The url of this RuleForDescribeRulesOutput.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this RuleForDescribeRulesOutput.


        :param url: The url of this RuleForDescribeRulesOutput.  # noqa: E501
        :type: str
        """

        self._url = url

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
        if issubclass(RuleForDescribeRulesOutput, dict):
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
        if not isinstance(other, RuleForDescribeRulesOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RuleForDescribeRulesOutput):
            return True

        return self.to_dict() != other.to_dict()
