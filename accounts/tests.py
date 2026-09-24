from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .forms import FeedbackForm, StudentForm
from .models import (
    Collage_Meta_Data,
    Contact,
    Departments,
    FeedBack,
    HOD_Model,
    Students,
)
from .serializers import (
    CollageMetaSerializer,
    ContactSerializer,
    DepartmentSerializer,
    FeedBackSerializer,
    HOD_ModelSerializer,
    StudentsSerializer,
)


class ModelTests(TestCase):
    def setUp(self):
        self.department = Departments.objects.create(name="Computer Engineering", code="CSE")

    def test_department_str(self):
        self.assertEqual(
            str(self.department),
            f"Computer Engineering {self.department.id} CSE",
        )

    def test_student_str(self):
        student = Students.objects.create(
            first_name="Rahul",
            last_name="Sahu",
            email="rahul@example.com",
            branch=self.department,
            register_no="REG001",
            phone_no=9876543210,
        )
        self.assertIn("Rahul", str(student))
        self.assertIn("Sahu", str(student))

    def test_hod_str(self):
        hod = HOD_Model.objects.create(
            name="Dr. Sharma",
            department=self.department,
            description="Head of CSE",
        )
        self.assertIn("Dr. Sharma", str(hod))

    def test_feedback_str(self):
        user = User.objects.create_user(username="student1", password="pass12345")
        feedback = FeedBack.objects.create(user=user, description="Great portal")
        self.assertEqual(str(feedback), "Great portal")

    def test_contact_str(self):
        contact = Contact.objects.create(email="office@college.edu", contact_no=1234567890)
        self.assertIn("office@college.edu", str(contact))

    def test_college_meta_data_create(self):
        college = Collage_Meta_Data.objects.create(name="GP Angul", start_in=1957)
        self.assertEqual(college.name, "GP Angul")
        self.assertEqual(college.start_in, 1957)


