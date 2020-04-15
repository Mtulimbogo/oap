from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
# from .models import *
from cv_registration import models
# from portal.cv_registration.models import *
from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render
from cv_registration import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.http import HttpResponseRedirect
# from django.core.files.storage import FileSystemStorage
# from django.core.files.storage import default_storage
# from django.conf import settings

# Create your views here.

# eGA organization homepage


def is_member(user):
    user_group = "main_staff"

    return user.groups.filter(name=user_group).exists()


@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def home(request):
    # User's name
    # user_firstname = request.user.first_name
    # print(user_firstname)
    # print(user_firstname)

    # Counting number of All applicants
    mzigo = models.applicant.objects.values_list(
        "id").filter(application_status='Submitted').order_by('id')
    # new_apl_list = models.applicant.objects.filter(id__in=mzigo).values()
    new_apl_count = models.applicant.objects.filter(id__in=mzigo).values().count()

    # Counting number of All Student applicants
    a = models.applicant.objects.values_list("id").filter(
        user__groups__name__in=["pt_student"]).filter(application_status='Submitted').order_by('id')
    student_apl = models.applicant.objects.filter(id__in=a).values().count()

    # Counting number of All non students applicants
    a = models.applicant.objects.values_list("id").filter(Q(user__groups__name__in=["mentors"]) | Q(
        user__groups__name__in=["researcher"])).filter(application_status='Submitted').order_by('id')
    non_student_apl_list = models.applicant.objects.filter(id__in=a).values().count()
    return render(request, "index.html", {"total_applicants_count": new_apl_count, "student_applicants_count": student_apl, "non_student_applicants_count": non_student_apl_list})


# @login_required(login_url='/accounts/login/')
# @user_passes_test(is_member, login_url='/accounts/login/')
# def dashboard(request):
#     mzigo = models.applicant.objects.values_list(
#         "id").filter(application_status='Submitted').order_by('id')
#     # new_apl_list = models.applicant.objects.filter(id__in=mzigo).values()
#     new_apl_count = models.applicant.objects.filter(id__in=mzigo).values().count()
#     print(new_apl_count)
#     return render(request, "index.html", {"total_applicants": new_apl_count})


# eGA organization - Add university page
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def add_university(request):
    return render(request, "add_university.html")


@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def insert_university_details(request):
    user_firstname = request.user.first_name
    if request.method == "POST":

        uni_data = models.university()
        uni_data.university_name = request.POST.get("university_name")
        uni_data.university_location = request.POST.get("university_location")
        uni_data.save()
        return render(request, "add_university.html", {"user_name": user_firstname})


@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def university_details(request):
    get_uni_data = models.university.objects.values_list()
    # get_uni = models.university.objects.values()
    # print(get_uni_data)
    # print(get_uni)
    # data = list(get_uni_data)
    # doc_header = "Railway Trains"
    link = "add_university"
    doc_para = "University Details"
    titles = ["S/No", "Name of University",
              "University Location", "Created On"]
    return render(request, "university_details.html", {"data": get_uni_data, "data_tiles": titles, "doc_para": doc_para, "link": link})


@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def add_university_agent(request):
    get_uni_data = models.university.objects.values_list("id", "university_name")
    # print(get_uni_data[0])
    return render(request, "university_agent.html", {"uni_names": get_uni_data})

# Saving details of university Details


@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def insert_agent_details(request):
    if request.method == "POST":

        agent_data = models.university_agent()
        agent_data.first_name = request.POST.get("first_name")
        agent_data.middle_name = request.POST.get("middle_name")
        agent_data.Last_name = request.POST.get("Last_name")
        agent_data.staff_id = request.POST.get("staff_id")
        agent_data.position = request.POST.get("position")
        agent_data.email = request.POST.get("email")
        agent_data.phone_no = request.POST.get("phone_no")
        # agent_data.university = request.POST.get("university")
        agent_data.university = models.university.objects.get(
            id=request.POST.get("university"))
        agent_data.save()
        return render(request, "university_agent.html")


