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


class DetectionResultsForDescribeImagesOutput(object):
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
        'detection_status': 'str',
        'items': 'list[ItemForDescribeImagesOutput]'
    }

    attribute_map = {
        'detection_status': 'DetectionStatus',
        'items': 'Items'
    }

    def __init__(self, detection_status=None, items=None, _configuration=None):  # noqa: E501
        """DetectionResultsForDescribeImagesOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._detection_status = None
        self._items = None
        self.discriminator = None

        if detection_status is not None:
            self.detection_status = detection_status
        if items is not None:
            self.items = items

    @property
    def detection_status(self):
        """Gets the detection_status of this DetectionResultsForDescribeImagesOutput.  # noqa: E501


        :return: The detection_status of this DetectionResultsForDescribeImagesOutput.  # noqa: E501
        :rtype: str
        """
        return self._detection_status

    @detection_status.setter
    def detection_status(self, detection_status):
        """Sets the detection_status of this DetectionResultsForDescribeImagesOutput.


        :param detection_status: The detection_status of this DetectionResultsForDescribeImagesOutput.  # noqa: E501
        :type: str
        """

        self._detection_status = detection_status

    @property
    def items(self):
        """Gets the items of this DetectionResultsForDescribeImagesOutput.  # noqa: E501


        :return: The items of this DetectionResultsForDescribeImagesOutput.  # noqa: E501
        :rtype: list[ItemForDescribeImagesOutput]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this DetectionResultsForDescribeImagesOutput.


        :param items: The items of this DetectionResultsForDescribeImagesOutput.  # noqa: E501
        :type: list[ItemForDescribeImagesOutput]
        """

        self._items = items

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
        if issubclass(DetectionResultsForDescribeImagesOutput, dict):
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
        if not isinstance(other, DetectionResultsForDescribeImagesOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DetectionResultsForDescribeImagesOutput):
            return True

        return self.to_dict() != other.to_dict()
