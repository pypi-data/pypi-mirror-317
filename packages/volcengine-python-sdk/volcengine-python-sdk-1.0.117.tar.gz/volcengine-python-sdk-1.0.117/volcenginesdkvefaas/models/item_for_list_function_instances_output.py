# coding: utf-8

"""
    vefaas

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class ItemForListFunctionInstancesOutput(object):
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
        'availability_zone': 'str',
        'creation_time': 'str',
        'id': 'str',
        'instance_name': 'str',
        'instance_status': 'str',
        'instance_type': 'str',
        'revision_number': 'int',
        'user_vpc_ip': 'str',
        'user_vpc_ipv6': 'str'
    }

    attribute_map = {
        'availability_zone': 'AvailabilityZone',
        'creation_time': 'CreationTime',
        'id': 'Id',
        'instance_name': 'InstanceName',
        'instance_status': 'InstanceStatus',
        'instance_type': 'InstanceType',
        'revision_number': 'RevisionNumber',
        'user_vpc_ip': 'UserVpcIP',
        'user_vpc_ipv6': 'UserVpcIPv6'
    }

    def __init__(self, availability_zone=None, creation_time=None, id=None, instance_name=None, instance_status=None, instance_type=None, revision_number=None, user_vpc_ip=None, user_vpc_ipv6=None, _configuration=None):  # noqa: E501
        """ItemForListFunctionInstancesOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._availability_zone = None
        self._creation_time = None
        self._id = None
        self._instance_name = None
        self._instance_status = None
        self._instance_type = None
        self._revision_number = None
        self._user_vpc_ip = None
        self._user_vpc_ipv6 = None
        self.discriminator = None

        if availability_zone is not None:
            self.availability_zone = availability_zone
        if creation_time is not None:
            self.creation_time = creation_time
        if id is not None:
            self.id = id
        if instance_name is not None:
            self.instance_name = instance_name
        if instance_status is not None:
            self.instance_status = instance_status
        if instance_type is not None:
            self.instance_type = instance_type
        if revision_number is not None:
            self.revision_number = revision_number
        if user_vpc_ip is not None:
            self.user_vpc_ip = user_vpc_ip
        if user_vpc_ipv6 is not None:
            self.user_vpc_ipv6 = user_vpc_ipv6

    @property
    def availability_zone(self):
        """Gets the availability_zone of this ItemForListFunctionInstancesOutput.  # noqa: E501


        :return: The availability_zone of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._availability_zone

    @availability_zone.setter
    def availability_zone(self, availability_zone):
        """Sets the availability_zone of this ItemForListFunctionInstancesOutput.


        :param availability_zone: The availability_zone of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :type: str
        """

        self._availability_zone = availability_zone

    @property
    def creation_time(self):
        """Gets the creation_time of this ItemForListFunctionInstancesOutput.  # noqa: E501


        :return: The creation_time of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        """Sets the creation_time of this ItemForListFunctionInstancesOutput.


        :param creation_time: The creation_time of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :type: str
        """

        self._creation_time = creation_time

    @property
    def id(self):
        """Gets the id of this ItemForListFunctionInstancesOutput.  # noqa: E501


        :return: The id of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ItemForListFunctionInstancesOutput.


        :param id: The id of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def instance_name(self):
        """Gets the instance_name of this ItemForListFunctionInstancesOutput.  # noqa: E501


        :return: The instance_name of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._instance_name

    @instance_name.setter
    def instance_name(self, instance_name):
        """Sets the instance_name of this ItemForListFunctionInstancesOutput.


        :param instance_name: The instance_name of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :type: str
        """

        self._instance_name = instance_name

    @property
    def instance_status(self):
        """Gets the instance_status of this ItemForListFunctionInstancesOutput.  # noqa: E501


        :return: The instance_status of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._instance_status

    @instance_status.setter
    def instance_status(self, instance_status):
        """Sets the instance_status of this ItemForListFunctionInstancesOutput.


        :param instance_status: The instance_status of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :type: str
        """

        self._instance_status = instance_status

    @property
    def instance_type(self):
        """Gets the instance_type of this ItemForListFunctionInstancesOutput.  # noqa: E501


        :return: The instance_type of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._instance_type

    @instance_type.setter
    def instance_type(self, instance_type):
        """Sets the instance_type of this ItemForListFunctionInstancesOutput.


        :param instance_type: The instance_type of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :type: str
        """

        self._instance_type = instance_type

    @property
    def revision_number(self):
        """Gets the revision_number of this ItemForListFunctionInstancesOutput.  # noqa: E501


        :return: The revision_number of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :rtype: int
        """
        return self._revision_number

    @revision_number.setter
    def revision_number(self, revision_number):
        """Sets the revision_number of this ItemForListFunctionInstancesOutput.


        :param revision_number: The revision_number of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :type: int
        """

        self._revision_number = revision_number

    @property
    def user_vpc_ip(self):
        """Gets the user_vpc_ip of this ItemForListFunctionInstancesOutput.  # noqa: E501


        :return: The user_vpc_ip of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._user_vpc_ip

    @user_vpc_ip.setter
    def user_vpc_ip(self, user_vpc_ip):
        """Sets the user_vpc_ip of this ItemForListFunctionInstancesOutput.


        :param user_vpc_ip: The user_vpc_ip of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :type: str
        """

        self._user_vpc_ip = user_vpc_ip

    @property
    def user_vpc_ipv6(self):
        """Gets the user_vpc_ipv6 of this ItemForListFunctionInstancesOutput.  # noqa: E501


        :return: The user_vpc_ipv6 of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :rtype: str
        """
        return self._user_vpc_ipv6

    @user_vpc_ipv6.setter
    def user_vpc_ipv6(self, user_vpc_ipv6):
        """Sets the user_vpc_ipv6 of this ItemForListFunctionInstancesOutput.


        :param user_vpc_ipv6: The user_vpc_ipv6 of this ItemForListFunctionInstancesOutput.  # noqa: E501
        :type: str
        """

        self._user_vpc_ipv6 = user_vpc_ipv6

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
        if issubclass(ItemForListFunctionInstancesOutput, dict):
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
        if not isinstance(other, ItemForListFunctionInstancesOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ItemForListFunctionInstancesOutput):
            return True

        return self.to_dict() != other.to_dict()
