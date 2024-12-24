# coding: utf-8

"""
    rocketmq

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class CreateTopicRequest(object):
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
        'access_policies': 'list[AccessPolicyForCreateTopicInput]',
        'description': 'str',
        'instance_id': 'str',
        'message_type': 'int',
        'queue_number': 'int',
        'topic_name': 'str'
    }

    attribute_map = {
        'access_policies': 'AccessPolicies',
        'description': 'Description',
        'instance_id': 'InstanceId',
        'message_type': 'MessageType',
        'queue_number': 'QueueNumber',
        'topic_name': 'TopicName'
    }

    def __init__(self, access_policies=None, description=None, instance_id=None, message_type=None, queue_number=None, topic_name=None, _configuration=None):  # noqa: E501
        """CreateTopicRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._access_policies = None
        self._description = None
        self._instance_id = None
        self._message_type = None
        self._queue_number = None
        self._topic_name = None
        self.discriminator = None

        if access_policies is not None:
            self.access_policies = access_policies
        if description is not None:
            self.description = description
        self.instance_id = instance_id
        self.message_type = message_type
        self.queue_number = queue_number
        self.topic_name = topic_name

    @property
    def access_policies(self):
        """Gets the access_policies of this CreateTopicRequest.  # noqa: E501


        :return: The access_policies of this CreateTopicRequest.  # noqa: E501
        :rtype: list[AccessPolicyForCreateTopicInput]
        """
        return self._access_policies

    @access_policies.setter
    def access_policies(self, access_policies):
        """Sets the access_policies of this CreateTopicRequest.


        :param access_policies: The access_policies of this CreateTopicRequest.  # noqa: E501
        :type: list[AccessPolicyForCreateTopicInput]
        """

        self._access_policies = access_policies

    @property
    def description(self):
        """Gets the description of this CreateTopicRequest.  # noqa: E501


        :return: The description of this CreateTopicRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateTopicRequest.


        :param description: The description of this CreateTopicRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def instance_id(self):
        """Gets the instance_id of this CreateTopicRequest.  # noqa: E501


        :return: The instance_id of this CreateTopicRequest.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this CreateTopicRequest.


        :param instance_id: The instance_id of this CreateTopicRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and instance_id is None:
            raise ValueError("Invalid value for `instance_id`, must not be `None`")  # noqa: E501

        self._instance_id = instance_id

    @property
    def message_type(self):
        """Gets the message_type of this CreateTopicRequest.  # noqa: E501


        :return: The message_type of this CreateTopicRequest.  # noqa: E501
        :rtype: int
        """
        return self._message_type

    @message_type.setter
    def message_type(self, message_type):
        """Sets the message_type of this CreateTopicRequest.


        :param message_type: The message_type of this CreateTopicRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and message_type is None:
            raise ValueError("Invalid value for `message_type`, must not be `None`")  # noqa: E501
        if (self._configuration.client_side_validation and
                message_type is not None and message_type > 4):  # noqa: E501
            raise ValueError("Invalid value for `message_type`, must be a value less than or equal to `4`")  # noqa: E501
        if (self._configuration.client_side_validation and
                message_type is not None and message_type < 0):  # noqa: E501
            raise ValueError("Invalid value for `message_type`, must be a value greater than or equal to `0`")  # noqa: E501

        self._message_type = message_type

    @property
    def queue_number(self):
        """Gets the queue_number of this CreateTopicRequest.  # noqa: E501


        :return: The queue_number of this CreateTopicRequest.  # noqa: E501
        :rtype: int
        """
        return self._queue_number

    @queue_number.setter
    def queue_number(self, queue_number):
        """Sets the queue_number of this CreateTopicRequest.


        :param queue_number: The queue_number of this CreateTopicRequest.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and queue_number is None:
            raise ValueError("Invalid value for `queue_number`, must not be `None`")  # noqa: E501
        if (self._configuration.client_side_validation and
                queue_number is not None and queue_number > 120):  # noqa: E501
            raise ValueError("Invalid value for `queue_number`, must be a value less than or equal to `120`")  # noqa: E501
        if (self._configuration.client_side_validation and
                queue_number is not None and queue_number < 1):  # noqa: E501
            raise ValueError("Invalid value for `queue_number`, must be a value greater than or equal to `1`")  # noqa: E501

        self._queue_number = queue_number

    @property
    def topic_name(self):
        """Gets the topic_name of this CreateTopicRequest.  # noqa: E501


        :return: The topic_name of this CreateTopicRequest.  # noqa: E501
        :rtype: str
        """
        return self._topic_name

    @topic_name.setter
    def topic_name(self, topic_name):
        """Sets the topic_name of this CreateTopicRequest.


        :param topic_name: The topic_name of this CreateTopicRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and topic_name is None:
            raise ValueError("Invalid value for `topic_name`, must not be `None`")  # noqa: E501
        if (self._configuration.client_side_validation and
                topic_name is not None and len(topic_name) > 128):
            raise ValueError("Invalid value for `topic_name`, length must be less than or equal to `128`")  # noqa: E501

        self._topic_name = topic_name

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
        if issubclass(CreateTopicRequest, dict):
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
        if not isinstance(other, CreateTopicRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateTopicRequest):
            return True

        return self.to_dict() != other.to_dict()
