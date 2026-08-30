from django.shortcuts import render
from .models import Syllabus, Semester
from accounts.models import Departments

# Create your views here.


def departments(request):

    branches = Departments.objects.all()

    return render(
        request,
        'exams/branchs.html',
        {
            "branches":branches
        }
    )



def syllabus(request, branch_id):
    syllabuses = Syllabus.objects.filter(branch=branch_id)

    print(syllabus)

    return render(
        request,
        'exams/links.html',
        {
            "syllabuses":syllabuses
        }
    )