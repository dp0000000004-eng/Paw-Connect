from django.test import TestCase
from django.urls import reverse

from accounts.models import Departments

from .models import Semester, Syllabus


class ExamModelTests(TestCase):
    def setUp(self):
        self.department = Departments.objects.create(name="CSE", code="CSE")
        self.semester = Semester.objects.create(semester=5)

    def test_semester_str(self):
        self.assertEqual(str(self.semester), "5")

    def test_syllabus_str(self):
        syllabus = Syllabus.objects.create(
            branch=self.department,
            semester=self.semester,
            link="https://example.com/cse-sem5.pdf",
        )
        self.assertEqual(str(syllabus), "https://example.com/cse-sem5.pdf")


class ExamViewTests(TestCase):
    def setUp(self):
        self.department = Departments.objects.create(name="Computer Engg", code="CSE")
        self.semester = Semester.objects.create(semester=3)
        Syllabus.objects.create(
            branch=self.department,
            semester=self.semester,
            link="https://example.com/syllabus.pdf",
        )

    def test_departments_page(self):
        response = self.client.get(reverse("exam:branch"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Computer Engg")

    def test_syllabus_page_loads(self):
        response = self.client.get(reverse("exam:syllabus", args=[self.department.id]))
        self.assertEqual(response.status_code, 200)
