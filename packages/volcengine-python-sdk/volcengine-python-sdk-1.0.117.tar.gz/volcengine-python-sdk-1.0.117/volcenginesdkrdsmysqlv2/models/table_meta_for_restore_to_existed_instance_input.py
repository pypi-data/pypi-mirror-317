# coding: utf-8

"""
    rds_mysql_v2

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class TableMetaForRestoreToExistedInstanceInput(object):
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
        'db_name': 'str',
        'new_db_name': 'str',
        'table': 'list[TableForRestoreToExistedInstanceInput]'
    }

    attribute_map = {
        'db_name': 'DBName',
        'new_db_name': 'NewDBName',
        'table': 'Table'
    }

    def __init__(self, db_name=None, new_db_name=None, table=None, _configuration=None):  # noqa: E501
        """TableMetaForRestoreToExistedInstanceInput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._db_name = None
        self._new_db_name = None
        self._table = None
        self.discriminator = None

        if db_name is not None:
            self.db_name = db_name
        if new_db_name is not None:
            self.new_db_name = new_db_name
        if table is not None:
            self.table = table

    @property
    def db_name(self):
        """Gets the db_name of this TableMetaForRestoreToExistedInstanceInput.  # noqa: E501


        :return: The db_name of this TableMetaForRestoreToExistedInstanceInput.  # noqa: E501
        :rtype: str
        """
        return self._db_name

    @db_name.setter
    def db_name(self, db_name):
        """Sets the db_name of this TableMetaForRestoreToExistedInstanceInput.


        :param db_name: The db_name of this TableMetaForRestoreToExistedInstanceInput.  # noqa: E501
        :type: str
        """

        self._db_name = db_name

    @property
    def new_db_name(self):
        """Gets the new_db_name of this TableMetaForRestoreToExistedInstanceInput.  # noqa: E501


        :return: The new_db_name of this TableMetaForRestoreToExistedInstanceInput.  # noqa: E501
        :rtype: str
        """
        return self._new_db_name

    @new_db_name.setter
    def new_db_name(self, new_db_name):
        """Sets the new_db_name of this TableMetaForRestoreToExistedInstanceInput.


        :param new_db_name: The new_db_name of this TableMetaForRestoreToExistedInstanceInput.  # noqa: E501
        :type: str
        """

        self._new_db_name = new_db_name

    @property
    def table(self):
        """Gets the table of this TableMetaForRestoreToExistedInstanceInput.  # noqa: E501


        :return: The table of this TableMetaForRestoreToExistedInstanceInput.  # noqa: E501
        :rtype: list[TableForRestoreToExistedInstanceInput]
        """
        return self._table

    @table.setter
    def table(self, table):
        """Sets the table of this TableMetaForRestoreToExistedInstanceInput.


        :param table: The table of this TableMetaForRestoreToExistedInstanceInput.  # noqa: E501
        :type: list[TableForRestoreToExistedInstanceInput]
        """

        self._table = table

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
        if issubclass(TableMetaForRestoreToExistedInstanceInput, dict):
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
        if not isinstance(other, TableMetaForRestoreToExistedInstanceInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TableMetaForRestoreToExistedInstanceInput):
            return True

        return self.to_dict() != other.to_dict()
