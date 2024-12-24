# coding: utf-8

"""
    filenas

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class CreateFileSystemRequest(object):
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
        'capacity': 'int',
        'charge_type': 'str',
        'client_token': 'str',
        'description': 'str',
        'file_system_name': 'str',
        'file_system_type': 'str',
        'project_name': 'str',
        'protocol_type': 'str',
        'snapshot_id': 'str',
        'storage_type': 'str',
        'tags': 'list[TagForCreateFileSystemInput]',
        'zone_id': 'str'
    }

    attribute_map = {
        'capacity': 'Capacity',
        'charge_type': 'ChargeType',
        'client_token': 'ClientToken',
        'description': 'Description',
        'file_system_name': 'FileSystemName',
        'file_system_type': 'FileSystemType',
        'project_name': 'ProjectName',
        'protocol_type': 'ProtocolType',
        'snapshot_id': 'SnapshotId',
        'storage_type': 'StorageType',
        'tags': 'Tags',
        'zone_id': 'ZoneId'
    }

    def __init__(self, capacity=None, charge_type=None, client_token=None, description=None, file_system_name=None, file_system_type=None, project_name=None, protocol_type=None, snapshot_id=None, storage_type=None, tags=None, zone_id=None, _configuration=None):  # noqa: E501
        """CreateFileSystemRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._capacity = None
        self._charge_type = None
        self._client_token = None
        self._description = None
        self._file_system_name = None
        self._file_system_type = None
        self._project_name = None
        self._protocol_type = None
        self._snapshot_id = None
        self._storage_type = None
        self._tags = None
        self._zone_id = None
        self.discriminator = None

        self.capacity = capacity
        self.charge_type = charge_type
        if client_token is not None:
            self.client_token = client_token
        if description is not None:
            self.description = description
        self.file_system_name = file_system_name
        self.file_system_type = file_system_type
        if project_name is not None:
            self.project_name = project_name
        self.protocol_type = protocol_type
        if snapshot_id is not None:
            self.snapshot_id = snapshot_id
        if storage_type is not None:
            self.storage_type = storage_type
        if tags is not None:
            self.tags = tags
        self.zone_id = zone_id

    @property
    def capacity(self):
        """Gets the capacity of this CreateFileSystemRequest.  # noqa: E501


        :return: The capacity of this CreateFileSystemRequest.  # noqa: E501
        :rtype: int
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this CreateFileSystemRequest.


        :param capacity: The capacity of this CreateFileSystemRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and capacity is None:
            raise ValueError("Invalid value for `capacity`, must not be `None`")  # noqa: E501

        self._capacity = capacity

    @property
    def charge_type(self):
        """Gets the charge_type of this CreateFileSystemRequest.  # noqa: E501


        :return: The charge_type of this CreateFileSystemRequest.  # noqa: E501
        :rtype: str
        """
        return self._charge_type

    @charge_type.setter
    def charge_type(self, charge_type):
        """Sets the charge_type of this CreateFileSystemRequest.


        :param charge_type: The charge_type of this CreateFileSystemRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and charge_type is None:
            raise ValueError("Invalid value for `charge_type`, must not be `None`")  # noqa: E501
        allowed_values = ["PayAsYouGo"]  # noqa: E501
        if (self._configuration.client_side_validation and
                charge_type not in allowed_values):
            raise ValueError(
                "Invalid value for `charge_type` ({0}), must be one of {1}"  # noqa: E501
                .format(charge_type, allowed_values)
            )

        self._charge_type = charge_type

    @property
    def client_token(self):
        """Gets the client_token of this CreateFileSystemRequest.  # noqa: E501


        :return: The client_token of this CreateFileSystemRequest.  # noqa: E501
        :rtype: str
        """
        return self._client_token

    @client_token.setter
    def client_token(self, client_token):
        """Sets the client_token of this CreateFileSystemRequest.


        :param client_token: The client_token of this CreateFileSystemRequest.  # noqa: E501
        :type: str
        """

        self._client_token = client_token

    @property
    def description(self):
        """Gets the description of this CreateFileSystemRequest.  # noqa: E501


        :return: The description of this CreateFileSystemRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateFileSystemRequest.


        :param description: The description of this CreateFileSystemRequest.  # noqa: E501
        :type: str
        """
        if (self._configuration.client_side_validation and
                description is not None and len(description) > 120):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `120`")  # noqa: E501

        self._description = description

    @property
    def file_system_name(self):
        """Gets the file_system_name of this CreateFileSystemRequest.  # noqa: E501


        :return: The file_system_name of this CreateFileSystemRequest.  # noqa: E501
        :rtype: str
        """
        return self._file_system_name

    @file_system_name.setter
    def file_system_name(self, file_system_name):
        """Sets the file_system_name of this CreateFileSystemRequest.


        :param file_system_name: The file_system_name of this CreateFileSystemRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and file_system_name is None:
            raise ValueError("Invalid value for `file_system_name`, must not be `None`")  # noqa: E501
        if (self._configuration.client_side_validation and
                file_system_name is not None and len(file_system_name) > 128):
            raise ValueError("Invalid value for `file_system_name`, length must be less than or equal to `128`")  # noqa: E501
        if (self._configuration.client_side_validation and
                file_system_name is not None and len(file_system_name) < 1):
            raise ValueError("Invalid value for `file_system_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._file_system_name = file_system_name

    @property
    def file_system_type(self):
        """Gets the file_system_type of this CreateFileSystemRequest.  # noqa: E501


        :return: The file_system_type of this CreateFileSystemRequest.  # noqa: E501
        :rtype: str
        """
        return self._file_system_type

    @file_system_type.setter
    def file_system_type(self, file_system_type):
        """Sets the file_system_type of this CreateFileSystemRequest.


        :param file_system_type: The file_system_type of this CreateFileSystemRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and file_system_type is None:
            raise ValueError("Invalid value for `file_system_type`, must not be `None`")  # noqa: E501
        allowed_values = ["Extreme", "Capacity", "Cache"]  # noqa: E501
        if (self._configuration.client_side_validation and
                file_system_type not in allowed_values):
            raise ValueError(
                "Invalid value for `file_system_type` ({0}), must be one of {1}"  # noqa: E501
                .format(file_system_type, allowed_values)
            )

        self._file_system_type = file_system_type

    @property
    def project_name(self):
        """Gets the project_name of this CreateFileSystemRequest.  # noqa: E501


        :return: The project_name of this CreateFileSystemRequest.  # noqa: E501
        :rtype: str
        """
        return self._project_name

    @project_name.setter
    def project_name(self, project_name):
        """Sets the project_name of this CreateFileSystemRequest.


        :param project_name: The project_name of this CreateFileSystemRequest.  # noqa: E501
        :type: str
        """

        self._project_name = project_name

    @property
    def protocol_type(self):
        """Gets the protocol_type of this CreateFileSystemRequest.  # noqa: E501


        :return: The protocol_type of this CreateFileSystemRequest.  # noqa: E501
        :rtype: str
        """
        return self._protocol_type

    @protocol_type.setter
    def protocol_type(self, protocol_type):
        """Sets the protocol_type of this CreateFileSystemRequest.


        :param protocol_type: The protocol_type of this CreateFileSystemRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and protocol_type is None:
            raise ValueError("Invalid value for `protocol_type`, must not be `None`")  # noqa: E501
        allowed_values = ["NFS"]  # noqa: E501
        if (self._configuration.client_side_validation and
                protocol_type not in allowed_values):
            raise ValueError(
                "Invalid value for `protocol_type` ({0}), must be one of {1}"  # noqa: E501
                .format(protocol_type, allowed_values)
            )

        self._protocol_type = protocol_type

    @property
    def snapshot_id(self):
        """Gets the snapshot_id of this CreateFileSystemRequest.  # noqa: E501


        :return: The snapshot_id of this CreateFileSystemRequest.  # noqa: E501
        :rtype: str
        """
        return self._snapshot_id

    @snapshot_id.setter
    def snapshot_id(self, snapshot_id):
        """Sets the snapshot_id of this CreateFileSystemRequest.


        :param snapshot_id: The snapshot_id of this CreateFileSystemRequest.  # noqa: E501
        :type: str
        """

        self._snapshot_id = snapshot_id

    @property
    def storage_type(self):
        """Gets the storage_type of this CreateFileSystemRequest.  # noqa: E501


        :return: The storage_type of this CreateFileSystemRequest.  # noqa: E501
        :rtype: str
        """
        return self._storage_type

    @storage_type.setter
    def storage_type(self, storage_type):
        """Sets the storage_type of this CreateFileSystemRequest.


        :param storage_type: The storage_type of this CreateFileSystemRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["Standard"]  # noqa: E501
        if (self._configuration.client_side_validation and
                storage_type not in allowed_values):
            raise ValueError(
                "Invalid value for `storage_type` ({0}), must be one of {1}"  # noqa: E501
                .format(storage_type, allowed_values)
            )

        self._storage_type = storage_type

    @property
    def tags(self):
        """Gets the tags of this CreateFileSystemRequest.  # noqa: E501


        :return: The tags of this CreateFileSystemRequest.  # noqa: E501
        :rtype: list[TagForCreateFileSystemInput]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CreateFileSystemRequest.


        :param tags: The tags of this CreateFileSystemRequest.  # noqa: E501
        :type: list[TagForCreateFileSystemInput]
        """

        self._tags = tags

    @property
    def zone_id(self):
        """Gets the zone_id of this CreateFileSystemRequest.  # noqa: E501


        :return: The zone_id of this CreateFileSystemRequest.  # noqa: E501
        :rtype: str
        """
        return self._zone_id

    @zone_id.setter
    def zone_id(self, zone_id):
        """Sets the zone_id of this CreateFileSystemRequest.


        :param zone_id: The zone_id of this CreateFileSystemRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and zone_id is None:
            raise ValueError("Invalid value for `zone_id`, must not be `None`")  # noqa: E501

        self._zone_id = zone_id

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
        if issubclass(CreateFileSystemRequest, dict):
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
        if not isinstance(other, CreateFileSystemRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateFileSystemRequest):
            return True

        return self.to_dict() != other.to_dict()
