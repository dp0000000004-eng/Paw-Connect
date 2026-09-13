from .models import Semester, Syllabus , StudyNotes
from rest_framework import serializers
import bleach


class SemesterSerializer(serializers.ModelSerializer):
    def validate_semester(self, value):
        return bleach.clean(value)

    class Meta:
        model = Semester
        fields = ['id', 'semester']

    extra_kwags = {
        "semester":{
            "min_value":1,
            "max_value":6
        }
    }


class SyllabusSerializer(serializers.ModelSerializer):

    def validate_branch(self, value):
        return bleach.clean(value)
    def validate_branch(self, value):
        return bleach.clean(value)
    def validate_link(self, value):
        return bleach.clean(value)

    branch = serializers.StringRelatedField()

    class Meta:
        model = Syllabus
        fields = ['id', 'branch', 'semester', 'link']


class StudyNoteSerializer(serializers.ModelSerializer):

    def validate_branch(self, value):
        return bleach.clean(value)
    def validate_branch(self, value):
        return bleach.clean(value)
    def validate_link(self, value):
        return bleach.clean(value)

    branch = serializers.StringRelatedField()
    class Meta:
        model = StudyNotes
        fields = ['id', 'branch', 'semseter', 'link']