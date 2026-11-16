from rest_framework.throttling import UserRateThrottle


class AIPromptThrottle(UserRateThrottle):
    scope = "max_ai_prompt"