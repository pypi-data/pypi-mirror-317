# coding: utf-8

"""
    redis

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ModifyEnterpriseDBInstanceCapacityRequest(object):
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
        'apply_immediately': 'bool',
        'backup_point_name': 'str',
        'client_token': 'str',
        'create_backup': 'bool',
        'flash_per_shard': 'int',
        'instance_id': 'str',
        'ram_per_shard': 'int',
        'shard_number': 'int'
    }

    attribute_map = {
        'apply_immediately': 'ApplyImmediately',
        'backup_point_name': 'BackupPointName',
        'client_token': 'ClientToken',
        'create_backup': 'CreateBackup',
        'flash_per_shard': 'FlashPerShard',
        'instance_id': 'InstanceId',
        'ram_per_shard': 'RamPerShard',
        'shard_number': 'ShardNumber'
    }

    def __init__(self, apply_immediately=None, backup_point_name=None, client_token=None, create_backup=None, flash_per_shard=None, instance_id=None, ram_per_shard=None, shard_number=None, _configuration=None):  # noqa: E501
        """ModifyEnterpriseDBInstanceCapacityRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._apply_immediately = None
        self._backup_point_name = None
        self._client_token = None
        self._create_backup = None
        self._flash_per_shard = None
        self._instance_id = None
        self._ram_per_shard = None
        self._shard_number = None
        self.discriminator = None

        self.apply_immediately = apply_immediately
        if backup_point_name is not None:
            self.backup_point_name = backup_point_name
        if client_token is not None:
            self.client_token = client_token
        if create_backup is not None:
            self.create_backup = create_backup
        self.flash_per_shard = flash_per_shard
        self.instance_id = instance_id
        self.ram_per_shard = ram_per_shard
        self.shard_number = shard_number

    @property
    def apply_immediately(self):
        """Gets the apply_immediately of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501


        :return: The apply_immediately of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :rtype: bool
        """
        return self._apply_immediately

    @apply_immediately.setter
    def apply_immediately(self, apply_immediately):
        """Sets the apply_immediately of this ModifyEnterpriseDBInstanceCapacityRequest.


        :param apply_immediately: The apply_immediately of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :type: bool
        """
        if self._configuration.client_side_validation and apply_immediately is None:
            raise ValueError("Invalid value for `apply_immediately`, must not be `None`")  # noqa: E501

        self._apply_immediately = apply_immediately

    @property
    def backup_point_name(self):
        """Gets the backup_point_name of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501


        :return: The backup_point_name of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :rtype: str
        """
        return self._backup_point_name

    @backup_point_name.setter
    def backup_point_name(self, backup_point_name):
        """Sets the backup_point_name of this ModifyEnterpriseDBInstanceCapacityRequest.


        :param backup_point_name: The backup_point_name of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :type: str
        """

        self._backup_point_name = backup_point_name

    @property
    def client_token(self):
        """Gets the client_token of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501


        :return: The client_token of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_token

    @client_token.setter
    def client_token(self, client_token):
        """Sets the client_token of this ModifyEnterpriseDBInstanceCapacityRequest.


        :param client_token: The client_token of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :type: str
        """

        self._client_token = client_token

    @property
    def create_backup(self):
        """Gets the create_backup of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501


        :return: The create_backup of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :rtype: bool
        """
        return self._create_backup

    @create_backup.setter
    def create_backup(self, create_backup):
        """Sets the create_backup of this ModifyEnterpriseDBInstanceCapacityRequest.


        :param create_backup: The create_backup of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :type: bool
        """

        self._create_backup = create_backup

    @property
    def flash_per_shard(self):
        """Gets the flash_per_shard of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501


        :return: The flash_per_shard of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :rtype: int
        """
        return self._flash_per_shard

    @flash_per_shard.setter
    def flash_per_shard(self, flash_per_shard):
        """Sets the flash_per_shard of this ModifyEnterpriseDBInstanceCapacityRequest.


        :param flash_per_shard: The flash_per_shard of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and flash_per_shard is None:
            raise ValueError("Invalid value for `flash_per_shard`, must not be `None`")  # noqa: E501

        self._flash_per_shard = flash_per_shard

    @property
    def instance_id(self):
        """Gets the instance_id of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501


        :return: The instance_id of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this ModifyEnterpriseDBInstanceCapacityRequest.


        :param instance_id: The instance_id of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and instance_id is None:
            raise ValueError("Invalid value for `instance_id`, must not be `None`")  # noqa: E501

        self._instance_id = instance_id

    @property
    def ram_per_shard(self):
        """Gets the ram_per_shard of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501


        :return: The ram_per_shard of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :rtype: int
        """
        return self._ram_per_shard

    @ram_per_shard.setter
    def ram_per_shard(self, ram_per_shard):
        """Sets the ram_per_shard of this ModifyEnterpriseDBInstanceCapacityRequest.


        :param ram_per_shard: The ram_per_shard of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and ram_per_shard is None:
            raise ValueError("Invalid value for `ram_per_shard`, must not be `None`")  # noqa: E501

        self._ram_per_shard = ram_per_shard

    @property
    def shard_number(self):
        """Gets the shard_number of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501


        :return: The shard_number of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :rtype: int
        """
        return self._shard_number

    @shard_number.setter
    def shard_number(self, shard_number):
        """Sets the shard_number of this ModifyEnterpriseDBInstanceCapacityRequest.


        :param shard_number: The shard_number of this ModifyEnterpriseDBInstanceCapacityRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and shard_number is None:
            raise ValueError("Invalid value for `shard_number`, must not be `None`")  # noqa: E501

        self._shard_number = shard_number

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
        if issubclass(ModifyEnterpriseDBInstanceCapacityRequest, dict):
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
        if not isinstance(other, ModifyEnterpriseDBInstanceCapacityRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModifyEnterpriseDBInstanceCapacityRequest):
            return True

        return self.to_dict() != other.to_dict()
