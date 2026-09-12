
from django.shortcuts import render
from .models import Syllabus
from accounts.models import Departments
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from .serializers import SyllabusSerializer


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
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
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
