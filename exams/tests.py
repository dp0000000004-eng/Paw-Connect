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


class ExtraExamViewTests(TestCase):
    def setUp(self):
        self.cse = Departments.objects.create(name="Computer Engg", code="CSE")
        self.ee = Departments.objects.create(name="Electrical Engg", code="EE")
        self.semester = Semester.objects.create(semester=3)
        Syllabus.objects.create(
            branch=self.cse,
            semester=self.semester,
            link="https://example.com/cse.pdf",
        )
        Syllabus.objects.create(
            branch=self.ee,
            semester=self.semester,
            link="https://example.com/ee.pdf",
        )

    def test_departments_lists_all_branches(self):
        response = self.client.get(reverse("exam:branch"))
        self.assertContains(response, "Computer Engg")
        self.assertContains(response, "Electrical Engg")
        self.assertTemplateUsed(response, "exams/branchs.html")

    def test_syllabus_shows_link_for_that_branch(self):
        response = self.client.get(reverse("exam:syllabus", args=[self.cse.id]))
        self.assertContains(response, "https://example.com/cse.pdf")
        self.assertNotContains(response, "https://example.com/ee.pdf")
        self.assertTemplateUsed(response, "exams/links.html")

    def test_syllabus_unknown_branch_still_ok(self):
        response = self.client.get(reverse("exam:syllabus", args=[99999]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "https://example.com/cse.pdf")

    def test_syllabus_related_to_semester(self):
        item = Syllabus.objects.get(link="https://example.com/cse.pdf")
        self.assertEqual(item.semester.semester, 3)
        self.assertEqual(item.branch.code, "CSE")
