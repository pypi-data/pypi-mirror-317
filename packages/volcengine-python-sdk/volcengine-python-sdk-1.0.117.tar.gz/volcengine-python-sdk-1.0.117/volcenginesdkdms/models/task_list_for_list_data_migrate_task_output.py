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


class TaskListForListDataMigrateTaskOutput(object):
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
        'create_time': 'str',
        'task_id': 'int',
        'task_name': 'str',
        'task_progress': 'TaskProgressForListDataMigrateTaskOutput',
        'task_status': 'str'
    }

    attribute_map = {
        'create_time': 'CreateTime',
        'task_id': 'TaskID',
        'task_name': 'TaskName',
        'task_progress': 'TaskProgress',
        'task_status': 'TaskStatus'
    }

    def __init__(self, create_time=None, task_id=None, task_name=None, task_progress=None, task_status=None, _configuration=None):  # noqa: E501
        """TaskListForListDataMigrateTaskOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._create_time = None
        self._task_id = None
        self._task_name = None
        self._task_progress = None
        self._task_status = None
        self.discriminator = None

        if create_time is not None:
            self.create_time = create_time
        if task_id is not None:
            self.task_id = task_id
        if task_name is not None:
            self.task_name = task_name
        if task_progress is not None:
            self.task_progress = task_progress
        if task_status is not None:
            self.task_status = task_status

    @property
    def create_time(self):
        """Gets the create_time of this TaskListForListDataMigrateTaskOutput.  # noqa: E501


        :return: The create_time of this TaskListForListDataMigrateTaskOutput.  # noqa: E501
        :rtype: str
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this TaskListForListDataMigrateTaskOutput.


        :param create_time: The create_time of this TaskListForListDataMigrateTaskOutput.  # noqa: E501
        :type: str
        """

        self._create_time = create_time

    @property
    def task_id(self):
        """Gets the task_id of this TaskListForListDataMigrateTaskOutput.  # noqa: E501


        :return: The task_id of this TaskListForListDataMigrateTaskOutput.  # noqa: E501
        :rtype: int
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this TaskListForListDataMigrateTaskOutput.


        :param task_id: The task_id of this TaskListForListDataMigrateTaskOutput.  # noqa: E501
        :type: int
        """

        self._task_id = task_id

    @property
    def task_name(self):
        """Gets the task_name of this TaskListForListDataMigrateTaskOutput.  # noqa: E501


        :return: The task_name of this TaskListForListDataMigrateTaskOutput.  # noqa: E501
        :rtype: str
        """
        return self._task_name

    @task_name.setter
    def task_name(self, task_name):
        """Sets the task_name of this TaskListForListDataMigrateTaskOutput.


        :param task_name: The task_name of this TaskListForListDataMigrateTaskOutput.  # noqa: E501
        :type: str
        """

        self._task_name = task_name

    @property
    def task_progress(self):
        """Gets the task_progress of this TaskListForListDataMigrateTaskOutput.  # noqa: E501


        :return: The task_progress of this TaskListForListDataMigrateTaskOutput.  # noqa: E501
        :rtype: TaskProgressForListDataMigrateTaskOutput
        """
        return self._task_progress

    @task_progress.setter
    def task_progress(self, task_progress):
        """Sets the task_progress of this TaskListForListDataMigrateTaskOutput.


        :param task_progress: The task_progress of this TaskListForListDataMigrateTaskOutput.  # noqa: E501
        :type: TaskProgressForListDataMigrateTaskOutput
        """

        self._task_progress = task_progress

    @property
    def task_status(self):
        """Gets the task_status of this TaskListForListDataMigrateTaskOutput.  # noqa: E501


        :return: The task_status of this TaskListForListDataMigrateTaskOutput.  # noqa: E501
        :rtype: str
        """
        return self._task_status

    @task_status.setter
    def task_status(self, task_status):
        """Sets the task_status of this TaskListForListDataMigrateTaskOutput.


        :param task_status: The task_status of this TaskListForListDataMigrateTaskOutput.  # noqa: E501
        :type: str
        """

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
        if issubclass(TaskListForListDataMigrateTaskOutput, dict):
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
        if not isinstance(other, TaskListForListDataMigrateTaskOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TaskListForListDataMigrateTaskOutput):
            return True

        return self.to_dict() != other.to_dict()
