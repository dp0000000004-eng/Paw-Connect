from django.urls import path
from . import views

app_name = "exam"

urlpatterns = [
    path('dept/', views.departments, name="branch"),
    path('link/<int:branch_id>', views.syllabus, name="syllabus"),
    path('semi/', views.semester_API_view),
    path('note-dept/', views.study_dept_note_view, name="dept_note"),
    path('study-note/<int:branch_id>', views.study_note_view, name="study_note"),
    # path('study-note/<int:branch_id>/data.xml', views.study_note_data_view, name="study_note_data"),
    path('priv-paper/', views.priv_paper, name="priv_paper"),
    path('revision-support/', views.revision_view, name="revision_view"),
    path('vid-dept/', views.videoDept, name="vid_dept"),
    path('video-support/<int:branch_id>', views.vid_support_view, name="vid_support_view"),
]
