from .models import Chat
from rest_framework import serializers
import bleach


class ChatSerializer(serializers.ModelSerializer):

    def validate_user(self, value):
        return bleach.clean(value)
    def validate_prompt(self, value):
        return bleach.clean(value)
    def validate_response(self, value):
        return bleach.clean(value)
    class Meta:
        model = Chat
        fields = ['id', 'user','prompt', 'response']