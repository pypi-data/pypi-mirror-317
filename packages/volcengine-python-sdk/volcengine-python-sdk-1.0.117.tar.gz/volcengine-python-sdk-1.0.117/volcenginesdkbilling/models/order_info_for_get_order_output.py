# coding: utf-8

"""
    billing

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: common-version
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from volcenginesdkcore.configuration import Configuration


class OrderInfoForGetOrderOutput(object):
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
        'buyer_customer_name': 'str',
        'buyer_id': 'int',
        'coupon_amount': 'str',
        'create_time': 'str',
        'discount_amount': 'str',
        'order_id': 'str',
        'order_type': 'str',
        'original_amount': 'str',
        'paid_amount': 'str',
        'payable_amount': 'str',
        'payer_customer_name': 'str',
        'payer_id': 'int',
        'seller_customer_name': 'str',
        'seller_id': 'int',
        'status': 'str',
        'subject_no': 'str'
    }

    attribute_map = {
        'buyer_customer_name': 'BuyerCustomerName',
        'buyer_id': 'BuyerID',
        'coupon_amount': 'CouponAmount',
        'create_time': 'CreateTime',
        'discount_amount': 'DiscountAmount',
        'order_id': 'OrderID',
        'order_type': 'OrderType',
        'original_amount': 'OriginalAmount',
        'paid_amount': 'PaidAmount',
        'payable_amount': 'PayableAmount',
        'payer_customer_name': 'PayerCustomerName',
        'payer_id': 'PayerID',
        'seller_customer_name': 'SellerCustomerName',
        'seller_id': 'SellerID',
        'status': 'Status',
        'subject_no': 'SubjectNo'
    }

    def __init__(self, buyer_customer_name=None, buyer_id=None, coupon_amount=None, create_time=None, discount_amount=None, order_id=None, order_type=None, original_amount=None, paid_amount=None, payable_amount=None, payer_customer_name=None, payer_id=None, seller_customer_name=None, seller_id=None, status=None, subject_no=None, _configuration=None):  # noqa: E501
        """OrderInfoForGetOrderOutput - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._buyer_customer_name = None
        self._buyer_id = None
        self._coupon_amount = None
        self._create_time = None
        self._discount_amount = None
        self._order_id = None
        self._order_type = None
        self._original_amount = None
        self._paid_amount = None
        self._payable_amount = None
        self._payer_customer_name = None
        self._payer_id = None
        self._seller_customer_name = None
        self._seller_id = None
        self._status = None
        self._subject_no = None
        self.discriminator = None

        if buyer_customer_name is not None:
            self.buyer_customer_name = buyer_customer_name
        if buyer_id is not None:
            self.buyer_id = buyer_id
        if coupon_amount is not None:
            self.coupon_amount = coupon_amount
        if create_time is not None:
            self.create_time = create_time
        if discount_amount is not None:
            self.discount_amount = discount_amount
        if order_id is not None:
            self.order_id = order_id
        if order_type is not None:
            self.order_type = order_type
        if original_amount is not None:
            self.original_amount = original_amount
        if paid_amount is not None:
            self.paid_amount = paid_amount
        if payable_amount is not None:
            self.payable_amount = payable_amount
        if payer_customer_name is not None:
            self.payer_customer_name = payer_customer_name
        if payer_id is not None:
            self.payer_id = payer_id
        if seller_customer_name is not None:
            self.seller_customer_name = seller_customer_name
        if seller_id is not None:
            self.seller_id = seller_id
        if status is not None:
            self.status = status
        if subject_no is not None:
            self.subject_no = subject_no

    @property
    def buyer_customer_name(self):
        """Gets the buyer_customer_name of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The buyer_customer_name of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._buyer_customer_name

    @buyer_customer_name.setter
    def buyer_customer_name(self, buyer_customer_name):
        """Sets the buyer_customer_name of this OrderInfoForGetOrderOutput.


        :param buyer_customer_name: The buyer_customer_name of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._buyer_customer_name = buyer_customer_name

    @property
    def buyer_id(self):
        """Gets the buyer_id of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The buyer_id of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: int
        """
        return self._buyer_id

    @buyer_id.setter
    def buyer_id(self, buyer_id):
        """Sets the buyer_id of this OrderInfoForGetOrderOutput.


        :param buyer_id: The buyer_id of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: int
        """

        self._buyer_id = buyer_id

    @property
    def coupon_amount(self):
        """Gets the coupon_amount of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The coupon_amount of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._coupon_amount

    @coupon_amount.setter
    def coupon_amount(self, coupon_amount):
        """Sets the coupon_amount of this OrderInfoForGetOrderOutput.


        :param coupon_amount: The coupon_amount of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._coupon_amount = coupon_amount

    @property
    def create_time(self):
        """Gets the create_time of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The create_time of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this OrderInfoForGetOrderOutput.


        :param create_time: The create_time of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._create_time = create_time

    @property
    def discount_amount(self):
        """Gets the discount_amount of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The discount_amount of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._discount_amount

    @discount_amount.setter
    def discount_amount(self, discount_amount):
        """Sets the discount_amount of this OrderInfoForGetOrderOutput.


        :param discount_amount: The discount_amount of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._discount_amount = discount_amount

    @property
    def order_id(self):
        """Gets the order_id of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The order_id of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this OrderInfoForGetOrderOutput.


        :param order_id: The order_id of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._order_id = order_id

    @property
    def order_type(self):
        """Gets the order_type of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The order_type of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._order_type

    @order_type.setter
    def order_type(self, order_type):
        """Sets the order_type of this OrderInfoForGetOrderOutput.


        :param order_type: The order_type of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._order_type = order_type

    @property
    def original_amount(self):
        """Gets the original_amount of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The original_amount of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._original_amount

    @original_amount.setter
    def original_amount(self, original_amount):
        """Sets the original_amount of this OrderInfoForGetOrderOutput.


        :param original_amount: The original_amount of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._original_amount = original_amount

    @property
    def paid_amount(self):
        """Gets the paid_amount of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The paid_amount of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._paid_amount

    @paid_amount.setter
    def paid_amount(self, paid_amount):
        """Sets the paid_amount of this OrderInfoForGetOrderOutput.


        :param paid_amount: The paid_amount of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._paid_amount = paid_amount

    @property
    def payable_amount(self):
        """Gets the payable_amount of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The payable_amount of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._payable_amount

    @payable_amount.setter
    def payable_amount(self, payable_amount):
        """Sets the payable_amount of this OrderInfoForGetOrderOutput.


        :param payable_amount: The payable_amount of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._payable_amount = payable_amount

    @property
    def payer_customer_name(self):
        """Gets the payer_customer_name of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The payer_customer_name of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._payer_customer_name

    @payer_customer_name.setter
    def payer_customer_name(self, payer_customer_name):
        """Sets the payer_customer_name of this OrderInfoForGetOrderOutput.


        :param payer_customer_name: The payer_customer_name of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._payer_customer_name = payer_customer_name

    @property
    def payer_id(self):
        """Gets the payer_id of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The payer_id of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: int
        """
        return self._payer_id

    @payer_id.setter
    def payer_id(self, payer_id):
        """Sets the payer_id of this OrderInfoForGetOrderOutput.


        :param payer_id: The payer_id of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: int
        """

        self._payer_id = payer_id

    @property
    def seller_customer_name(self):
        """Gets the seller_customer_name of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The seller_customer_name of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._seller_customer_name

    @seller_customer_name.setter
    def seller_customer_name(self, seller_customer_name):
        """Sets the seller_customer_name of this OrderInfoForGetOrderOutput.


        :param seller_customer_name: The seller_customer_name of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._seller_customer_name = seller_customer_name

    @property
    def seller_id(self):
        """Gets the seller_id of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The seller_id of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: int
        """
        return self._seller_id

    @seller_id.setter
    def seller_id(self, seller_id):
        """Sets the seller_id of this OrderInfoForGetOrderOutput.


        :param seller_id: The seller_id of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: int
        """

        self._seller_id = seller_id

    @property
    def status(self):
        """Gets the status of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The status of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this OrderInfoForGetOrderOutput.


        :param status: The status of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def subject_no(self):
        """Gets the subject_no of this OrderInfoForGetOrderOutput.  # noqa: E501


        :return: The subject_no of this OrderInfoForGetOrderOutput.  # noqa: E501
        :rtype: str
        """
        return self._subject_no

    @subject_no.setter
    def subject_no(self, subject_no):
        """Sets the subject_no of this OrderInfoForGetOrderOutput.


        :param subject_no: The subject_no of this OrderInfoForGetOrderOutput.  # noqa: E501
        :type: str
        """

        self._subject_no = subject_no

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
        if issubclass(OrderInfoForGetOrderOutput, dict):
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
        if not isinstance(other, OrderInfoForGetOrderOutput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrderInfoForGetOrderOutput):
            return True

        return self.to_dict() != other.to_dict()
