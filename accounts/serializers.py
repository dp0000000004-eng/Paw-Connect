from rest_framework import serializers
from .models import Collage_Meta_Data, Departments
import bleach
from .models import Students, HOD_Model, FeedBack, Contact


class CollageMetaSerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        return bleach.clean(value)
    def validate_start_in(self, value):
        return bleach.clean(value)
    class Meta:
        model = Collage_Meta_Data
        fields = ['id', 'name', 'start_in']

    extra_kwags = {

        "start_in":{
            "min_value":4,
            "max_value":4
        }
    }



class DepartmentSerializer(serializers.ModelSerializer):

    def validate_name(self, value):
        return bleach.clean(value)
    def validate_code(self, value):
        return bleach.clean(value)
    class Meta:
        model = Departments
        fields = ['id', 'name', 'code']

class HOD_ModelSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()

    def validate_name(self, value):
        return bleach.clean(value)
    def validate_department(self, value):              #ERROR
        return bleach.clean(value)
    def validate_description(self, value):
        return bleach.clean(value)
    

    class Meta:
        model = HOD_Model
        fields = ['id', 'name', 'department', 'description']


class StudentsSerializer(serializers.ModelSerializer):

    def validate_first_name(self, value):
        return bleach.clean(value, tags=[], strip=True)
    def validate_last_name(self, value):
        return bleach.clean(value)
    def validate_email(self, value):
        return bleach.clean(value)
    def validate_branch(self, value):
        return bleach.clean(str(value))
    def validate_register_no(self, value):
        return bleach.clean(value)
    def validate_phone_no(self, value):
        return bleach.clean(value)
    class Meta:
        model = Students
        fields = ['id', 'first_name', 'last_name', 'email', 'branch', 'register_no','phone_no' ]

    extra_kwags = {
        "phone_no":{
            "min_value":10,
            "max_value":10
        }
    }

class ContactSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        return bleach.clean(value)
    def validate_contact_no(self, value):
        return bleach.clean(value)
    class Meta:
        model = Contact
        fields = ['id', 'email', 'contact_no']

    extra_kwags = {
        "phone_no":{
            "min_value":10,
            "max_value":10
        }
    }



class FeedBackSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = FeedBack
        fields = ['id', 'user', 'description']