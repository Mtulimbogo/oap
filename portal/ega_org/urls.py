from django.urls import path
from django.conf.urls import url
from portal.ega_org import views

urlpatterns = [
    #University details
    # path('', views.dashboard), 
    # path('ega_home', views.home), #Home page
    path('', views.home, name="ega"), #Home page
    path('add_university', views.add_university, name="add_university"), #reDirects to add university fORM PAGE
    path('insert_university_details', views.insert_university_details, name="INSERT UNIVERSITY DATA TO DB"), #INSERT UNIVERSITTY DETAILS TO DB
    # path('add_university_details', views.university_details, name="add_university_details"),
    path('add_university_agent', views.add_university_agent, name="add_university_agent"),
    path('insert_university_agent', views.insert_agent_details, name="INSERT UNIVERSITY AGENT DATA"),
    path('view_university_agent', views.view_university_agent, name="view_university_agent"),
    path('university_details', views.university_details, name="university_details"),
    # path('approve_the_applicants', views.approve_the_applicants, name="approve_the_applicants"), #approve_the_applicants from university
    path('view_the_uni_approved_applicants', views.view_the_approved_applicants, name="view_the_uni_approved_applicants"), #View all students approved/Accepted by the university Agent
    path('view_the_uni_unapproved_applicants', views.view_the_uni_unapproved_applicants, name="view_the_uni_unapproved_applicants"), #View all Non-students Disapproved/Rejected by the university Agent
        #RE-APPROVE OR RE-DISAPPROVE THE STUDENT FROM THE UNIVERSITY DECISION 
    # path('decision_to_stdnt/(?P<int:aplc_id>)/$ ', views.unprv_aplc, name="decision_to_stdnt"),
    # url('decision_to_stdnt/(?P<aplc_id>\d+)/$', views.unprv_aplc, name="decision_to_stdnt"),
    url('ega_accept_stdnt/(?P<aplc_id>\d+)/$', views.ega_accept_stdnt, name="ega_accept_stdnt"),
    url('ega_revoke_stdnt/(?P<aplc_id>\d+)/$', views.unprv_aplc, name="ega_revoke_stdnt"),
    #Viewing More details of the applicant
    url('ega_single_page/(?P<aplc_id>\d+)/$', views.ega_single_page, name="ega_single_page"), 
    #path('view_non_student', views.view_non_student, name="view_the_approved_applicants"),

    #SELECT APPLICANTS
    path('view_applicants_all', views.view_applicants_all, name="view_applicants_all"), #VIEW ALL APPLICANTS
    path('student_applicant', views.student_applicants_list, name="student_applicant"), #VIEW STUDENT APPLICANT
    path('non_student_applicant', views.view_non_student, name="non_student_applicant"), #VIEW NON STUDENT APPLICANT
    url('accept_aplc/(?P<aplc_id>\d+)/$', views.accept_aplc, name="accept_aplc"), #ACCEPT BUTTON
    url('reject_aplc/(?P<aplc_id>\d+)/$', views.reject_aplc, name="reject_aplc"), #REJECT BUTTON
    # url('accept_aplc', views.accept_aplc, name="accept_aplc"), #ACCEPT BUTTON
    # url('reject_aplc', views.reject_aplc, name="reject_aplc"), #REJECT BUTTON
    url('applicant_single_page/(?P<aplc_id>\d+)/$', views.applicant_single_page, name="applicant_single_page"), #MORE DETAILS OF THE APPLICANT

    url('table_trial', views.table_trial, name="table_trial"), #VIEW ALL APPLICANTS



    

   


    #Applicant results
]
