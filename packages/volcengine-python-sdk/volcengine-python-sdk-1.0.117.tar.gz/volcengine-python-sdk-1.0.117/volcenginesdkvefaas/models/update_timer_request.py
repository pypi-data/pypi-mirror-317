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


class UpdateTimerRequest(object):
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
        'crontab': 'str',
        'description': 'str',
        'enable_concurrency': 'bool',
        'enabled': 'bool',
        'function_id': 'str',
        'id': 'str',
        'payload': 'str',
        'retries': 'int',
        'top_param': 'TopParamForUpdateTimerInput'
    }

    attribute_map = {
        'crontab': 'Crontab',
        'description': 'Description',
        'enable_concurrency': 'EnableConcurrency',
        'enabled': 'Enabled',
        'function_id': 'FunctionId',
        'id': 'Id',
        'payload': 'Payload',
        'retries': 'Retries',
        'top_param': 'TopParam'
    }

    def __init__(self, crontab=None, description=None, enable_concurrency=None, enabled=None, function_id=None, id=None, payload=None, retries=None, top_param=None, _configuration=None):  # noqa: E501
        """UpdateTimerRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._crontab = None
        self._description = None
        self._enable_concurrency = None
        self._enabled = None
        self._function_id = None
        self._id = None
        self._payload = None
        self._retries = None
        self._top_param = None
        self.discriminator = None

        if crontab is not None:
            self.crontab = crontab
        if description is not None:
            self.description = description
        if enable_concurrency is not None:
            self.enable_concurrency = enable_concurrency
        if enabled is not None:
            self.enabled = enabled
        self.function_id = function_id
        self.id = id
        if payload is not None:
            self.payload = payload
        if retries is not None:
            self.retries = retries
        if top_param is not None:
            self.top_param = top_param

    @property
    def crontab(self):
        """Gets the crontab of this UpdateTimerRequest.  # noqa: E501


        :return: The crontab of this UpdateTimerRequest.  # noqa: E501
        :rtype: str
        """
        return self._crontab

    @crontab.setter
    def crontab(self, crontab):
        """Sets the crontab of this UpdateTimerRequest.


        :param crontab: The crontab of this UpdateTimerRequest.  # noqa: E501
        :type: str
        """

        self._crontab = crontab

    @property
    def description(self):
        """Gets the description of this UpdateTimerRequest.  # noqa: E501


        :return: The description of this UpdateTimerRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateTimerRequest.


        :param description: The description of this UpdateTimerRequest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def enable_concurrency(self):
        """Gets the enable_concurrency of this UpdateTimerRequest.  # noqa: E501


        :return: The enable_concurrency of this UpdateTimerRequest.  # noqa: E501
        :rtype: bool
        """
        return self._enable_concurrency

    @enable_concurrency.setter
    def enable_concurrency(self, enable_concurrency):
        """Sets the enable_concurrency of this UpdateTimerRequest.


        :param enable_concurrency: The enable_concurrency of this UpdateTimerRequest.  # noqa: E501
        :type: bool
        """

        self._enable_concurrency = enable_concurrency

    @property
    def enabled(self):
        """Gets the enabled of this UpdateTimerRequest.  # noqa: E501


        :return: The enabled of this UpdateTimerRequest.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this UpdateTimerRequest.


        :param enabled: The enabled of this UpdateTimerRequest.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def function_id(self):
        """Gets the function_id of this UpdateTimerRequest.  # noqa: E501


        :return: The function_id of this UpdateTimerRequest.  # noqa: E501
        :rtype: str
        """
        return self._function_id

    @function_id.setter
    def function_id(self, function_id):
        """Sets the function_id of this UpdateTimerRequest.


        :param function_id: The function_id of this UpdateTimerRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and function_id is None:
            raise ValueError("Invalid value for `function_id`, must not be `None`")  # noqa: E501

        self._function_id = function_id

    @property
    def id(self):
        """Gets the id of this UpdateTimerRequest.  # noqa: E501


        :return: The id of this UpdateTimerRequest.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UpdateTimerRequest.


        :param id: The id of this UpdateTimerRequest.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def payload(self):
        """Gets the payload of this UpdateTimerRequest.  # noqa: E501


        :return: The payload of this UpdateTimerRequest.  # noqa: E501
        :rtype: str
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """Sets the payload of this UpdateTimerRequest.


        :param payload: The payload of this UpdateTimerRequest.  # noqa: E501
        :type: str
        """

        self._payload = payload

    @property
    def retries(self):
        """Gets the retries of this UpdateTimerRequest.  # noqa: E501


        :return: The retries of this UpdateTimerRequest.  # noqa: E501
        :rtype: int
        """
        return self._retries

    @retries.setter
    def retries(self, retries):
        """Sets the retries of this UpdateTimerRequest.


        :param retries: The retries of this UpdateTimerRequest.  # noqa: E501
        :type: int
        """

        self._retries = retries

    @property
    def top_param(self):
        """Gets the top_param of this UpdateTimerRequest.  # noqa: E501


        :return: The top_param of this UpdateTimerRequest.  # noqa: E501
        :rtype: TopParamForUpdateTimerInput
        """
        return self._top_param

    @top_param.setter
    def top_param(self, top_param):
        """Sets the top_param of this UpdateTimerRequest.


        :param top_param: The top_param of this UpdateTimerRequest.  # noqa: E501
        :type: TopParamForUpdateTimerInput
        """

        self._top_param = top_param

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
        if issubclass(UpdateTimerRequest, dict):
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
        if not isinstance(other, UpdateTimerRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateTimerRequest):
            return True

        return self.to_dict() != other.to_dict()
