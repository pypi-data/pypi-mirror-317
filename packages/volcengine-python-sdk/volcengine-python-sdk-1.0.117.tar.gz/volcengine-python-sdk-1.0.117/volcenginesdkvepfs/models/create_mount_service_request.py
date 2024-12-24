# coding: utf-8

"""
    vepfs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class CreateMountServiceRequest(object):
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
        'mount_service_name': 'str',
        'node_type': 'str',
        'project': 'str',
        'subnet_id': 'str',
        'vpc_id': 'str',
        'zone_id': 'str'
    }

    attribute_map = {
        'mount_service_name': 'MountServiceName',
        'node_type': 'NodeType',
        'project': 'Project',
        'subnet_id': 'SubnetId',
        'vpc_id': 'VpcId',
        'zone_id': 'ZoneId'
    }

    def __init__(self, mount_service_name=None, node_type=None, project=None, subnet_id=None, vpc_id=None, zone_id=None, _configuration=None):  # noqa: E501
        """CreateMountServiceRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._mount_service_name = None
        self._node_type = None
        self._project = None
        self._subnet_id = None
        self._vpc_id = None
        self._zone_id = None
        self.discriminator = None

        if mount_service_name is not None:
            self.mount_service_name = mount_service_name
        if node_type is not None:
            self.node_type = node_type
        if project is not None:
            self.project = project
        if subnet_id is not None:
            self.subnet_id = subnet_id
        if vpc_id is not None:
            self.vpc_id = vpc_id
        if zone_id is not None:
            self.zone_id = zone_id

    @property
    def mount_service_name(self):
        """Gets the mount_service_name of this CreateMountServiceRequest.  # noqa: E501


        :return: The mount_service_name of this CreateMountServiceRequest.  # noqa: E501
        :rtype: str
        """
        return self._mount_service_name

    @mount_service_name.setter
    def mount_service_name(self, mount_service_name):
        """Sets the mount_service_name of this CreateMountServiceRequest.


        :param mount_service_name: The mount_service_name of this CreateMountServiceRequest.  # noqa: E501
        :type: str
        """

        self._mount_service_name = mount_service_name

    @property
    def node_type(self):
        """Gets the node_type of this CreateMountServiceRequest.  # noqa: E501


        :return: The node_type of this CreateMountServiceRequest.  # noqa: E501
        :rtype: str
        """
        return self._node_type

    @node_type.setter
    def node_type(self, node_type):
        """Sets the node_type of this CreateMountServiceRequest.


        :param node_type: The node_type of this CreateMountServiceRequest.  # noqa: E501
        :type: str
        """

        self._node_type = node_type

    @property
    def project(self):
        """Gets the project of this CreateMountServiceRequest.  # noqa: E501


        :return: The project of this CreateMountServiceRequest.  # noqa: E501
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this CreateMountServiceRequest.


        :param project: The project of this CreateMountServiceRequest.  # noqa: E501
        :type: str
        """

        self._project = project

    @property
    def subnet_id(self):
        """Gets the subnet_id of this CreateMountServiceRequest.  # noqa: E501


        :return: The subnet_id of this CreateMountServiceRequest.  # noqa: E501
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """Sets the subnet_id of this CreateMountServiceRequest.


        :param subnet_id: The subnet_id of this CreateMountServiceRequest.  # noqa: E501
        :type: str
        """

        self._subnet_id = subnet_id

    @property
    def vpc_id(self):
        """Gets the vpc_id of this CreateMountServiceRequest.  # noqa: E501


        :return: The vpc_id of this CreateMountServiceRequest.  # noqa: E501
        :rtype: str
        """
        return self._vpc_id

    @vpc_id.setter
    def vpc_id(self, vpc_id):
        """Sets the vpc_id of this CreateMountServiceRequest.


        :param vpc_id: The vpc_id of this CreateMountServiceRequest.  # noqa: E501
        :type: str
        """

        self._vpc_id = vpc_id

    @property
    def zone_id(self):
        """Gets the zone_id of this CreateMountServiceRequest.  # noqa: E501


        :return: The zone_id of this CreateMountServiceRequest.  # noqa: E501
        :rtype: str
        """
        return self._zone_id

    @zone_id.setter
    def zone_id(self, zone_id):
        """Sets the zone_id of this CreateMountServiceRequest.


        :param zone_id: The zone_id of this CreateMountServiceRequest.  # noqa: E501
        :type: str
        """

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
        if issubclass(CreateMountServiceRequest, dict):
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
        if not isinstance(other, CreateMountServiceRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateMountServiceRequest):
            return True

        return self.to_dict() != other.to_dict()
