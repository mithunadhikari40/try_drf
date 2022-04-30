from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class CustomRateThrottle(UserRateThrottle):
    scope = 'custom_rate_annon'