@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def view_university_agent(request):
    get_agent_data = models.university_agent.objects.values_list(
        "id", "first_name", "middle_name", "Last_name", "staff_id", "position", "email", "phone_no", "university_id", "created_on")
    # get_aghgent_data = university_agent.objects.values()
    alldata = []

    # print(sensor)
    for index, values in enumerate(get_agent_data):
        mxi = []
        # print(list(values))
        universitydata = models.university.objects.filter(
            id=list(values)[8]).values_list("university_name")
        # traindata = train_detail.objects.filter(id=gateid.train_id).value_list("id")
        # print(universitydata)
        if len(universitydata) > 0:
            datavals = list(universitydata[0])
            # print(type(datavals))
            # print(datavals)
            mxi = list(values)
            mxi[8] = datavals[0]

            # print(mxi)
            # print(values.index)
        else:
            mxi = list(values)
        alldata.append(mxi)
        # print( alldata.append(mxi))
    # data = list(get_uni_data)
    # print(get_aghgent_data)
    link = "add_university_agent"
    doc_para = "University Agent Details"
    titles = ["S/N", "First Name", "Middle Name", "Last Name", "Staff ID", "Position", "Email",
              "Phone Number", "University Name", "Created On"]
    return render(request, "university_details.html", {"data": alldata, "data_tiles": titles, "doc_para": doc_para, "link": link})
    #   return render(request, "university_details.html")
# eGA organization - View applicant  page.


#
##############################################################################################################################
# view applicants to approve
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def approve_the_applicants(request):
    # new_apl_list = models.applicant_student.objects.values().filter(university_appvoment='Pending').order_by('id')

    mzigo = models.applicant_student.objects.values_list(
        "applicant_additional_id").filter(university_appvoment='Pending').order_by('id')
    new_apl_list = models.applicant.objects.filter(id__in=mzigo).values()

    paginator = Paginator(new_apl_list, 50)
    try:
        page_obj = paginator.page('page')
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "applicant.html", {'new_aplicants': page_obj})


# view approved student applicants
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def view_the_approved_applicants(request):
    the_applicants = models.applicant_student.objects.values_list(
        "applicant_additional_id").filter(university_appvoment='Approved').order_by('id')
    new_apl_list = models.applicant.objects.filter(id__in=the_applicants).values()

    paginator = Paginator(new_apl_list, 50)
    try:
        page_obj = paginator.page('page')
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "approved_applicant.html", {'approved_aplc': page_obj})
    # return NotImplementedError


# view un-approved student applicants
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def view_the_uni_unapproved_applicants(request):
    # un_apl = models.applicant.objects.values().filter(university_appvoment='DisApproved')
    the_applicants = models.applicant_student.objects.values_list(
        "applicant_additional_id").filter(university_appvoment='DisApproved').order_by('id')
    un_apl = models.applicant.objects.filter(id__in=the_applicants).values()

    paginator = Paginator(un_apl, 50)
    try:
        page_obj = paginator.page('page')
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "not_approved_applicant.html", {'disapproved_aplc': page_obj})


# view non students applicants
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def view_non_student(request):
    # the_applicants = models.applicant.objects.values_list(
    #     "id").filter(application_status='Submitted').order_by('id')
    # new_apl_list = models.applicant.objects.filter(id__in=the_applicants).values()

    # a = models.applicant.objects.filter(user__groups__name__in=["mentor", "researcher"])
    a = models.applicant.objects.values_list("id").filter(Q(user__groups__name__in=["mentors"]) | Q(
        user__groups__name__in=["researcher"])).filter(application_status='Submitted').order_by('id')
    new_apl_list = models.applicant.objects.filter(id__in=a).values()
    # a = models.applicant.objects.exclude(user__groups__name__in=["pt_student"])
    # print(a)
    # User.objects.filter(groups__name__in=['foo'])

    paginator = Paginator(new_apl_list, 50)
    try:
        page_obj = paginator.page('page')
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "non_student_applicants_list.html", {'approved_aplc': page_obj})
    # return NotImplementedError


@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def unprv_aplc(request, aplc_id):
    models.applicant_student.objects.filter(id=aplc_id).update(university_appvoment='DisApproved')

    # print("tumefika dar")
    # return redirect(single_page)
    return HttpResponseRedirect('ega_single_page/'+str(aplc_id))


@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def ega_accept_stdnt(request, aplc_id):
    models.applicant_student.objects.filter(id=aplc_id).update(university_appvoment='Approved')
    # print("tumefika dar")
    # return redirect(single_page)
    return HttpResponseRedirect('ega_single_page/'+str(aplc_id))


# More deatils of the applicant
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def ega_single_page(request, aplc_id):
    aplicant_id = aplc_id
    # print(aplicant_id)
    apl_details = models.applicant.objects.values().filter(id=aplicant_id)
    # apl_details = models.applicant.objects.values().filter(id=aplicant_id)
    apl_skills = models.skill.objects.values().filter(applicant_id=aplicant_id)
    apl_work_experience = models.work_experience.objects.values().filter(applicant_id=aplicant_id)
    apl_project = models.project.objects.values().filter(applicant_id=aplicant_id)
    apl_accademic = models.accademic.objects.values().filter(applicant_id=aplicant_id)

    student_prog_year = models.applicant_student.objects.values(
        'program', 'year_study').filter(applicant_additional=aplicant_id)
    approval_status = models.applicant_student.objects.values_list(
        "university_appvoment").filter(applicant_additional=aplicant_id)
    # print(student_prog_year)
    return render(request, "single_applicant_detail.html", {'details': apl_details,
                                                            'skilldetail': apl_skills,
                                                            'apl_work_experience': apl_work_experience,
                                                            'apl_accademic': apl_accademic,
                                                            'apl_project': apl_project,
                                                            'student_prog_year': student_prog_year,
                                                            'approval_status': list(approval_status)[0][0]})


