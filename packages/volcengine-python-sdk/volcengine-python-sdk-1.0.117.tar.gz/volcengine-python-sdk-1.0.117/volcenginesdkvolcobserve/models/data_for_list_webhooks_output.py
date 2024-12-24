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


class DataForListWebhooksOutput(object):
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
        'created_at': 'str',
        'event_rule_ids': 'list[str]',
        'id': 'str',
        'name': 'str',
        'rule_ids': 'list[str]',
        'type': 'str',
        'updated_at': 'str',
        'url': 'str'
    }

    attribute_map = {
        'created_at': 'CreatedAt',
        'event_rule_ids': 'EventRuleIds',
        'id': 'Id',
        'name': 'Name',
        'rule_ids': 'RuleIds',
        'type': 'Type',
        'updated_at': 'UpdatedAt',
        'url': 'Url'
    }

    def __init__(self, created_at=None, event_rule_ids=None, id=None, name=None, rule_ids=None, type=None, updated_at=None, url=None, _configuration=None):  # noqa: E501
        """DataForListWebhooksOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._created_at = None
        self._event_rule_ids = None
        self._id = None
        self._name = None
        self._rule_ids = None
        self._type = None
        self._updated_at = None
        self._url = None
        self.discriminator = None

        if created_at is not None:
            self.created_at = created_at
        if event_rule_ids is not None:
            self.event_rule_ids = event_rule_ids
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if rule_ids is not None:
            self.rule_ids = rule_ids
        if type is not None:
            self.type = type
        if updated_at is not None:
            self.updated_at = updated_at
        if url is not None:
            self.url = url

    @property
    def created_at(self):
        """Gets the created_at of this DataForListWebhooksOutput.  # noqa: E501


        :return: The created_at of this DataForListWebhooksOutput.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this DataForListWebhooksOutput.


        :param created_at: The created_at of this DataForListWebhooksOutput.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def event_rule_ids(self):
        """Gets the event_rule_ids of this DataForListWebhooksOutput.  # noqa: E501


        :return: The event_rule_ids of this DataForListWebhooksOutput.  # noqa: E501
        :rtype: list[str]
        """
        return self._event_rule_ids

    @event_rule_ids.setter
    def event_rule_ids(self, event_rule_ids):
        """Sets the event_rule_ids of this DataForListWebhooksOutput.


        :param event_rule_ids: The event_rule_ids of this DataForListWebhooksOutput.  # noqa: E501
        :type: list[str]
        """

        self._event_rule_ids = event_rule_ids

    @property
    def id(self):
        """Gets the id of this DataForListWebhooksOutput.  # noqa: E501


        :return: The id of this DataForListWebhooksOutput.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DataForListWebhooksOutput.


        :param id: The id of this DataForListWebhooksOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this DataForListWebhooksOutput.  # noqa: E501


        :return: The name of this DataForListWebhooksOutput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DataForListWebhooksOutput.


        :param name: The name of this DataForListWebhooksOutput.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def rule_ids(self):
        """Gets the rule_ids of this DataForListWebhooksOutput.  # noqa: E501


        :return: The rule_ids of this DataForListWebhooksOutput.  # noqa: E501
        :rtype: list[str]
        """
        return self._rule_ids

    @rule_ids.setter
    def rule_ids(self, rule_ids):
        """Sets the rule_ids of this DataForListWebhooksOutput.


        :param rule_ids: The rule_ids of this DataForListWebhooksOutput.  # noqa: E501
        :type: list[str]
        """

        self._rule_ids = rule_ids

    @property
    def type(self):
        """Gets the type of this DataForListWebhooksOutput.  # noqa: E501


        :return: The type of this DataForListWebhooksOutput.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this DataForListWebhooksOutput.


        :param type: The type of this DataForListWebhooksOutput.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def updated_at(self):
        """Gets the updated_at of this DataForListWebhooksOutput.  # noqa: E501


        :return: The updated_at of this DataForListWebhooksOutput.  # noqa: E501
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this DataForListWebhooksOutput.


        :param updated_at: The updated_at of this DataForListWebhooksOutput.  # noqa: E501
        :type: str
        """

        self._updated_at = updated_at

    @property
    def url(self):
        """Gets the url of this DataForListWebhooksOutput.  # noqa: E501


        :return: The url of this DataForListWebhooksOutput.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this DataForListWebhooksOutput.


        :param url: The url of this DataForListWebhooksOutput.  # noqa: E501
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
        if issubclass(DataForListWebhooksOutput, dict):
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
        if not isinstance(other, DataForListWebhooksOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DataForListWebhooksOutput):
            return True

        return self.to_dict() != other.to_dict()
