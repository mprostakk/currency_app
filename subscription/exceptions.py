from rest_framework.exceptions import APIException


class SubscriptionException(APIException):
    status_code = 404
    default_detail = 'Subscription for user does not exist.'
    default_code = 'subscription_doesnt_exists'


class CurrencyException(APIException):
    status_code = 403
    default_detail = 'This currency doesnt exist in our system.'
    default_code = 'currency_doesnt_exists'


class SubscriptionDuplicateException(APIException):
    status_code = 403
    default_detail = 'User already has a subscription for currency.'
    default_code = 'subscription_duplicate'
