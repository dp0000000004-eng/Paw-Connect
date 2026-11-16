from rest_framework.throttling import AnonRateThrottle

class ConttactTrottle(AnonRateThrottle):
    scope = "ten"


class FeedBackTrottle(AnonRateThrottle):
    scope = "two"