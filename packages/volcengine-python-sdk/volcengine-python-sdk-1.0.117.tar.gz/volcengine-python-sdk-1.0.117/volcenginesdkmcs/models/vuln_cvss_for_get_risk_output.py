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


class VulnCvssForGetRiskOutput(object):
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
        'cvss_score': 'float',
        'cvss_vec': 'str'
    }

    attribute_map = {
        'cvss_score': 'CvssScore',
        'cvss_vec': 'CvssVec'
    }

    def __init__(self, cvss_score=None, cvss_vec=None, _configuration=None):  # noqa: E501
        """VulnCvssForGetRiskOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cvss_score = None
        self._cvss_vec = None
        self.discriminator = None

        if cvss_score is not None:
            self.cvss_score = cvss_score
        if cvss_vec is not None:
            self.cvss_vec = cvss_vec

    @property
    def cvss_score(self):
        """Gets the cvss_score of this VulnCvssForGetRiskOutput.  # noqa: E501


        :return: The cvss_score of this VulnCvssForGetRiskOutput.  # noqa: E501
        :rtype: float
        """
        return self._cvss_score

    @cvss_score.setter
    def cvss_score(self, cvss_score):
        """Sets the cvss_score of this VulnCvssForGetRiskOutput.


        :param cvss_score: The cvss_score of this VulnCvssForGetRiskOutput.  # noqa: E501
        :type: float
        """

        self._cvss_score = cvss_score

    @property
    def cvss_vec(self):
        """Gets the cvss_vec of this VulnCvssForGetRiskOutput.  # noqa: E501


        :return: The cvss_vec of this VulnCvssForGetRiskOutput.  # noqa: E501
        :rtype: str
        """
        return self._cvss_vec

    @cvss_vec.setter
    def cvss_vec(self, cvss_vec):
        """Sets the cvss_vec of this VulnCvssForGetRiskOutput.


        :param cvss_vec: The cvss_vec of this VulnCvssForGetRiskOutput.  # noqa: E501
        :type: str
        """

        self._cvss_vec = cvss_vec

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
        if issubclass(VulnCvssForGetRiskOutput, dict):
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
        if not isinstance(other, VulnCvssForGetRiskOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, VulnCvssForGetRiskOutput):
            return True

        return self.to_dict() != other.to_dict()
