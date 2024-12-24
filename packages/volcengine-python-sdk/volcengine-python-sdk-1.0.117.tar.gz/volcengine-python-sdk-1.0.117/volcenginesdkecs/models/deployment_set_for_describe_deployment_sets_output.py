# coding: utf-8

"""
    ecs

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class DeploymentSetForDescribeDeploymentSetsOutput(object):
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
        'capacities': 'list[CapacityForDescribeDeploymentSetsOutput]',
        'created_at': 'str',
        'deployment_set_description': 'str',
        'deployment_set_id': 'str',
        'deployment_set_name': 'str',
        'granularity': 'str',
        'group_count': 'int',
        'instance_amount': 'int',
        'instance_ids': 'list[str]',
        'strategy': 'str'
    }

    attribute_map = {
        'capacities': 'Capacities',
        'created_at': 'CreatedAt',
        'deployment_set_description': 'DeploymentSetDescription',
        'deployment_set_id': 'DeploymentSetId',
        'deployment_set_name': 'DeploymentSetName',
        'granularity': 'Granularity',
        'group_count': 'GroupCount',
        'instance_amount': 'InstanceAmount',
        'instance_ids': 'InstanceIds',
        'strategy': 'Strategy'
    }

    def __init__(self, capacities=None, created_at=None, deployment_set_description=None, deployment_set_id=None, deployment_set_name=None, granularity=None, group_count=None, instance_amount=None, instance_ids=None, strategy=None, _configuration=None):  # noqa: E501
        """DeploymentSetForDescribeDeploymentSetsOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._capacities = None
        self._created_at = None
        self._deployment_set_description = None
        self._deployment_set_id = None
        self._deployment_set_name = None
        self._granularity = None
        self._group_count = None
        self._instance_amount = None
        self._instance_ids = None
        self._strategy = None
        self.discriminator = None

        if capacities is not None:
            self.capacities = capacities
        if created_at is not None:
            self.created_at = created_at
        if deployment_set_description is not None:
            self.deployment_set_description = deployment_set_description
        if deployment_set_id is not None:
            self.deployment_set_id = deployment_set_id
        if deployment_set_name is not None:
            self.deployment_set_name = deployment_set_name
        if granularity is not None:
            self.granularity = granularity
        if group_count is not None:
            self.group_count = group_count
        if instance_amount is not None:
            self.instance_amount = instance_amount
        if instance_ids is not None:
            self.instance_ids = instance_ids
        if strategy is not None:
            self.strategy = strategy

    @property
    def capacities(self):
        """Gets the capacities of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501


        :return: The capacities of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :rtype: list[CapacityForDescribeDeploymentSetsOutput]
        """
        return self._capacities

    @capacities.setter
    def capacities(self, capacities):
        """Sets the capacities of this DeploymentSetForDescribeDeploymentSetsOutput.


        :param capacities: The capacities of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :type: list[CapacityForDescribeDeploymentSetsOutput]
        """

        self._capacities = capacities

    @property
    def created_at(self):
        """Gets the created_at of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501


        :return: The created_at of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this DeploymentSetForDescribeDeploymentSetsOutput.


        :param created_at: The created_at of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def deployment_set_description(self):
        """Gets the deployment_set_description of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501


        :return: The deployment_set_description of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :rtype: str
        """
        return self._deployment_set_description

    @deployment_set_description.setter
    def deployment_set_description(self, deployment_set_description):
        """Sets the deployment_set_description of this DeploymentSetForDescribeDeploymentSetsOutput.


        :param deployment_set_description: The deployment_set_description of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :type: str
        """

        self._deployment_set_description = deployment_set_description

    @property
    def deployment_set_id(self):
        """Gets the deployment_set_id of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501


        :return: The deployment_set_id of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :rtype: str
        """
        return self._deployment_set_id

    @deployment_set_id.setter
    def deployment_set_id(self, deployment_set_id):
        """Sets the deployment_set_id of this DeploymentSetForDescribeDeploymentSetsOutput.


        :param deployment_set_id: The deployment_set_id of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :type: str
        """

        self._deployment_set_id = deployment_set_id

    @property
    def deployment_set_name(self):
        """Gets the deployment_set_name of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501


        :return: The deployment_set_name of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :rtype: str
        """
        return self._deployment_set_name

    @deployment_set_name.setter
    def deployment_set_name(self, deployment_set_name):
        """Sets the deployment_set_name of this DeploymentSetForDescribeDeploymentSetsOutput.


        :param deployment_set_name: The deployment_set_name of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :type: str
        """

        self._deployment_set_name = deployment_set_name

    @property
    def granularity(self):
        """Gets the granularity of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501


        :return: The granularity of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :rtype: str
        """
        return self._granularity

    @granularity.setter
    def granularity(self, granularity):
        """Sets the granularity of this DeploymentSetForDescribeDeploymentSetsOutput.


        :param granularity: The granularity of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :type: str
        """

        self._granularity = granularity

    @property
    def group_count(self):
        """Gets the group_count of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501


        :return: The group_count of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :rtype: int
        """
        return self._group_count

    @group_count.setter
    def group_count(self, group_count):
        """Sets the group_count of this DeploymentSetForDescribeDeploymentSetsOutput.


        :param group_count: The group_count of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :type: int
        """

        self._group_count = group_count

    @property
    def instance_amount(self):
        """Gets the instance_amount of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501


        :return: The instance_amount of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :rtype: int
        """
        return self._instance_amount

    @instance_amount.setter
    def instance_amount(self, instance_amount):
        """Sets the instance_amount of this DeploymentSetForDescribeDeploymentSetsOutput.


        :param instance_amount: The instance_amount of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :type: int
        """

        self._instance_amount = instance_amount

    @property
    def instance_ids(self):
        """Gets the instance_ids of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501


        :return: The instance_ids of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :rtype: list[str]
        """
        return self._instance_ids

    @instance_ids.setter
    def instance_ids(self, instance_ids):
        """Sets the instance_ids of this DeploymentSetForDescribeDeploymentSetsOutput.


        :param instance_ids: The instance_ids of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :type: list[str]
        """

        self._instance_ids = instance_ids

    @property
    def strategy(self):
        """Gets the strategy of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501


        :return: The strategy of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :rtype: str
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        """Sets the strategy of this DeploymentSetForDescribeDeploymentSetsOutput.


        :param strategy: The strategy of this DeploymentSetForDescribeDeploymentSetsOutput.  # noqa: E501
        :type: str
        """

        self._strategy = strategy

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
        if issubclass(DeploymentSetForDescribeDeploymentSetsOutput, dict):
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
        if not isinstance(other, DeploymentSetForDescribeDeploymentSetsOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeploymentSetForDescribeDeploymentSetsOutput):
            return True

        return self.to_dict() != other.to_dict()
