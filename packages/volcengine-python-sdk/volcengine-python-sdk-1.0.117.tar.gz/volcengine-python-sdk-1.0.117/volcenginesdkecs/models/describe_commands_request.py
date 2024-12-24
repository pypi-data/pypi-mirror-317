# coding: utf-8

"""
    ecs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeCommandsRequest(object):
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
        'command_id': 'str',
        'content_encoding': 'str',
        'name': 'str',
        'order': 'str',
        'page_number': 'int',
        'page_size': 'int',
        'project_name': 'str',
        'provider': 'str',
        'tag_filters': 'list[TagFilterForDescribeCommandsInput]',
        'type': 'str'
    }

    attribute_map = {
        'command_id': 'CommandId',
        'content_encoding': 'ContentEncoding',
        'name': 'Name',
        'order': 'Order',
        'page_number': 'PageNumber',
        'page_size': 'PageSize',
        'project_name': 'ProjectName',
        'provider': 'Provider',
        'tag_filters': 'TagFilters',
        'type': 'Type'
    }

    def __init__(self, command_id=None, content_encoding=None, name=None, order=None, page_number=None, page_size=None, project_name=None, provider=None, tag_filters=None, type=None, _configuration=None):  # noqa: E501
        """DescribeCommandsRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._command_id = None
        self._content_encoding = None
        self._name = None
        self._order = None
        self._page_number = None
        self._page_size = None
        self._project_name = None
        self._provider = None
        self._tag_filters = None
        self._type = None
        self.discriminator = None

        if command_id is not None:
            self.command_id = command_id
        if content_encoding is not None:
            self.content_encoding = content_encoding
        if name is not None:
            self.name = name
        if order is not None:
            self.order = order
        if page_number is not None:
            self.page_number = page_number
        if page_size is not None:
            self.page_size = page_size
        if project_name is not None:
            self.project_name = project_name
        if provider is not None:
            self.provider = provider
        if tag_filters is not None:
            self.tag_filters = tag_filters
        if type is not None:
            self.type = type

    @property
    def command_id(self):
        """Gets the command_id of this DescribeCommandsRequest.  # noqa: E501


        :return: The command_id of this DescribeCommandsRequest.  # noqa: E501
        :rtype: str
        """
        return self._command_id

    @command_id.setter
    def command_id(self, command_id):
        """Sets the command_id of this DescribeCommandsRequest.


        :param command_id: The command_id of this DescribeCommandsRequest.  # noqa: E501
        :type: str
        """

        self._command_id = command_id

    @property
    def content_encoding(self):
        """Gets the content_encoding of this DescribeCommandsRequest.  # noqa: E501


        :return: The content_encoding of this DescribeCommandsRequest.  # noqa: E501
        :rtype: str
        """
        return self._content_encoding

    @content_encoding.setter
    def content_encoding(self, content_encoding):
        """Sets the content_encoding of this DescribeCommandsRequest.


        :param content_encoding: The content_encoding of this DescribeCommandsRequest.  # noqa: E501
        :type: str
        """

        self._content_encoding = content_encoding

    @property
    def name(self):
        """Gets the name of this DescribeCommandsRequest.  # noqa: E501


        :return: The name of this DescribeCommandsRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DescribeCommandsRequest.


        :param name: The name of this DescribeCommandsRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def order(self):
        """Gets the order of this DescribeCommandsRequest.  # noqa: E501


        :return: The order of this DescribeCommandsRequest.  # noqa: E501
        :rtype: str
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this DescribeCommandsRequest.


        :param order: The order of this DescribeCommandsRequest.  # noqa: E501
        :type: str
        """

        self._order = order

    @property
    def page_number(self):
        """Gets the page_number of this DescribeCommandsRequest.  # noqa: E501


        :return: The page_number of this DescribeCommandsRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this DescribeCommandsRequest.


        :param page_number: The page_number of this DescribeCommandsRequest.  # noqa: E501
        :type: int
        """

        self._page_number = page_number

    @property
    def page_size(self):
        """Gets the page_size of this DescribeCommandsRequest.  # noqa: E501


        :return: The page_size of this DescribeCommandsRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this DescribeCommandsRequest.


        :param page_size: The page_size of this DescribeCommandsRequest.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

    @property
    def project_name(self):
        """Gets the project_name of this DescribeCommandsRequest.  # noqa: E501


        :return: The project_name of this DescribeCommandsRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this DescribeCommandsRequest.


        :param project_name: The project_name of this DescribeCommandsRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def provider(self):
        """Gets the provider of this DescribeCommandsRequest.  # noqa: E501


        :return: The provider of this DescribeCommandsRequest.  # noqa: E501
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """Sets the provider of this DescribeCommandsRequest.


        :param provider: The provider of this DescribeCommandsRequest.  # noqa: E501
        :type: str
        """

        self._provider = provider

    @property
    def tag_filters(self):
        """Gets the tag_filters of this DescribeCommandsRequest.  # noqa: E501


        :return: The tag_filters of this DescribeCommandsRequest.  # noqa: E501
        :rtype: list[TagFilterForDescribeCommandsInput]
        """
        return self._tag_filters

    @tag_filters.setter
    def tag_filters(self, tag_filters):
        """Sets the tag_filters of this DescribeCommandsRequest.


        :param tag_filters: The tag_filters of this DescribeCommandsRequest.  # noqa: E501
        :type: list[TagFilterForDescribeCommandsInput]
        """

        self._tag_filters = tag_filters

    @property
    def type(self):
        """Gets the type of this DescribeCommandsRequest.  # noqa: E501


        :return: The type of this DescribeCommandsRequest.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this DescribeCommandsRequest.


        :param type: The type of this DescribeCommandsRequest.  # noqa: E501
        :type: str
        """

        self._type = type

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
        if issubclass(DescribeCommandsRequest, dict):
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
        if not isinstance(other, DescribeCommandsRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeCommandsRequest):
            return True

        return self.to_dict() != other.to_dict()
