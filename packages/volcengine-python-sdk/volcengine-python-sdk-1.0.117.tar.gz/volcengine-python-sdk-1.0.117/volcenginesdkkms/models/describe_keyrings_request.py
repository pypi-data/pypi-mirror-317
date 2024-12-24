# coding: utf-8

"""
    kms

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeKeyringsRequest(object):
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
        'current_page': 'int',
        'filters': 'str',
        'page_size': 'int',
        'project_name': 'str'
    }

    attribute_map = {
        'current_page': 'CurrentPage',
        'filters': 'Filters',
        'page_size': 'PageSize',
        'project_name': 'ProjectName'
    }

    def __init__(self, current_page=None, filters=None, page_size=None, project_name=None, _configuration=None):  # noqa: E501
        """DescribeKeyringsRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._current_page = None
        self._filters = None
        self._page_size = None
        self._project_name = None
        self.discriminator = None

        if current_page is not None:
            self.current_page = current_page
        if filters is not None:
            self.filters = filters
        if page_size is not None:
            self.page_size = page_size
        if project_name is not None:
            self.project_name = project_name

    @property
    def current_page(self):
        """Gets the current_page of this DescribeKeyringsRequest.  # noqa: E501


        :return: The current_page of this DescribeKeyringsRequest.  # noqa: E501
        :rtype: int
        """
        return self._current_page

    @current_page.setter
    def current_page(self, current_page):
        """Sets the current_page of this DescribeKeyringsRequest.


        :param current_page: The current_page of this DescribeKeyringsRequest.  # noqa: E501
        :type: int
        """
        if (self._configuration.client_side_validation and
                current_page is not None and current_page < 1):  # noqa: E501
            raise ValueError("Invalid value for `current_page`, must be a value greater than or equal to `1`")  # noqa: E501

        self._current_page = current_page

    @property
    def filters(self):
        """Gets the filters of this DescribeKeyringsRequest.  # noqa: E501


        :return: The filters of this DescribeKeyringsRequest.  # noqa: E501
        :rtype: str
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """Sets the filters of this DescribeKeyringsRequest.


        :param filters: The filters of this DescribeKeyringsRequest.  # noqa: E501
        :type: str
        """
        if (self._configuration.client_side_validation and
                filters is not None and len(filters) > 2048):
            raise ValueError("Invalid value for `filters`, length must be less than or equal to `2048`")  # noqa: E501

        self._filters = filters

    @property
    def page_size(self):
        """Gets the page_size of this DescribeKeyringsRequest.  # noqa: E501


        :return: The page_size of this DescribeKeyringsRequest.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this DescribeKeyringsRequest.


        :param page_size: The page_size of this DescribeKeyringsRequest.  # noqa: E501
        :type: int
        """
        if (self._configuration.client_side_validation and
                page_size is not None and page_size > 100):  # noqa: E501
            raise ValueError("Invalid value for `page_size`, must be a value less than or equal to `100`")  # noqa: E501
        if (self._configuration.client_side_validation and
                page_size is not None and page_size < 1):  # noqa: E501
            raise ValueError("Invalid value for `page_size`, must be a value greater than or equal to `1`")  # noqa: E501

        self._page_size = page_size

    @property
    def project_name(self):
        """Gets the project_name of this DescribeKeyringsRequest.  # noqa: E501


        :return: The project_name of this DescribeKeyringsRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this DescribeKeyringsRequest.


        :param project_name: The project_name of this DescribeKeyringsRequest.  # noqa: E501
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
        if issubclass(DescribeKeyringsRequest, dict):
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
        if not isinstance(other, DescribeKeyringsRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeKeyringsRequest):
            return True

        return self.to_dict() != other.to_dict()