class FormTests(TestCase):
    def setUp(self):
        self.department = Departments.objects.create(name="IoT", code="IOT")

    def test_student_form_valid(self):
        form = StudentForm(
            data={
                "first_name": "Asha",
                "last_name": "Das",
                "email": "asha@example.com",
                "branch": self.department.id,
                "register_no": "REG002",
                "phone_no": 9998887776,
            }
        )
        self.assertTrue(form.is_valid())

    def test_feedback_form_valid(self):
        form = FeedbackForm(data={"description": "Please add attendance."})
        self.assertTrue(form.is_valid())

    def test_feedback_form_empty_invalid(self):
        form = FeedbackForm(data={"description": ""})
        self.assertFalse(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="secret123",
        )
        self.department = Departments.objects.create(name="CSE", code="CSE")
        HOD_Model.objects.create(
            name="HOD One",
            department=self.department,
            description="Department head",
        )
        Contact.objects.create(email="help@college.edu", contact_no=1112223334)

    def test_home_get(self):
        response = self.client.get(reverse("user:home"))
        self.assertEqual(response.status_code, 200)

    def test_root_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_about_lists_hods(self):
        response = self.client.get(reverse("user:about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HOD One")

    def test_contact_page(self):
        response = self.client.get(reverse("user:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "help@college.edu")

    def test_login_get(self):
        response = self.client.get(reverse("user:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_success_redirects_home(self):
        response = self.client.post(
            reverse("user:login"),
            {"username": "tester", "password": "secret123"},
        )
        self.assertRedirects(response, reverse("user:home"))

    def test_login_invalid_credentials(self):
        response = self.client.post(
            reverse("user:login"),
            {"username": "tester", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid Credentials")

    def test_feedback_get_is_public(self):
        response = self.client.get(reverse("user:feedback"))
        self.assertEqual(response.status_code, 200)

    def test_feedback_post_saves(self):
        self.client.login(username="tester", password="secret123")
        response = self.client.post(
            reverse("user:feedback"),
            {"description": "Need more exam links"},
        )
        self.assertRedirects(response, reverse("user:home"))
        self.assertTrue(FeedBack.objects.filter(description="Need more exam links").exists())

    def test_logout_redirects_home(self):
        self.client.login(username="tester", password="secret123")
        response = self.client.get(reverse("user:logout"))
        self.assertRedirects(response, reverse("user:home"))

    def test_create_account_get(self):
        response = self.client.get(reverse("user:create_account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_acc.html")

    @patch("accounts.views.send_welcome_email")
    def test_create_account_post_creates_user(self, mock_send_mail):
        response = self.client.post(
            reverse("user:create_account"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "newpass123",
            },
        )
        self.assertRedirects(response, reverse("user:home"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    @patch("accounts.views.send_welcome_email")
    def test_create_account_duplicate_username(self, mock_send_mail):
        response = self.client.post(
            reverse("user:create_account"),
            {
                "username": "tester",
                "email": "dup@example.com",
                "password": "anotherpass",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username exists")


class ExtraAccountViewTests(TestCase):
    """More coverage for signup, sessions, and protected pages."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="secret123",
        )
        Contact.objects.create(email="help@college.edu", contact_no=1112223334)

    def test_home_uses_welcome_template(self):
        response = self.client.get(reverse("user:home"))
        self.assertTemplateUsed(response, "welcome.html")

    def test_login_uses_login_template(self):
        response = self.client.get(reverse("user:login"))
        self.assertTemplateUsed(response, "Login.html")

    def test_login_success_sets_session_user(self):
        self.client.post(
            reverse("user:login"),
            {"username": "tester", "password": "secret123"},
        )
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.id)

    def test_logout_requires_login(self):
        response = self.client.get(reverse("user:logout"))
        self.assertEqual(response.status_code, 302)

    def test_logout_ends_session(self):
        self.client.login(username="tester", password="secret123")
        self.client.get(reverse("user:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_feedback_get_when_logged_in(self):
        self.client.login(username="tester", password="secret123")
        response = self.client.get(reverse("user:feedback"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feedback.html")

    def test_feedback_post_linked_to_logged_in_user(self):
        self.client.login(username="tester", password="secret123")
        self.client.post(
            reverse("user:feedback"),
            {"description": "Campus wifi is slow"},
        )
        feedback = FeedBack.objects.get(description="Campus wifi is slow")
        self.assertEqual(feedback.user, self.user)

    @patch("accounts.views.send_welcome_email")
    def test_create_account_hashes_password(self, mock_send_mail):
        self.client.post(
            reverse("user:create_account"),
            {
                "username": "hasheduser",
                "email": "hash@example.com",
                "password": "plainpass99",
            },
        )
        user = User.objects.get(username="hasheduser")
        self.assertNotEqual(user.password, "plainpass99")
        self.assertTrue(user.check_password("plainpass99"))

    @patch("accounts.views.send_welcome_email")
    def test_create_account_sends_welcome_email(self, mock_send_mail):
        self.client.post(
            reverse("user:create_account"),
            {
                "username": "mailuser",
                "email": "mail@example.com",
                "password": "mailpass99",
            },
        )
        mock_send_mail.assert_called_once_with("mailuser", "mail@example.com")

    @patch("accounts.views.send_welcome_email")
    def test_create_account_duplicate_does_not_add_user(self, mock_send_mail):
        before = User.objects.count()
        self.client.post(
            reverse("user:create_account"),
            {
                "username": "tester",
                "email": "dup@example.com",
                "password": "anotherpass",
            },
        )
        self.assertEqual(User.objects.count(), before)

    def test_contact_lists_first_row(self):
        Contact.objects.create(email="second@college.edu", contact_no=9998887776)
        response = self.client.get(reverse("user:contact"))
        self.assertContains(response, "help@college.edu")

    def test_about_uses_about_template(self):
        response = self.client.get(reverse("user:about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")


class ExtraFormTests(TestCase):
    def test_student_form_missing_fields_invalid(self):
        form = StudentForm(data={"first_name": "Only"})
        self.assertFalse(form.is_valid())


class AccountImportTests(TestCase):
    def test_models_serializers_views_urls_import(self):
        from accounts import models as account_models
        from accounts import serializers as account_serializers
        from accounts import urls as account_urls
        from accounts import views as account_views

        self.assertTrue(account_models.Departments)
        self.assertTrue(account_serializers.HOD_ModelSerializer)
        self.assertTrue(account_views.about_view)
        self.assertTrue(account_urls.urlpatterns)


class AccountSerializerTests(TestCase):
    def setUp(self):
        self.department = Departments.objects.create(name="Computer Engineering", code="CSE")
        self.user = User.objects.create_user(username="serialuser", password="pass12345")

    def test_college_meta_serializer(self):
        college = Collage_Meta_Data.objects.create(name="GP Angul", start_in=1957)
        data = CollageMetaSerializer(college).data
        self.assertEqual(data["name"], "GP Angul")
        self.assertEqual(data["start_in"], 1957)

    def test_department_serializer(self):
        data = DepartmentSerializer(self.department).data
        self.assertEqual(data["name"], "Computer Engineering")
        self.assertEqual(data["code"], "CSE")

    def test_department_serializer_strips_html(self):
        serializer = DepartmentSerializer(
            data={"name": "<script>alert(1)</script>IoT", "code": "IOT"}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("<script>", serializer.validated_data["name"])

    def test_hod_serializer_uses_department_string(self):
        hod = HOD_Model.objects.create(
            name="Dr. Sharma",
            department=self.department,
            description="Head of CSE",
        )
        data = HOD_ModelSerializer(hod).data
        self.assertEqual(data["name"], "Dr. Sharma")
        self.assertEqual(data["department"], str(self.department))
        self.assertEqual(data["description"], "Head of CSE")

    def test_student_serializer(self):
        student = Students.objects.create(
            first_name="Rahul",
            last_name="Sahu",
            email="rahul@example.com",
            branch=self.department,
            register_no="REG001",
            phone_no=9876543210,
        )
        data = StudentsSerializer(student).data
        self.assertEqual(data["first_name"], "Rahul")
        self.assertEqual(data["branch"], self.department.id)
        self.assertEqual(data["register_no"], "REG001")

    def test_student_serializer_strips_html_on_name(self):
        serializer = StudentsSerializer()
        cleaned = serializer.validate_first_name("<b>Asha</b>")
        self.assertNotIn("<b>", cleaned)

    def test_contact_serializer(self):
        contact = Contact.objects.create(email="office@college.edu", contact_no=1234567890)
        data = ContactSerializer(contact).data
        self.assertEqual(data["email"], "office@college.edu")
        self.assertEqual(data["contact_no"], 1234567890)

    def test_feedback_serializer_uses_user_string(self):
        feedback = FeedBack.objects.create(user=self.user, description="Great portal")
        data = FeedBackSerializer(feedback).data
        self.assertEqual(data["user"], str(self.user))
        self.assertEqual(data["description"], "Great portal")


class AccountRestApiViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="apiuser",
            email="api@example.com",
            password="secret123",
        )
        self.department = Departments.objects.create(name="CSE", code="CSE")
        HOD_Model.objects.create(
            name="HOD One",
            department=self.department,
            description="Department head",
        )
        Contact.objects.create(email="help@college.edu", contact_no=1112223334)
        FeedBack.objects.create(user=self.user, description="Need labs")

    def test_about_json_lists_hods(self):
        response = self.client.get(reverse("user:about"), HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"].split(";")[0], "application/json")
        payload = response.json()
        self.assertIn("hods", payload)
        self.assertEqual(payload["hods"][0]["name"], "HOD One")
        self.assertEqual(payload["hods"][0]["department"], str(self.department))

    def test_about_xml_renders(self):
        response = self.client.get(reverse("user:about"), HTTP_ACCEPT="application/xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("xml", response["Content-Type"])
        self.assertIn(b"HOD One", response.content)

    def test_about_yaml_renders(self):
        response = self.client.get(reverse("user:about"), HTTP_ACCEPT="application/yaml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"HOD One", response.content)

    def test_contact_json_lists_contacts(self):
        response = self.client.get(reverse("user:contact"), HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("datas", payload)
        self.assertEqual(payload["datas"]["email"], "help@college.edu")

    def test_contact_csv_renders(self):
        response = self.client.get(reverse("user:contact"), HTTP_ACCEPT="text/csv")
        self.assertEqual(response.status_code, 200)
        self.assertIn("csv", response["Content-Type"])

    def test_feedback_json_lists_feedbacks(self):
        response = self.client.get(reverse("user:feedback"), HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("feedbacks", payload)
        self.assertEqual(payload["feedbacks"][0]["description"], "Need labs")
        self.assertEqual(payload["feedbacks"][0]["user"], "apiuser")

    def test_feedback_json_post_saves_when_authenticated(self):
        self.client.login(username="apiuser", password="secret123")
        response = self.client.post(
            reverse("user:feedback"),
            {"description": "API feedback"},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FeedBack.objects.filter(description="API feedback").exists())
