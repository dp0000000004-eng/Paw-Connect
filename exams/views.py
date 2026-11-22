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
from rest_framework.decorators import throttle_classes
from .throttles import ResourceThrottle
from .models import StudyVideo, StudyHandNote
from .serializers import StudyVideoSerializer, StudyNotesSerializer
from django.http import JsonResponse


def departments(request):

    branches = Departments.objects.all()
    return render(
        request,
        'exams/branchs.html',
        {"branches": branches}
    )


@api_view(['GET', 'POST'])
@throttle_classes([ResourceThrottle])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer, XMLRenderer, CSVRenderer, YAMLRenderer])
def syllabus(request, branch_id):

    syllabuses = Syllabus.objects.filter(branch=branch_id)
    syllabusesSerializer = SyllabusSerializer(syllabuses, many=True)
    return Response(
        {"syllabuses": syllabusesSerializer.data},
        template_name="exams/links.html"
    )


@api_view(['GET', 'POST'])
@throttle_classes([ResourceThrottle])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def semester_API_view(request):

    semesters = Semester.objects.all()
    semesterSerializer = SemesterSerializer(semesters, many=True)
    return Response(
        semesterSerializer.data
    )



def study_dept_note_view(request):
    dept = Departments.objects.all()
    return render(request, "exams/deptnote.html", {"branches":dept})


@api_view(['GET'])
@throttle_classes([ResourceThrottle])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def study_note_view(request, branch_id):

    notes = StudyHandNote.objects.filter(branch=branch_id).all()
    notesSerializer = StudyNotesSerializer(notes, many=True)
    payload = notesSerializer.data
    if request.accepted_renderer.format == 'html':
        branch = Departments.objects.filter(pk=branch_id).first()
        return Response(
            {
                "branch": branch,
                "branch_id": branch_id,
            },
            template_name="exams/study_note.html",
        )
    return Response(payload)



@api_view(['GET'])
@throttle_classes([ResourceThrottle])
@renderer_classes([TemplateHTMLRenderer])
def priv_paper(request):
    return Response(template_name="exams/priv_paper.html")


@api_view(['GET'])
@throttle_classes([ResourceThrottle])
@renderer_classes([TemplateHTMLRenderer])
def revision_view(request):
    return Response(template_name="exams/revision.html")


def videoDept(request):
    branches = Departments.objects.all()
    return render(
        request,
        'exams/VidBranchs.html',
        {"branches": branches}
    )


@api_view(['GET'])
@throttle_classes([ResourceThrottle])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def vid_support_view(request, branch_id):
    video = StudyVideo.objects.filter(branch=branch_id).all()
    videoSerializer = StudyVideoSerializer(video, many=True)

    return Response(videoSerializer.data, template_name="exams/video.html")