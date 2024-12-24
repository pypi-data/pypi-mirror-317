# coding: utf-8

"""
    vke

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ItemForListAddonsOutput(object):
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
        'config': 'str',
        'create_client_token': 'str',
        'create_time': 'str',
        'deploy_mode': 'str',
        'deploy_node_type': 'str',
        'name': 'str',
        'status': 'StatusForListAddonsOutput',
        'update_client_token': 'str',
        'update_time': 'str',
        'version': 'str'
    }

    attribute_map = {
        'cluster_id': 'ClusterId',
        'config': 'Config',
        'create_client_token': 'CreateClientToken',
        'create_time': 'CreateTime',
        'deploy_mode': 'DeployMode',
        'deploy_node_type': 'DeployNodeType',
        'name': 'Name',
        'status': 'Status',
        'update_client_token': 'UpdateClientToken',
        'update_time': 'UpdateTime',
        'version': 'Version'
    }

    def __init__(self, cluster_id=None, config=None, create_client_token=None, create_time=None, deploy_mode=None, deploy_node_type=None, name=None, status=None, update_client_token=None, update_time=None, version=None, _configuration=None):  # noqa: E501
        """ItemForListAddonsOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cluster_id = None
        self._config = None
        self._create_client_token = None
        self._create_time = None
        self._deploy_mode = None
        self._deploy_node_type = None
        self._name = None
        self._status = None
        self._update_client_token = None
        self._update_time = None
        self._version = None
        self.discriminator = None

        if cluster_id is not None:
            self.cluster_id = cluster_id
        if config is not None:
            self.config = config
        if create_client_token is not None:
            self.create_client_token = create_client_token
        if create_time is not None:
            self.create_time = create_time
        if deploy_mode is not None:
            self.deploy_mode = deploy_mode
        if deploy_node_type is not None:
            self.deploy_node_type = deploy_node_type
        if name is not None:
            self.name = name
        if status is not None:
            self.status = status
        if update_client_token is not None:
            self.update_client_token = update_client_token
        if update_time is not None:
            self.update_time = update_time
        if version is not None:
            self.version = version

    @property
    def cluster_id(self):
        """Gets the cluster_id of this ItemForListAddonsOutput.  # noqa: E501


        :return: The cluster_id of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """Sets the cluster_id of this ItemForListAddonsOutput.


        :param cluster_id: The cluster_id of this ItemForListAddonsOutput.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def config(self):
        """Gets the config of this ItemForListAddonsOutput.  # noqa: E501


        :return: The config of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: str
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this ItemForListAddonsOutput.


        :param config: The config of this ItemForListAddonsOutput.  # noqa: E501
        :type: str
        """

        self._config = config

    @property
    def create_client_token(self):
        """Gets the create_client_token of this ItemForListAddonsOutput.  # noqa: E501


        :return: The create_client_token of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: str
        """
        return self._create_client_token

    @create_client_token.setter
    def create_client_token(self, create_client_token):
        """Sets the create_client_token of this ItemForListAddonsOutput.


        :param create_client_token: The create_client_token of this ItemForListAddonsOutput.  # noqa: E501
        :type: str
        """

        self._create_client_token = create_client_token

    @property
    def create_time(self):
        """Gets the create_time of this ItemForListAddonsOutput.  # noqa: E501


        :return: The create_time of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: str
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this ItemForListAddonsOutput.


        :param create_time: The create_time of this ItemForListAddonsOutput.  # noqa: E501
        :type: str
        """

        self._create_time = create_time

    @property
    def deploy_mode(self):
        """Gets the deploy_mode of this ItemForListAddonsOutput.  # noqa: E501


        :return: The deploy_mode of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: str
        """
        return self._deploy_mode

    @deploy_mode.setter
    def deploy_mode(self, deploy_mode):
        """Sets the deploy_mode of this ItemForListAddonsOutput.


        :param deploy_mode: The deploy_mode of this ItemForListAddonsOutput.  # noqa: E501
        :type: str
        """

        self._deploy_mode = deploy_mode

    @property
    def deploy_node_type(self):
        """Gets the deploy_node_type of this ItemForListAddonsOutput.  # noqa: E501


        :return: The deploy_node_type of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: str
        """
        return self._deploy_node_type

    @deploy_node_type.setter
    def deploy_node_type(self, deploy_node_type):
        """Sets the deploy_node_type of this ItemForListAddonsOutput.


        :param deploy_node_type: The deploy_node_type of this ItemForListAddonsOutput.  # noqa: E501
        :type: str
        """

        self._deploy_node_type = deploy_node_type

    @property
    def name(self):
        """Gets the name of this ItemForListAddonsOutput.  # noqa: E501


        :return: The name of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ItemForListAddonsOutput.


        :param name: The name of this ItemForListAddonsOutput.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def status(self):
        """Gets the status of this ItemForListAddonsOutput.  # noqa: E501


        :return: The status of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: StatusForListAddonsOutput
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ItemForListAddonsOutput.


        :param status: The status of this ItemForListAddonsOutput.  # noqa: E501
        :type: StatusForListAddonsOutput
        """

        self._status = status

    @property
    def update_client_token(self):
        """Gets the update_client_token of this ItemForListAddonsOutput.  # noqa: E501


        :return: The update_client_token of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: str
        """
        return self._update_client_token

    @update_client_token.setter
    def update_client_token(self, update_client_token):
        """Sets the update_client_token of this ItemForListAddonsOutput.


        :param update_client_token: The update_client_token of this ItemForListAddonsOutput.  # noqa: E501
        :type: str
        """

        self._update_client_token = update_client_token

    @property
    def update_time(self):
        """Gets the update_time of this ItemForListAddonsOutput.  # noqa: E501


        :return: The update_time of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: str
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this ItemForListAddonsOutput.


        :param update_time: The update_time of this ItemForListAddonsOutput.  # noqa: E501
        :type: str
        """

        self._update_time = update_time

    @property
    def version(self):
        """Gets the version of this ItemForListAddonsOutput.  # noqa: E501


        :return: The version of this ItemForListAddonsOutput.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ItemForListAddonsOutput.


        :param version: The version of this ItemForListAddonsOutput.  # noqa: E501
        :type: str
        """

        self._version = version

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
        if issubclass(ItemForListAddonsOutput, dict):
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
        if not isinstance(other, ItemForListAddonsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ItemForListAddonsOutput):
            return True

        return self.to_dict() != other.to_dict()
