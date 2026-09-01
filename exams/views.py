
from django.shortcuts import render
from .models import Syllabus, Semester
from accounts.models import Departments


def departments(request):

    branches = Departments.objects.all()

    return render(
        request,
        'exams/branchs.html',
        {
            "branches": branches
        }
    )


def syllabus(request, branch_id):
    # Only syllabus records that belong to this department / branch
    syllabuses = Syllabus.objects.filter(branch=branch_id)

    return render(
        request,
        'exams/links.html',
        {
            "syllabuses": syllabuses
        }
    )
