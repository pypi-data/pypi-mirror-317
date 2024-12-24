# coding: utf-8

"""
    volc_observe

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ListAlertGroupRequest(object):
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
        'alert_states': 'list[str]',
        'end_at': 'int',
        'levels': 'list[str]',
        'namespaces': 'list[str]',
        'page_number': 'int',
        'page_size': 'int',
        'resource_id': 'str',
        'rule_ids': 'list[str]',
        'rule_name': 'str',
        'start_at': 'int'
    }

    attribute_map = {
        'alert_states': 'AlertStates',
        'end_at': 'EndAt',
        'levels': 'Levels',
        'namespaces': 'Namespaces',
        'page_number': 'PageNumber',
        'page_size': 'PageSize',
        'resource_id': 'ResourceId',
        'rule_ids': 'RuleIds',
        'rule_name': 'RuleName',
        'start_at': 'StartAt'
    }

    def __init__(self, alert_states=None, end_at=None, levels=None, namespaces=None, page_number=None, page_size=None, resource_id=None, rule_ids=None, rule_name=None, start_at=None, _configuration=None):  # noqa: E501
        """ListAlertGroupRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._alert_states = None
        self._end_at = None
        self._levels = None
        self._namespaces = None
        self._page_number = None
        self._page_size = None
        self._resource_id = None
        self._rule_ids = None
        self._rule_name = None
        self._start_at = None
        self.discriminator = None

        if alert_states is not None:
            self.alert_states = alert_states
        if end_at is not None:
            self.end_at = end_at
        if levels is not None:
            self.levels = levels
        if namespaces is not None:
            self.namespaces = namespaces
        if page_number is not None:
            self.page_number = page_number
        if page_size is not None:
            self.page_size = page_size
        if resource_id is not None:
            self.resource_id = resource_id
        if rule_ids is not None:
            self.rule_ids = rule_ids
        if rule_name is not None:
            self.rule_name = rule_name
        if start_at is not None:
            self.start_at = start_at

    @property
    def alert_states(self):
        """Gets the alert_states of this ListAlertGroupRequest.  # noqa: E501


        :return: The alert_states of this ListAlertGroupRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._alert_states

    @alert_states.setter
    def alert_states(self, alert_states):
        """Sets the alert_states of this ListAlertGroupRequest.


        :param alert_states: The alert_states of this ListAlertGroupRequest.  # noqa: E501
        :type: list[str]
        """

        self._alert_states = alert_states

    @property
    def end_at(self):
        """Gets the end_at of this ListAlertGroupRequest.  # noqa: E501


        :return: The end_at of this ListAlertGroupRequest.  # noqa: E501
        :rtype: int
        """
        return self._end_at

    @end_at.setter
    def end_at(self, end_at):
        """Sets the end_at of this ListAlertGroupRequest.


        :param end_at: The end_at of this ListAlertGroupRequest.  # noqa: E501
        :type: int
        """

        self._end_at = end_at

    @property
    def levels(self):
        """Gets the levels of this ListAlertGroupRequest.  # noqa: E501


        :return: The levels of this ListAlertGroupRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._levels

    @levels.setter
    def levels(self, levels):
        """Sets the levels of this ListAlertGroupRequest.


        :param levels: The levels of this ListAlertGroupRequest.  # noqa: E501
        :type: list[str]
        """

        self._levels = levels

    @property
    def namespaces(self):
        """Gets the namespaces of this ListAlertGroupRequest.  # noqa: E501


        :return: The namespaces of this ListAlertGroupRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._namespaces

    @namespaces.setter
    def namespaces(self, namespaces):
        """Sets the namespaces of this ListAlertGroupRequest.


        :param namespaces: The namespaces of this ListAlertGroupRequest.  # noqa: E501
        :type: list[str]
        """

        self._namespaces = namespaces

    @property
    def page_number(self):
        """Gets the page_number of this ListAlertGroupRequest.  # noqa: E501


        :return: The page_number of this ListAlertGroupRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this ListAlertGroupRequest.


        :param page_number: The page_number of this ListAlertGroupRequest.  # noqa: E501
        :type: int
        """

        self._page_number = page_number

    @property
    def page_size(self):
        """Gets the page_size of this ListAlertGroupRequest.  # noqa: E501


        :return: The page_size of this ListAlertGroupRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this ListAlertGroupRequest.


        :param page_size: The page_size of this ListAlertGroupRequest.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

    @property
    def resource_id(self):
        """Gets the resource_id of this ListAlertGroupRequest.  # noqa: E501


        :return: The resource_id of this ListAlertGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        """Sets the resource_id of this ListAlertGroupRequest.


        :param resource_id: The resource_id of this ListAlertGroupRequest.  # noqa: E501
        :type: str
        """

        self._resource_id = resource_id

    @property
    def rule_ids(self):
        """Gets the rule_ids of this ListAlertGroupRequest.  # noqa: E501


        :return: The rule_ids of this ListAlertGroupRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._rule_ids

    @rule_ids.setter
    def rule_ids(self, rule_ids):
        """Sets the rule_ids of this ListAlertGroupRequest.


        :param rule_ids: The rule_ids of this ListAlertGroupRequest.  # noqa: E501
        :type: list[str]
        """

        self._rule_ids = rule_ids

    @property
    def rule_name(self):
        """Gets the rule_name of this ListAlertGroupRequest.  # noqa: E501


        :return: The rule_name of this ListAlertGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._rule_name

    @rule_name.setter
    def rule_name(self, rule_name):
        """Sets the rule_name of this ListAlertGroupRequest.


        :param rule_name: The rule_name of this ListAlertGroupRequest.  # noqa: E501
        :type: str
        """

        self._rule_name = rule_name

    @property
    def start_at(self):
        """Gets the start_at of this ListAlertGroupRequest.  # noqa: E501


        :return: The start_at of this ListAlertGroupRequest.  # noqa: E501
        :rtype: int
        """
        return self._start_at

    @start_at.setter
    def start_at(self, start_at):
        """Sets the start_at of this ListAlertGroupRequest.


        :param start_at: The start_at of this ListAlertGroupRequest.  # noqa: E501
        :type: int
        """

        self._start_at = start_at

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
        if issubclass(ListAlertGroupRequest, dict):
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
        if not isinstance(other, ListAlertGroupRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ListAlertGroupRequest):
            return True

        return self.to_dict() != other.to_dict()