# SEELECT APPLICANTS
#################################################################################################################
# View all applicants
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def view_applicants_all(request):
    # get_agent_data = university_agent.objects.values_list("first_name","middle_name","last_name","gender","phone_no","created_on")
    # data = list(get_uni_data)
    # new_apl_list = models.applicant_student.objects.values().filter(university_appvoment='Pending').order_by('id')

    mzigo = models.applicant.objects.values_list(
        "id").filter(application_status='Submitted').order_by('id')
    new_apl_list = models.applicant.objects.filter(id__in=mzigo).values()
    new_apl_count = models.applicant.objects.filter(id__in=mzigo).values().count()
    # print(new_apl_count)

    paginator = Paginator(new_apl_list, 50)
    try:
        page_obj = paginator.page('page')
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "applicant.html", {'new_aplicants': page_obj})


# Accept button and status change
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def accept_aplc(request, aplc_id):
    models.applicant_student.objects.filter(id=aplc_id).update(application_status='Accepted')

    return HttpResponseRedirect('applicant_single_page/'+str(aplc_id))

# Reject button and status change
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def reject_aplc(request, aplc_id):
    models.applicant.objects.filter(id=aplc_id).update(application_status='Rejected')

    # print("tumefika dar")
    # return redirect(single_page)
    return HttpResponseRedirect('applicant_single_page/'+str(aplc_id))


# The single page for any applicant to be accepted or rejected with the status "Submitted"
# More deatils of the applicant
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def applicant_single_page(request, aplc_id):
    aplicant_id = aplc_id
    # print(aplicant_id)
    apl_details = models.applicant.objects.values().filter(id=aplicant_id)
    # apl_details = models.applicant.objects.values().filter(id=aplicant_id)
    apl_skills = models.skill.objects.values().filter(applicant_id=aplicant_id)
    apl_work_experience = models.work_experience.objects.values().filter(applicant_id=aplicant_id)
    apl_project = models.project.objects.values().filter(applicant_id=aplicant_id)
    apl_accademic = models.accademic.objects.values().filter(applicant_id=aplicant_id)
    # check if the applicant is a student then fetch more details

    student_prog_year = models.applicant_student.objects.values(
        'program', 'year_study').filter(applicant_additional=aplicant_id)
    approval_status = models.applicant_student.objects.values_list(
        "university_appvoment").filter(applicant_additional=aplicant_id)
    try:
        approval_status_check = list(approval_status)[0][0]

    except IndexError:
        # student_prog_year = 'null'
        approval_status_check = 'Submitted'
    print(student_prog_year)
    return render(request, "more_applicant_detail.html", {'apl_details': apl_details,
                                                          'aplicant_skills': apl_skills,
                                                          'student_prog_year': student_prog_year,
                                                          'apl_work_experience': apl_work_experience,
                                                          'apl_accademic': apl_accademic,
                                                          'apl_project': apl_project,
                                                          'approval_status': approval_status_check
                                                          })

####################################################################################################################


# view list  of all student applicants
@login_required(login_url='/accounts/login/')
@user_passes_test(is_member, login_url='/accounts/login/')
def student_applicants_list(request):
    # the_applicants = models.applicant_student.objects.values_list(
    #     "applicant_additional_id").filter(university_appvoment='Approved').order_by('id')
    # new_apl_list = models.applicant.objects.filter(id__in=the_applicants).values()

    a = models.applicant.objects.values_list("id").filter(
        user__groups__name__in=["pt_student"]).filter(application_status='Submitted').order_by('id')
    new_apl_list = models.applicant.objects.filter(id__in=a).values()

    paginator = Paginator(new_apl_list, 50)
    try:
        page_obj = paginator.page('page')
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "student_applicants_list.html", {'approved_aplc': page_obj})
    # return NotImplementedError
    # return NotImplementedError


# view list  of all non student applicants
# def non_student_applicants_list(request):
#     return render(request, "non_student_applicants.html")
#     # return NotImplementedError


def table_trial(request):
    return render(request, "table.html")
