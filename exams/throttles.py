from rest_framework.throttling import AnonRateThrottle


class ResourceThrottle(AnonRateThrottle):
    scope = "fifteen"