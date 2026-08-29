from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import FeedbackForm, StudentForm
from .models import (
    Collage_Meta_Data,
    Contact,
    Departments,
    FeedBack,
    HOD_Model,
    Students,
)


class ModelTests(TestCase):
    def setUp(self):
        self.department = Departments.objects.create(name="Computer Engineering", code="CSE")

    def test_department_str(self):
        self.assertEqual(str(self.department), "Computer Engineering(CSE)")

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

    def test_israt_requires_login(self):
        response = self.client.get(reverse("user:israt"))
        self.assertEqual(response.status_code, 302)

    def test_israt_when_logged_in(self):
        self.client.login(username="tester", password="secret123")
        response = self.client.get(reverse("user:israt"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello From Israt")

    def test_feedback_requires_login(self):
        response = self.client.get(reverse("user:feedback"))
        self.assertEqual(response.status_code, 302)

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

    @patch("accounts.views.smtplib.SMTP_SSL")
    def test_create_account_get(self, mock_smtp):
        mock_smtp.return_value.__enter__.return_value = MagicMock()
        response = self.client.get(reverse("user:create_account"))
        self.assertEqual(response.status_code, 200)

    @patch("accounts.views.smtplib.SMTP_SSL")
    def test_create_account_post_creates_user(self, mock_smtp):
        mock_smtp.return_value.__enter__.return_value = MagicMock()
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

    @patch("accounts.views.smtplib.SMTP_SSL")
    def test_create_account_duplicate_username(self, mock_smtp):
        mock_smtp.return_value.__enter__.return_value = MagicMock()
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
