# coding: utf-8

"""
    cv20240606

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class HighAesGeneralV20LResponse(object):
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
        'code': 'int',
        'data': 'DataForHighAesGeneralV20LOutput',
        'message': 'str',
        'request_id': 'str',
        'status': 'int',
        'time_elapsed': 'str'
    }

    attribute_map = {
        'code': 'code',
        'data': 'data',
        'message': 'message',
        'request_id': 'request_id',
        'status': 'status',
        'time_elapsed': 'time_elapsed'
    }

    def __init__(self, code=None, data=None, message=None, request_id=None, status=None, time_elapsed=None, _configuration=None):  # noqa: E501
        """HighAesGeneralV20LResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._code = None
        self._data = None
        self._message = None
        self._request_id = None
        self._status = None
        self._time_elapsed = None
        self.discriminator = None

        if code is not None:
            self.code = code
        if data is not None:
            self.data = data
        if message is not None:
            self.message = message
        if request_id is not None:
            self.request_id = request_id
        if status is not None:
            self.status = status
        if time_elapsed is not None:
            self.time_elapsed = time_elapsed

    @property
    def code(self):
        """Gets the code of this HighAesGeneralV20LResponse.  # noqa: E501


        :return: The code of this HighAesGeneralV20LResponse.  # noqa: E501
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this HighAesGeneralV20LResponse.


        :param code: The code of this HighAesGeneralV20LResponse.  # noqa: E501
        :type: int
        """

        self._code = code

    @property
    def data(self):
        """Gets the data of this HighAesGeneralV20LResponse.  # noqa: E501


        :return: The data of this HighAesGeneralV20LResponse.  # noqa: E501
        :rtype: DataForHighAesGeneralV20LOutput
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this HighAesGeneralV20LResponse.


        :param data: The data of this HighAesGeneralV20LResponse.  # noqa: E501
        :type: DataForHighAesGeneralV20LOutput
        """

        self._data = data

    @property
    def message(self):
        """Gets the message of this HighAesGeneralV20LResponse.  # noqa: E501


        :return: The message of this HighAesGeneralV20LResponse.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this HighAesGeneralV20LResponse.


        :param message: The message of this HighAesGeneralV20LResponse.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def request_id(self):
        """Gets the request_id of this HighAesGeneralV20LResponse.  # noqa: E501


        :return: The request_id of this HighAesGeneralV20LResponse.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this HighAesGeneralV20LResponse.


        :param request_id: The request_id of this HighAesGeneralV20LResponse.  # noqa: E501
        :type: str
        """

        self._request_id = request_id

    @property
    def status(self):
        """Gets the status of this HighAesGeneralV20LResponse.  # noqa: E501


        :return: The status of this HighAesGeneralV20LResponse.  # noqa: E501
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this HighAesGeneralV20LResponse.


        :param status: The status of this HighAesGeneralV20LResponse.  # noqa: E501
        :type: int
        """

        self._status = status

    @property
    def time_elapsed(self):
        """Gets the time_elapsed of this HighAesGeneralV20LResponse.  # noqa: E501


        :return: The time_elapsed of this HighAesGeneralV20LResponse.  # noqa: E501
        :rtype: str
        """
        return self._time_elapsed

    @time_elapsed.setter
    def time_elapsed(self, time_elapsed):
        """Sets the time_elapsed of this HighAesGeneralV20LResponse.


        :param time_elapsed: The time_elapsed of this HighAesGeneralV20LResponse.  # noqa: E501
        :type: str
        """

        self._time_elapsed = time_elapsed

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
        if issubclass(HighAesGeneralV20LResponse, dict):
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
        if not isinstance(other, HighAesGeneralV20LResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, HighAesGeneralV20LResponse):
            return True

        return self.to_dict() != other.to_dict()
