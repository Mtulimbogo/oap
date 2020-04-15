
from django.urls import path
from portal.cv_registration import views
urlpatterns = [
    path("", views.personalinfo),
    path("newgate", views.personalinfo, name="dashboard"),
    path("dashboard", views.personalinfo, name="dashboard"),
    path("work_experience", views.work_experience, name="work_experience"),
    path("add_work_experience", views.add_work_experience, name="add_work_experience"),
    path("skills_work", views.skills_work, name="skills_work"),
    path("add_skills", views.add_skills, name="add_skills"),
    path("education", views.education, name="education"),
    path("add_education", views.add_education, name="add_education"),
    path('contact_details', views.contact_details, name="contact_details"),
    path('additional_attachments', views.additional_attachments, name="additional_attachments")
]
