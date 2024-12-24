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


class ListBotAnalyseProtectRulePriorityAvailableRequest(object):
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
        'bot_space': 'str',
        'host': 'str',
        'page': 'int',
        'page_size': 'int',
        'path': 'str',
        'project_name': 'str'
    }

    attribute_map = {
        'bot_space': 'BotSpace',
        'host': 'Host',
        'page': 'Page',
        'page_size': 'PageSize',
        'path': 'Path',
        'project_name': 'ProjectName'
    }

    def __init__(self, bot_space=None, host=None, page=None, page_size=None, path=None, project_name=None, _configuration=None):  # noqa: E501
        """ListBotAnalyseProtectRulePriorityAvailableRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._bot_space = None
        self._host = None
        self._page = None
        self._page_size = None
        self._path = None
        self._project_name = None
        self.discriminator = None

        self.bot_space = bot_space
        self.host = host
        if page is not None:
            self.page = page
        if page_size is not None:
            self.page_size = page_size
        self.path = path
        if project_name is not None:
            self.project_name = project_name

    @property
    def bot_space(self):
        """Gets the bot_space of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501


        :return: The bot_space of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :rtype: str
        """
        return self._bot_space

    @bot_space.setter
    def bot_space(self, bot_space):
        """Sets the bot_space of this ListBotAnalyseProtectRulePriorityAvailableRequest.


        :param bot_space: The bot_space of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and bot_space is None:
            raise ValueError("Invalid value for `bot_space`, must not be `None`")  # noqa: E501

        self._bot_space = bot_space

    @property
    def host(self):
        """Gets the host of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501


        :return: The host of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this ListBotAnalyseProtectRulePriorityAvailableRequest.


        :param host: The host of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and host is None:
            raise ValueError("Invalid value for `host`, must not be `None`")  # noqa: E501

        self._host = host

    @property
    def page(self):
        """Gets the page of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501


        :return: The page of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :rtype: int
        """
        return self._page

    @page.setter
    def page(self, page):
        """Sets the page of this ListBotAnalyseProtectRulePriorityAvailableRequest.


        :param page: The page of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :type: int
        """

        self._page = page

    @property
    def page_size(self):
        """Gets the page_size of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501


        :return: The page_size of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this ListBotAnalyseProtectRulePriorityAvailableRequest.


        :param page_size: The page_size of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

    @property
    def path(self):
        """Gets the path of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501


        :return: The path of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this ListBotAnalyseProtectRulePriorityAvailableRequest.


        :param path: The path of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and path is None:
            raise ValueError("Invalid value for `path`, must not be `None`")  # noqa: E501

        self._path = path

    @property
    def project_name(self):
        """Gets the project_name of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501


        :return: The project_name of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this ListBotAnalyseProtectRulePriorityAvailableRequest.


        :param project_name: The project_name of this ListBotAnalyseProtectRulePriorityAvailableRequest.  # noqa: E501
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
        if issubclass(ListBotAnalyseProtectRulePriorityAvailableRequest, dict):
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
        if not isinstance(other, ListBotAnalyseProtectRulePriorityAvailableRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ListBotAnalyseProtectRulePriorityAvailableRequest):
            return True

        return self.to_dict() != other.to_dict()
