# coding: utf-8

"""
    waf

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class UpdateCustomBotConfigRequest(object):
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
        'accurate': 'AccurateForUpdateCustomBotConfigInput',
        'action': 'str',
        'bot_type': 'str',
        'description': 'str',
        'enable': 'int',
        'host': 'str',
        'id': 'int',
        'project_name': 'str'
    }

    attribute_map = {
        'accurate': 'Accurate',
        'action': 'Action',
        'bot_type': 'BotType',
        'description': 'Description',
        'enable': 'Enable',
        'host': 'Host',
        'id': 'Id',
        'project_name': 'ProjectName'
    }

    def __init__(self, accurate=None, action=None, bot_type=None, description=None, enable=None, host=None, id=None, project_name=None, _configuration=None):  # noqa: E501
        """UpdateCustomBotConfigRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._accurate = None
        self._action = None
        self._bot_type = None
        self._description = None
        self._enable = None
        self._host = None
        self._id = None
        self._project_name = None
        self.discriminator = None

        if accurate is not None:
            self.accurate = accurate
        self.action = action
        self.bot_type = bot_type
        if description is not None:
            self.description = description
        self.enable = enable
        self.host = host
        self.id = id
        if project_name is not None:
            self.project_name = project_name

    @property
    def accurate(self):
        """Gets the accurate of this UpdateCustomBotConfigRequest.  # noqa: E501


        :return: The accurate of this UpdateCustomBotConfigRequest.  # noqa: E501
        :rtype: AccurateForUpdateCustomBotConfigInput
        """
        return self._accurate

    @accurate.setter
    def accurate(self, accurate):
        """Sets the accurate of this UpdateCustomBotConfigRequest.


        :param accurate: The accurate of this UpdateCustomBotConfigRequest.  # noqa: E501
        :type: AccurateForUpdateCustomBotConfigInput
        """

        self._accurate = accurate

    @property
    def action(self):
        """Gets the action of this UpdateCustomBotConfigRequest.  # noqa: E501


        :return: The action of this UpdateCustomBotConfigRequest.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this UpdateCustomBotConfigRequest.


        :param action: The action of this UpdateCustomBotConfigRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and action is None:
            raise ValueError("Invalid value for `action`, must not be `None`")  # noqa: E501

        self._action = action

    @property
    def bot_type(self):
        """Gets the bot_type of this UpdateCustomBotConfigRequest.  # noqa: E501


        :return: The bot_type of this UpdateCustomBotConfigRequest.  # noqa: E501
        :rtype: str
        """
        return self._bot_type

    @bot_type.setter
    def bot_type(self, bot_type):
        """Sets the bot_type of this UpdateCustomBotConfigRequest.


        :param bot_type: The bot_type of this UpdateCustomBotConfigRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and bot_type is None:
            raise ValueError("Invalid value for `bot_type`, must not be `None`")  # noqa: E501

        self._bot_type = bot_type

    @property
    def description(self):
        """Gets the description of this UpdateCustomBotConfigRequest.  # noqa: E501


        :return: The description of this UpdateCustomBotConfigRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateCustomBotConfigRequest.


        :param description: The description of this UpdateCustomBotConfigRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def enable(self):
        """Gets the enable of this UpdateCustomBotConfigRequest.  # noqa: E501


        :return: The enable of this UpdateCustomBotConfigRequest.  # noqa: E501
        :rtype: int
        """
        return self._enable

    @enable.setter
    def enable(self, enable):
        """Sets the enable of this UpdateCustomBotConfigRequest.


        :param enable: The enable of this UpdateCustomBotConfigRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and enable is None:
            raise ValueError("Invalid value for `enable`, must not be `None`")  # noqa: E501

        self._enable = enable

    @property
    def host(self):
        """Gets the host of this UpdateCustomBotConfigRequest.  # noqa: E501


        :return: The host of this UpdateCustomBotConfigRequest.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this UpdateCustomBotConfigRequest.


        :param host: The host of this UpdateCustomBotConfigRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and host is None:
            raise ValueError("Invalid value for `host`, must not be `None`")  # noqa: E501

        self._host = host

    @property
    def id(self):
        """Gets the id of this UpdateCustomBotConfigRequest.  # noqa: E501


        :return: The id of this UpdateCustomBotConfigRequest.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UpdateCustomBotConfigRequest.


        :param id: The id of this UpdateCustomBotConfigRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def project_name(self):
        """Gets the project_name of this UpdateCustomBotConfigRequest.  # noqa: E501


        :return: The project_name of this UpdateCustomBotConfigRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this UpdateCustomBotConfigRequest.


        :param project_name: The project_name of this UpdateCustomBotConfigRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

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
        if issubclass(UpdateCustomBotConfigRequest, dict):
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
        if not isinstance(other, UpdateCustomBotConfigRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateCustomBotConfigRequest):
            return True

        return self.to_dict() != other.to_dict()
