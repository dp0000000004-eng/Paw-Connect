from django.urls import path
from . import views

app_name = "exam"

urlpatterns = [
    path('dept/', views.departments, name="branch"),
    path('link/<int:branch_id>', views.syllabus, name="syllabus"),
    path('semi/', views.semester_API_view),
    path('study-note/', views.study_note_view, name="study_note"),
    path('priv-paper/', views.priv_paper, name="priv_paper"),
    path('revision-support/', views.revision_view, name="revision_view"),
    path('video-support/', views.vid_support_view, name="vid_support_view"),
]