# coding: utf-8

"""
    dms

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ListDataMigrateTaskRequest(object):
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
        'limit': 'int',
        'offset': 'int',
        'task_status': 'str'
    }

    attribute_map = {
        'limit': 'Limit',
        'offset': 'Offset',
        'task_status': 'TaskStatus'
    }

    def __init__(self, limit=None, offset=None, task_status=None, _configuration=None):  # noqa: E501
        """ListDataMigrateTaskRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._limit = None
        self._offset = None
        self._task_status = None
        self.discriminator = None

        if limit is not None:
            self.limit = limit
        self.offset = offset
        if task_status is not None:
            self.task_status = task_status

    @property
    def limit(self):
        """Gets the limit of this ListDataMigrateTaskRequest.  # noqa: E501


        :return: The limit of this ListDataMigrateTaskRequest.  # noqa: E501
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListDataMigrateTaskRequest.


        :param limit: The limit of this ListDataMigrateTaskRequest.  # noqa: E501
        :type: int
        """
        if (self._configuration.client_side_validation and
                limit is not None and limit > 100):  # noqa: E501
            raise ValueError("Invalid value for `limit`, must be a value less than or equal to `100`")  # noqa: E501
        if (self._configuration.client_side_validation and
                limit is not None and limit < 1):  # noqa: E501
            raise ValueError("Invalid value for `limit`, must be a value greater than or equal to `1`")  # noqa: E501

        self._limit = limit

    @property
    def offset(self):
        """Gets the offset of this ListDataMigrateTaskRequest.  # noqa: E501


        :return: The offset of this ListDataMigrateTaskRequest.  # noqa: E501
        :rtype: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this ListDataMigrateTaskRequest.


        :param offset: The offset of this ListDataMigrateTaskRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and offset is None:
            raise ValueError("Invalid value for `offset`, must not be `None`")  # noqa: E501
        if (self._configuration.client_side_validation and
                offset is not None and offset < 0):  # noqa: E501
            raise ValueError("Invalid value for `offset`, must be a value greater than or equal to `0`")  # noqa: E501

        self._offset = offset

    @property
    def task_status(self):
        """Gets the task_status of this ListDataMigrateTaskRequest.  # noqa: E501


        :return: The task_status of this ListDataMigrateTaskRequest.  # noqa: E501
        :rtype: str
        """
        return self._task_status

    @task_status.setter
    def task_status(self, task_status):
        """Sets the task_status of this ListDataMigrateTaskRequest.


        :param task_status: The task_status of this ListDataMigrateTaskRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["Preparing", "Transferring", "Suspended", "Success", "Stopping", "Stopped", "Failure", "ResultGenerating"]  # noqa: E501
        if (self._configuration.client_side_validation and
                task_status not in allowed_values):
            raise ValueError(
                "Invalid value for `task_status` ({0}), must be one of {1}"  # noqa: E501
                .format(task_status, allowed_values)
            )

        self._task_status = task_status

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
        if issubclass(ListDataMigrateTaskRequest, dict):
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
        if not isinstance(other, ListDataMigrateTaskRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ListDataMigrateTaskRequest):
            return True

        return self.to_dict() != other.to_dict()
