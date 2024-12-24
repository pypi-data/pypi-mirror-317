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


class FilterForListClustersInput(object):
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
        'create_client_token': 'str',
        'delete_protection_enabled': 'bool',
        'ids': 'list[str]',
        'name': 'str',
        'pods_config_pod_network_mode': 'str',
        'statuses': 'list[StatusForListClustersInput]',
        'update_client_token': 'str'
    }

    attribute_map = {
        'create_client_token': 'CreateClientToken',
        'delete_protection_enabled': 'DeleteProtectionEnabled',
        'ids': 'Ids',
        'name': 'Name',
        'pods_config_pod_network_mode': 'PodsConfig.PodNetworkMode',
        'statuses': 'Statuses',
        'update_client_token': 'UpdateClientToken'
    }

    def __init__(self, create_client_token=None, delete_protection_enabled=None, ids=None, name=None, pods_config_pod_network_mode=None, statuses=None, update_client_token=None, _configuration=None):  # noqa: E501
        """FilterForListClustersInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._create_client_token = None
        self._delete_protection_enabled = None
        self._ids = None
        self._name = None
        self._pods_config_pod_network_mode = None
        self._statuses = None
        self._update_client_token = None
        self.discriminator = None

        if create_client_token is not None:
            self.create_client_token = create_client_token
        if delete_protection_enabled is not None:
            self.delete_protection_enabled = delete_protection_enabled
        if ids is not None:
            self.ids = ids
        if name is not None:
            self.name = name
        if pods_config_pod_network_mode is not None:
            self.pods_config_pod_network_mode = pods_config_pod_network_mode
        if statuses is not None:
            self.statuses = statuses
        if update_client_token is not None:
            self.update_client_token = update_client_token

    @property
    def create_client_token(self):
        """Gets the create_client_token of this FilterForListClustersInput.  # noqa: E501


        :return: The create_client_token of this FilterForListClustersInput.  # noqa: E501
        :rtype: str
        """
        return self._create_client_token

    @create_client_token.setter
    def create_client_token(self, create_client_token):
        """Sets the create_client_token of this FilterForListClustersInput.


        :param create_client_token: The create_client_token of this FilterForListClustersInput.  # noqa: E501
        :type: str
        """

        self._create_client_token = create_client_token

    @property
    def delete_protection_enabled(self):
        """Gets the delete_protection_enabled of this FilterForListClustersInput.  # noqa: E501


        :return: The delete_protection_enabled of this FilterForListClustersInput.  # noqa: E501
        :rtype: bool
        """
        return self._delete_protection_enabled

    @delete_protection_enabled.setter
    def delete_protection_enabled(self, delete_protection_enabled):
        """Sets the delete_protection_enabled of this FilterForListClustersInput.


        :param delete_protection_enabled: The delete_protection_enabled of this FilterForListClustersInput.  # noqa: E501
        :type: bool
        """

        self._delete_protection_enabled = delete_protection_enabled

    @property
    def ids(self):
        """Gets the ids of this FilterForListClustersInput.  # noqa: E501


        :return: The ids of this FilterForListClustersInput.  # noqa: E501
        :rtype: list[str]
        """
        return self._ids

    @ids.setter
    def ids(self, ids):
        """Sets the ids of this FilterForListClustersInput.


        :param ids: The ids of this FilterForListClustersInput.  # noqa: E501
        :type: list[str]
        """

        self._ids = ids

    @property
    def name(self):
        """Gets the name of this FilterForListClustersInput.  # noqa: E501


        :return: The name of this FilterForListClustersInput.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this FilterForListClustersInput.


        :param name: The name of this FilterForListClustersInput.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def pods_config_pod_network_mode(self):
        """Gets the pods_config_pod_network_mode of this FilterForListClustersInput.  # noqa: E501


        :return: The pods_config_pod_network_mode of this FilterForListClustersInput.  # noqa: E501
        :rtype: str
        """
        return self._pods_config_pod_network_mode

    @pods_config_pod_network_mode.setter
    def pods_config_pod_network_mode(self, pods_config_pod_network_mode):
        """Sets the pods_config_pod_network_mode of this FilterForListClustersInput.


        :param pods_config_pod_network_mode: The pods_config_pod_network_mode of this FilterForListClustersInput.  # noqa: E501
        :type: str
        """
        allowed_values = ["Flannel", "VpcCniShared", "CalicoBgp", "CalicoVxlan", "VpcCniDedicated"]  # noqa: E501
        if (self._configuration.client_side_validation and
                pods_config_pod_network_mode not in allowed_values):
            raise ValueError(
                "Invalid value for `pods_config_pod_network_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(pods_config_pod_network_mode, allowed_values)
            )

        self._pods_config_pod_network_mode = pods_config_pod_network_mode

    @property
    def statuses(self):
        """Gets the statuses of this FilterForListClustersInput.  # noqa: E501


        :return: The statuses of this FilterForListClustersInput.  # noqa: E501
        :rtype: list[StatusForListClustersInput]
        """
        return self._statuses

    @statuses.setter
    def statuses(self, statuses):
        """Sets the statuses of this FilterForListClustersInput.


        :param statuses: The statuses of this FilterForListClustersInput.  # noqa: E501
        :type: list[StatusForListClustersInput]
        """

        self._statuses = statuses

    @property
    def update_client_token(self):
        """Gets the update_client_token of this FilterForListClustersInput.  # noqa: E501


        :return: The update_client_token of this FilterForListClustersInput.  # noqa: E501
        :rtype: str
        """
        return self._update_client_token

    @update_client_token.setter
    def update_client_token(self, update_client_token):
        """Sets the update_client_token of this FilterForListClustersInput.


        :param update_client_token: The update_client_token of this FilterForListClustersInput.  # noqa: E501
        :type: str
        """

        self._update_client_token = update_client_token

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
        if issubclass(FilterForListClustersInput, dict):
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
        if not isinstance(other, FilterForListClustersInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FilterForListClustersInput):
            return True

        return self.to_dict() != other.to_dict()
