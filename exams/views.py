
from django.shortcuts import render
from .models import Syllabus, Semester
from accounts.models import Departments
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from .serializers import SyllabusSerializer, SemesterSerializer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from rest_framework_csv.renderers import CSVRenderer


def departments(request):

    branches = Departments.objects.all()

    return render(
        request,
        'exams/branchs.html',
        {
            "branches": branches
        }
    )

@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, XMLRenderer, CSVRenderer, YAMLRenderer])
def syllabus(request, branch_id):
    # Only syllabus records that belong to this department / branch
    syllabuses = Syllabus.objects.filter(branch=branch_id)
    syllabusesSerializer = SyllabusSerializer(syllabuses, many=True)

    return Response(
        {
            "syllabuses": syllabusesSerializer.data
        },
        template_name="exams/links.html"
    )


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def semester_API_view(request):
    semesters = Semester.objects.all()
    semesterSerializer = SemesterSerializer(semesters, many=True)

    return Response(
        semesterSerializer.data
    )