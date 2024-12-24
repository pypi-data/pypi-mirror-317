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


class DescribeDBInstancePriceDetailResponse(object):
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
        'billing_method': 'str',
        'charge_item_prices': 'list[ChargeItemPriceForDescribeDBInstancePriceDetailOutput]',
        'coupon_amount': 'float',
        'currency': 'str',
        'discount_price': 'float',
        'original_price': 'float',
        'payable_price': 'float',
        'quantity': 'int',
        'refund_amount': 'float'
    }

    attribute_map = {
        'billing_method': 'BillingMethod',
        'charge_item_prices': 'ChargeItemPrices',
        'coupon_amount': 'CouponAmount',
        'currency': 'Currency',
        'discount_price': 'DiscountPrice',
        'original_price': 'OriginalPrice',
        'payable_price': 'PayablePrice',
        'quantity': 'Quantity',
        'refund_amount': 'RefundAmount'
    }

    def __init__(self, billing_method=None, charge_item_prices=None, coupon_amount=None, currency=None, discount_price=None, original_price=None, payable_price=None, quantity=None, refund_amount=None, _configuration=None):  # noqa: E501
        """DescribeDBInstancePriceDetailResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._billing_method = None
        self._charge_item_prices = None
        self._coupon_amount = None
        self._currency = None
        self._discount_price = None
        self._original_price = None
        self._payable_price = None
        self._quantity = None
        self._refund_amount = None
        self.discriminator = None

        if billing_method is not None:
            self.billing_method = billing_method
        if charge_item_prices is not None:
            self.charge_item_prices = charge_item_prices
        if coupon_amount is not None:
            self.coupon_amount = coupon_amount
        if currency is not None:
            self.currency = currency
        if discount_price is not None:
            self.discount_price = discount_price
        if original_price is not None:
            self.original_price = original_price
        if payable_price is not None:
            self.payable_price = payable_price
        if quantity is not None:
            self.quantity = quantity
        if refund_amount is not None:
            self.refund_amount = refund_amount

    @property
    def billing_method(self):
        """Gets the billing_method of this DescribeDBInstancePriceDetailResponse.  # noqa: E501


        :return: The billing_method of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :rtype: str
        """
        return self._billing_method

    @billing_method.setter
    def billing_method(self, billing_method):
        """Sets the billing_method of this DescribeDBInstancePriceDetailResponse.


        :param billing_method: The billing_method of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :type: str
        """

        self._billing_method = billing_method

    @property
    def charge_item_prices(self):
        """Gets the charge_item_prices of this DescribeDBInstancePriceDetailResponse.  # noqa: E501


        :return: The charge_item_prices of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :rtype: list[ChargeItemPriceForDescribeDBInstancePriceDetailOutput]
        """
        return self._charge_item_prices

    @charge_item_prices.setter
    def charge_item_prices(self, charge_item_prices):
        """Sets the charge_item_prices of this DescribeDBInstancePriceDetailResponse.


        :param charge_item_prices: The charge_item_prices of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :type: list[ChargeItemPriceForDescribeDBInstancePriceDetailOutput]
        """

        self._charge_item_prices = charge_item_prices

    @property
    def coupon_amount(self):
        """Gets the coupon_amount of this DescribeDBInstancePriceDetailResponse.  # noqa: E501


        :return: The coupon_amount of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :rtype: float
        """
        return self._coupon_amount

    @coupon_amount.setter
    def coupon_amount(self, coupon_amount):
        """Sets the coupon_amount of this DescribeDBInstancePriceDetailResponse.


        :param coupon_amount: The coupon_amount of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :type: float
        """

        self._coupon_amount = coupon_amount

    @property
    def currency(self):
        """Gets the currency of this DescribeDBInstancePriceDetailResponse.  # noqa: E501


        :return: The currency of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this DescribeDBInstancePriceDetailResponse.


        :param currency: The currency of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :type: str
        """

        self._currency = currency

    @property
    def discount_price(self):
        """Gets the discount_price of this DescribeDBInstancePriceDetailResponse.  # noqa: E501


        :return: The discount_price of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :rtype: float
        """
        return self._discount_price

    @discount_price.setter
    def discount_price(self, discount_price):
        """Sets the discount_price of this DescribeDBInstancePriceDetailResponse.


        :param discount_price: The discount_price of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :type: float
        """

        self._discount_price = discount_price

    @property
    def original_price(self):
        """Gets the original_price of this DescribeDBInstancePriceDetailResponse.  # noqa: E501


        :return: The original_price of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :rtype: float
        """
        return self._original_price

    @original_price.setter
    def original_price(self, original_price):
        """Sets the original_price of this DescribeDBInstancePriceDetailResponse.


        :param original_price: The original_price of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :type: float
        """

        self._original_price = original_price

    @property
    def payable_price(self):
        """Gets the payable_price of this DescribeDBInstancePriceDetailResponse.  # noqa: E501


        :return: The payable_price of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :rtype: float
        """
        return self._payable_price

    @payable_price.setter
    def payable_price(self, payable_price):
        """Sets the payable_price of this DescribeDBInstancePriceDetailResponse.


        :param payable_price: The payable_price of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :type: float
        """

        self._payable_price = payable_price

    @property
    def quantity(self):
        """Gets the quantity of this DescribeDBInstancePriceDetailResponse.  # noqa: E501


        :return: The quantity of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this DescribeDBInstancePriceDetailResponse.


        :param quantity: The quantity of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :type: int
        """

        self._quantity = quantity

    @property
    def refund_amount(self):
        """Gets the refund_amount of this DescribeDBInstancePriceDetailResponse.  # noqa: E501


        :return: The refund_amount of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :rtype: float
        """
        return self._refund_amount

    @refund_amount.setter
    def refund_amount(self, refund_amount):
        """Sets the refund_amount of this DescribeDBInstancePriceDetailResponse.


        :param refund_amount: The refund_amount of this DescribeDBInstancePriceDetailResponse.  # noqa: E501
        :type: float
        """

        self._refund_amount = refund_amount

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
        if issubclass(DescribeDBInstancePriceDetailResponse, dict):
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
        if not isinstance(other, DescribeDBInstancePriceDetailResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DescribeDBInstancePriceDetailResponse):
            return True

        return self.to_dict() != other.to_dict()
