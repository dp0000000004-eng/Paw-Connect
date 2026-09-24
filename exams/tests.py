from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import Departments

from .models import Semester, StudyNotes, Syllabus
from .serializers import SemesterSerializer, StudyNoteSerializer, SyllabusSerializer


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


class ExamImportTests(TestCase):
    def test_models_serializers_views_urls_import(self):
        from exams import models as exam_models
        from exams import serializers as exam_serializers
        from exams import urls as exam_urls
        from exams import views as exam_views

        self.assertTrue(exam_models.StudyNotes)
        self.assertTrue(exam_serializers.SyllabusSerializer)
        self.assertTrue(exam_views.semester_API_view)
        self.assertTrue(exam_urls.urlpatterns)


class ExamModelExtraTests(TestCase):
    def test_study_notes_str(self):
        department = Departments.objects.create(name="CSE", code="CSE")
        semester = Semester.objects.create(semester=4)
        note = StudyNotes.objects.create(
            branch=department,
            semseter=semester,
            link="https://example.com/notes.pdf",
        )
        self.assertIn("CSE", str(note))
        self.assertIn("4", str(note))


class ExamSerializerTests(TestCase):
    def setUp(self):
        self.department = Departments.objects.create(name="Computer Engg", code="CSE")
        self.semester = Semester.objects.create(semester=3)
        self.syllabus = Syllabus.objects.create(
            branch=self.department,
            semester=self.semester,
            link="https://example.com/syllabus.pdf",
        )
        self.note = StudyNotes.objects.create(
            branch=self.department,
            semseter=self.semester,
            link="https://example.com/notes.pdf",
        )

    def test_semester_serializer(self):
        data = SemesterSerializer(self.semester).data
        self.assertEqual(data["semester"], 3)

    def test_syllabus_serializer_uses_branch_string(self):
        data = SyllabusSerializer(self.syllabus).data
        self.assertEqual(data["branch"], str(self.department))
        self.assertEqual(data["semester"], self.semester.id)
        self.assertEqual(data["link"], "https://example.com/syllabus.pdf")

    def test_study_note_serializer_uses_branch_string(self):
        data = StudyNoteSerializer(self.note).data
        self.assertEqual(data["branch"], str(self.department))
        self.assertEqual(data["semseter"], self.semester.id)
        self.assertEqual(data["link"], "https://example.com/notes.pdf")

    def test_syllabus_serializer_strips_html_from_link(self):
        serializer = SyllabusSerializer()
        cleaned = serializer.validate_link("https://example.com/<script>x</script>file.pdf")
        self.assertNotIn("<script>", cleaned)


class ExamRestApiViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
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

    def test_semester_api_returns_json(self):
        response = self.client.get("/exams/semi/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"].split(";")[0], "application/json")
        payload = response.json()
        self.assertEqual(payload[0]["semester"], 3)

    def test_syllabus_json_filters_by_branch(self):
        response = self.client.get(
            reverse("exam:syllabus", args=[self.cse.id]),
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("syllabuses", payload)
        links = [item["link"] for item in payload["syllabuses"]]
        self.assertEqual(links, ["https://example.com/cse.pdf"])

    def test_syllabus_xml_renders(self):
        response = self.client.get(
            reverse("exam:syllabus", args=[self.cse.id]),
            HTTP_ACCEPT="application/xml",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"cse.pdf", response.content)
        self.assertNotIn(b"ee.pdf", response.content)
