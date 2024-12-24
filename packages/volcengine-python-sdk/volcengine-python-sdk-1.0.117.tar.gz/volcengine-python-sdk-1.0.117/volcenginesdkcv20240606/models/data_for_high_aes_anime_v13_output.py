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


class DataForHighAesAnimeV13Output(object):
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
        'algorithm_base_resp': 'AlgorithmBaseRespForHighAesAnimeV13Output',
        'binary_data_base64': 'list[str]',
        'image_urls': 'list[str]',
        'resp_data': 'str',
        'response_data': 'str',
        'status': 'str',
        'task_id': 'str'
    }

    attribute_map = {
        'algorithm_base_resp': 'algorithm_base_resp',
        'binary_data_base64': 'binary_data_base64',
        'image_urls': 'image_urls',
        'resp_data': 'resp_data',
        'response_data': 'response_data',
        'status': 'status',
        'task_id': 'task_id'
    }

    def __init__(self, algorithm_base_resp=None, binary_data_base64=None, image_urls=None, resp_data=None, response_data=None, status=None, task_id=None, _configuration=None):  # noqa: E501
        """DataForHighAesAnimeV13Output - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._algorithm_base_resp = None
        self._binary_data_base64 = None
        self._image_urls = None
        self._resp_data = None
        self._response_data = None
        self._status = None
        self._task_id = None
        self.discriminator = None

        if algorithm_base_resp is not None:
            self.algorithm_base_resp = algorithm_base_resp
        if binary_data_base64 is not None:
            self.binary_data_base64 = binary_data_base64
        if image_urls is not None:
            self.image_urls = image_urls
        if resp_data is not None:
            self.resp_data = resp_data
        if response_data is not None:
            self.response_data = response_data
        if status is not None:
            self.status = status
        if task_id is not None:
            self.task_id = task_id

    @property
    def algorithm_base_resp(self):
        """Gets the algorithm_base_resp of this DataForHighAesAnimeV13Output.  # noqa: E501


        :return: The algorithm_base_resp of this DataForHighAesAnimeV13Output.  # noqa: E501
        :rtype: AlgorithmBaseRespForHighAesAnimeV13Output
        """
        return self._algorithm_base_resp

    @algorithm_base_resp.setter
    def algorithm_base_resp(self, algorithm_base_resp):
        """Sets the algorithm_base_resp of this DataForHighAesAnimeV13Output.


        :param algorithm_base_resp: The algorithm_base_resp of this DataForHighAesAnimeV13Output.  # noqa: E501
        :type: AlgorithmBaseRespForHighAesAnimeV13Output
        """

        self._algorithm_base_resp = algorithm_base_resp

    @property
    def binary_data_base64(self):
        """Gets the binary_data_base64 of this DataForHighAesAnimeV13Output.  # noqa: E501


        :return: The binary_data_base64 of this DataForHighAesAnimeV13Output.  # noqa: E501
        :rtype: list[str]
        """
        return self._binary_data_base64

    @binary_data_base64.setter
    def binary_data_base64(self, binary_data_base64):
        """Sets the binary_data_base64 of this DataForHighAesAnimeV13Output.


        :param binary_data_base64: The binary_data_base64 of this DataForHighAesAnimeV13Output.  # noqa: E501
        :type: list[str]
        """

        self._binary_data_base64 = binary_data_base64

    @property
    def image_urls(self):
        """Gets the image_urls of this DataForHighAesAnimeV13Output.  # noqa: E501


        :return: The image_urls of this DataForHighAesAnimeV13Output.  # noqa: E501
        :rtype: list[str]
        """
        return self._image_urls

    @image_urls.setter
    def image_urls(self, image_urls):
        """Sets the image_urls of this DataForHighAesAnimeV13Output.


        :param image_urls: The image_urls of this DataForHighAesAnimeV13Output.  # noqa: E501
        :type: list[str]
        """

        self._image_urls = image_urls

    @property
    def resp_data(self):
        """Gets the resp_data of this DataForHighAesAnimeV13Output.  # noqa: E501


        :return: The resp_data of this DataForHighAesAnimeV13Output.  # noqa: E501
        :rtype: str
        """
        return self._resp_data

    @resp_data.setter
    def resp_data(self, resp_data):
        """Sets the resp_data of this DataForHighAesAnimeV13Output.


        :param resp_data: The resp_data of this DataForHighAesAnimeV13Output.  # noqa: E501
        :type: str
        """

        self._resp_data = resp_data

    @property
    def response_data(self):
        """Gets the response_data of this DataForHighAesAnimeV13Output.  # noqa: E501


        :return: The response_data of this DataForHighAesAnimeV13Output.  # noqa: E501
        :rtype: str
        """
        return self._response_data

    @response_data.setter
    def response_data(self, response_data):
        """Sets the response_data of this DataForHighAesAnimeV13Output.


        :param response_data: The response_data of this DataForHighAesAnimeV13Output.  # noqa: E501
        :type: str
        """

        self._response_data = response_data

    @property
    def status(self):
        """Gets the status of this DataForHighAesAnimeV13Output.  # noqa: E501


        :return: The status of this DataForHighAesAnimeV13Output.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DataForHighAesAnimeV13Output.


        :param status: The status of this DataForHighAesAnimeV13Output.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def task_id(self):
        """Gets the task_id of this DataForHighAesAnimeV13Output.  # noqa: E501


        :return: The task_id of this DataForHighAesAnimeV13Output.  # noqa: E501
        :rtype: str
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this DataForHighAesAnimeV13Output.


        :param task_id: The task_id of this DataForHighAesAnimeV13Output.  # noqa: E501
        :type: str
        """

        self._task_id = task_id

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
        if issubclass(DataForHighAesAnimeV13Output, dict):
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
        if not isinstance(other, DataForHighAesAnimeV13Output):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DataForHighAesAnimeV13Output):
            return True

        return self.to_dict() != other.to_dict()
