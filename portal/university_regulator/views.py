# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from cv_registration import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.http import HttpResponseRedirect
# Create your views here.
from django.core.mail import send_mail


def home(request):

    return render(request, "Home.html")
    # return NotImplementedError


def view_unapproved(request):
    # un_apl = models.applicant.objects.values().filter(university_appvoment='DisApproved')
    the_applicants = models.applicant_student.objects.values_list(
        "applicant_additional_id").filter(university_appvoment='DisApproved').order_by('id')
    un_apl = models.applicant.objects.filter(id__in=the_applicants).values()
    print(un_apl)
    print(the_applicants)
    paginator = Paginator(un_apl, 50)
    try:
        page_obj = paginator.page('page')
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "not_approved_applicants.html", {'disapproved_aplc': page_obj})

    # return NotImplementedError


def approve_apl(request):
    # new_apl_list = models.applicant_student.objects.values().filter(university_appvoment='Pending').order_by('id')

    mzigo = models.applicant_student.objects.values_list(
        "applicant_additional_id").filter(university_appvoment='Pending').order_by('id')
    new_apl_list = models.applicant.objects.filter(user_id__in=mzigo).values()
    print("applicants to approve::")
    print(mzigo)
    print(new_apl_list)
    paginator = Paginator(new_apl_list, 50)
    try:
        page_obj = paginator.page('page')
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "applicants.html", {'new_aplicants': page_obj})

    # return render (request, "applicants.html",{'new_aplicants':new_apl_list})

    # return NotImplementedError


def view_approved(request):
    the_applicants = models.applicant_student.objects.values_list(
        "applicant_additional_id").filter(university_appvoment='Approved').order_by('id')
    print(the_applicants[0])
    new_apl_list = models.applicant.objects.filter(id__in=the_applicants).values()

    print(new_apl_list)
    paginator = Paginator(new_apl_list, 50)
    try:
        page_obj = paginator.page('page')
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "approved_applicants.html", {'approved_aplc': page_obj})
    # return NotImplementedError


def applicants_list(request):
    return render(request, "applicants.html")
    # return NotImplementedError


def complited_students(request):
    return render(request, "Complited_Students.html")
    # return NotImplementedError


def ongoing_students(request):
    return render(request, "Ongoing_Students.html")


def single_page(request, aplicant_id):
    apl_details = models.applicant.objects.values().filter(id=aplicant_id)
    apl_skills = models.skill.objects.values().filter(applicant_id=aplicant_id)

    student_prog_year = models.applicant_student.objects.values(
        'program', 'year_study').filter(applicant_additional=aplicant_id)
    approval_status = models.applicant_student.objects.values_list(
        "university_appvoment").filter(applicant_additional=aplicant_id)
    print(approval_status)
    return render(request, "single_applicant.html", {'details': apl_details,
                                                     'skilldetail': apl_skills,
                                                     'student_prog_year': student_prog_year, })


def aprv_aplc(request, aplc_id):
    models.applicant_student.objects.filter(id=aplc_id).update(university_appvoment='Approved')

    return HttpResponseRedirect('university/single_page/'+str(aplc_id))


def unprv_aplc(request, aplc_id):
    models.applicant_student.objects.filter(id=aplc_id).update(university_appvoment='DisApproved')
    return HttpResponseRedirect('university/single_page/'+str(aplc_id))


def send_applicant_mail(applicant, position):
    """
    position: the position the applicant requested.
    Applicant:  Full Name of applicant in form "first_name" __ "middle_name" __ "last_name"
    """
    subject = "eGA-RIDC" + position + "Application"
