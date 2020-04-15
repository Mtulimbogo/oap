from django.conf.urls import url, include
from portal.university_regulator import views

urlpatterns = [
    url('home', views.home, name = "university_homepage"),
    url('approve_applicants', views.approve_apl, name="approve_applicants"),
    url('view_approved_applicants', views.view_approved,
        name="view_approved_applicants"),
    url('view_unapproved_applicants', views.view_unapproved,
        name="view_unapproved_applicants"),
    url('applicant', views.applicants_list, name="applicant"),
    url('complited_students', views.complited_students, name="complited_students"),
    url('ongoing_students', views.ongoing_students, name="ongoing_students"),

    # # Handle applications
    url('single_page/(?P<aplicant_id>\d+)/$', views.single_page, name = "single_page"),
    url('aprove_stdnt/(?P<aplc_id>\d+)/$', views.aprv_aplc, name = "aprove_stdnt"),
    url('revork_stdnt/(?P<aplc_id>\d+)/$', views.unprv_aplc, name="revork_stdnt"),
    # url('single_page', views.single_page), (?P<aplc_id>\d+)/$
]
