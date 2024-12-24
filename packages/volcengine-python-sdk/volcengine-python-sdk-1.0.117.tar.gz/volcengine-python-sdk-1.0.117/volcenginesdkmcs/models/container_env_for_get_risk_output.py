# coding: utf-8

"""
    mcs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ContainerEnvForGetRiskOutput(object):
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
        'cluster_id': 'str',
        'cluster_name': 'str',
        'container_group_id': 'str',
        'container_group_name': 'str',
        'container_id': 'str',
        'container_name': 'str',
        'node_id': 'str',
        'node_name': 'str',
        'node_pool_id': 'str',
        'node_pool_name': 'str'
    }

    attribute_map = {
        'cluster_id': 'ClusterID',
        'cluster_name': 'ClusterName',
        'container_group_id': 'ContainerGroupID',
        'container_group_name': 'ContainerGroupName',
        'container_id': 'ContainerID',
        'container_name': 'ContainerName',
        'node_id': 'NodeID',
        'node_name': 'NodeName',
        'node_pool_id': 'NodePoolID',
        'node_pool_name': 'NodePoolName'
    }

    def __init__(self, cluster_id=None, cluster_name=None, container_group_id=None, container_group_name=None, container_id=None, container_name=None, node_id=None, node_name=None, node_pool_id=None, node_pool_name=None, _configuration=None):  # noqa: E501
        """ContainerEnvForGetRiskOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cluster_id = None
        self._cluster_name = None
        self._container_group_id = None
        self._container_group_name = None
        self._container_id = None
        self._container_name = None
        self._node_id = None
        self._node_name = None
        self._node_pool_id = None
        self._node_pool_name = None
        self.discriminator = None

        if cluster_id is not None:
            self.cluster_id = cluster_id
        if cluster_name is not None:
            self.cluster_name = cluster_name
        if container_group_id is not None:
            self.container_group_id = container_group_id
        if container_group_name is not None:
            self.container_group_name = container_group_name
        if container_id is not None:
            self.container_id = container_id
        if container_name is not None:
            self.container_name = container_name
        if node_id is not None:
            self.node_id = node_id
        if node_name is not None:
            self.node_name = node_name
        if node_pool_id is not None:
            self.node_pool_id = node_pool_id
        if node_pool_name is not None:
            self.node_pool_name = node_pool_name

    @property
    def cluster_id(self):
        """Gets the cluster_id of this ContainerEnvForGetRiskOutput.  # noqa: E501


        :return: The cluster_id of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """Sets the cluster_id of this ContainerEnvForGetRiskOutput.


        :param cluster_id: The cluster_id of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def cluster_name(self):
        """Gets the cluster_name of this ContainerEnvForGetRiskOutput.  # noqa: E501


        :return: The cluster_name of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._cluster_name

    @cluster_name.setter
    def cluster_name(self, cluster_name):
        """Sets the cluster_name of this ContainerEnvForGetRiskOutput.


        :param cluster_name: The cluster_name of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._cluster_name = cluster_name

    @property
    def container_group_id(self):
        """Gets the container_group_id of this ContainerEnvForGetRiskOutput.  # noqa: E501


        :return: The container_group_id of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._container_group_id

    @container_group_id.setter
    def container_group_id(self, container_group_id):
        """Sets the container_group_id of this ContainerEnvForGetRiskOutput.


        :param container_group_id: The container_group_id of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._container_group_id = container_group_id

    @property
    def container_group_name(self):
        """Gets the container_group_name of this ContainerEnvForGetRiskOutput.  # noqa: E501


        :return: The container_group_name of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._container_group_name

    @container_group_name.setter
    def container_group_name(self, container_group_name):
        """Sets the container_group_name of this ContainerEnvForGetRiskOutput.


        :param container_group_name: The container_group_name of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._container_group_name = container_group_name

    @property
    def container_id(self):
        """Gets the container_id of this ContainerEnvForGetRiskOutput.  # noqa: E501


        :return: The container_id of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._container_id

    @container_id.setter
    def container_id(self, container_id):
        """Sets the container_id of this ContainerEnvForGetRiskOutput.


        :param container_id: The container_id of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._container_id = container_id

    @property
    def container_name(self):
        """Gets the container_name of this ContainerEnvForGetRiskOutput.  # noqa: E501


        :return: The container_name of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._container_name

    @container_name.setter
    def container_name(self, container_name):
        """Sets the container_name of this ContainerEnvForGetRiskOutput.


        :param container_name: The container_name of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._container_name = container_name

    @property
    def node_id(self):
        """Gets the node_id of this ContainerEnvForGetRiskOutput.  # noqa: E501


        :return: The node_id of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id):
        """Sets the node_id of this ContainerEnvForGetRiskOutput.


        :param node_id: The node_id of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._node_id = node_id

    @property
    def node_name(self):
        """Gets the node_name of this ContainerEnvForGetRiskOutput.  # noqa: E501


        :return: The node_name of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._node_name

    @node_name.setter
    def node_name(self, node_name):
        """Sets the node_name of this ContainerEnvForGetRiskOutput.


        :param node_name: The node_name of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._node_name = node_name

    @property
    def node_pool_id(self):
        """Gets the node_pool_id of this ContainerEnvForGetRiskOutput.  # noqa: E501


        :return: The node_pool_id of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._node_pool_id

    @node_pool_id.setter
    def node_pool_id(self, node_pool_id):
        """Sets the node_pool_id of this ContainerEnvForGetRiskOutput.


        :param node_pool_id: The node_pool_id of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._node_pool_id = node_pool_id

    @property
    def node_pool_name(self):
        """Gets the node_pool_name of this ContainerEnvForGetRiskOutput.  # noqa: E501


        :return: The node_pool_name of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._node_pool_name

    @node_pool_name.setter
    def node_pool_name(self, node_pool_name):
        """Sets the node_pool_name of this ContainerEnvForGetRiskOutput.


        :param node_pool_name: The node_pool_name of this ContainerEnvForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._node_pool_name = node_pool_name

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
        if issubclass(ContainerEnvForGetRiskOutput, dict):
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
        if not isinstance(other, ContainerEnvForGetRiskOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ContainerEnvForGetRiskOutput):
            return True

        return self.to_dict() != other.to_dict()
