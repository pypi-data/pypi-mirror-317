# coding: utf-8

"""
    mongodb

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DescribeDBInstanceBackupURLResponse(object):
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
        'backup_download_link': 'str',
        'backup_id': 'str',
        'download_progress': 'int',
        'instance_id': 'str',
        'link_expired_time': 'str'
    }

    attribute_map = {
        'backup_download_link': 'BackupDownloadLink',
        'backup_id': 'BackupId',
        'download_progress': 'DownloadProgress',
        'instance_id': 'InstanceId',
        'link_expired_time': 'LinkExpiredTime'
    }

    def __init__(self, backup_download_link=None, backup_id=None, download_progress=None, instance_id=None, link_expired_time=None, _configuration=None):  # noqa: E501
        """DescribeDBInstanceBackupURLResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._backup_download_link = None
        self._backup_id = None
        self._download_progress = None
        self._instance_id = None
        self._link_expired_time = None
        self.discriminator = None

        if backup_download_link is not None:
            self.backup_download_link = backup_download_link
        if backup_id is not None:
            self.backup_id = backup_id
        if download_progress is not None:
            self.download_progress = download_progress
        if instance_id is not None:
            self.instance_id = instance_id
        if link_expired_time is not None:
            self.link_expired_time = link_expired_time

    @property
    def backup_download_link(self):
        """Gets the backup_download_link of this DescribeDBInstanceBackupURLResponse.  # noqa: E501


        :return: The backup_download_link of this DescribeDBInstanceBackupURLResponse.  # noqa: E501
        :rtype: str
        """
        return self._backup_download_link

    @backup_download_link.setter
    def backup_download_link(self, backup_download_link):
        """Sets the backup_download_link of this DescribeDBInstanceBackupURLResponse.


        :param backup_download_link: The backup_download_link of this DescribeDBInstanceBackupURLResponse.  # noqa: E501
        :type: str
        """

        self._backup_download_link = backup_download_link

    @property
    def backup_id(self):
        """Gets the backup_id of this DescribeDBInstanceBackupURLResponse.  # noqa: E501


        :return: The backup_id of this DescribeDBInstanceBackupURLResponse.  # noqa: E501
        :rtype: str
        """
        return self._backup_id

    @backup_id.setter
    def backup_id(self, backup_id):
        """Sets the backup_id of this DescribeDBInstanceBackupURLResponse.


        :param backup_id: The backup_id of this DescribeDBInstanceBackupURLResponse.  # noqa: E501
        :type: str
        """

        self._backup_id = backup_id

    @property
    def download_progress(self):
        """Gets the download_progress of this DescribeDBInstanceBackupURLResponse.  # noqa: E501


        :return: The download_progress of this DescribeDBInstanceBackupURLResponse.  # noqa: E501
        :rtype: int
        """
        return self._download_progress

    @download_progress.setter
    def download_progress(self, download_progress):
        """Sets the download_progress of this DescribeDBInstanceBackupURLResponse.


        :param download_progress: The download_progress of this DescribeDBInstanceBackupURLResponse.  # noqa: E501
        :type: int
        """

        self._download_progress = download_progress

    @property
    def instance_id(self):
        """Gets the instance_id of this DescribeDBInstanceBackupURLResponse.  # noqa: E501


        :return: The instance_id of this DescribeDBInstanceBackupURLResponse.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this DescribeDBInstanceBackupURLResponse.


        :param instance_id: The instance_id of this DescribeDBInstanceBackupURLResponse.  # noqa: E501
        :type: str
        """

        self._instance_id = instance_id

    @property
    def link_expired_time(self):
        """Gets the link_expired_time of this DescribeDBInstanceBackupURLResponse.  # noqa: E501


        :return: The link_expired_time of this DescribeDBInstanceBackupURLResponse.  # noqa: E501
        :rtype: str
        """
        return self._link_expired_time

    @link_expired_time.setter
    def link_expired_time(self, link_expired_time):
        """Sets the link_expired_time of this DescribeDBInstanceBackupURLResponse.


        :param link_expired_time: The link_expired_time of this DescribeDBInstanceBackupURLResponse.  # noqa: E501
        :type: str
        """

        self._link_expired_time = link_expired_time

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
        if issubclass(DescribeDBInstanceBackupURLResponse, dict):
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
        if not isinstance(other, DescribeDBInstanceBackupURLResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeDBInstanceBackupURLResponse):
            return True

        return self.to_dict() != other.to_dict()
