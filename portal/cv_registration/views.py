from django.core.mail import send_mass_mail
import pathlib
from uuid import uuid4
import os
from random import choice
from string import ascii_lowercase, digits
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from cv_registration import models
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
import clamd
User = get_user_model()


@login_required(login_url='/accounts/login/')
# @permission_required('polls.can_vote', raise_exception=True)
def personalinfo(request):
    if is_member(request.user, "pt_student"):
        type_of_applicant = {"applicant_group": "pt_student"}
    elif is_member(request.user, "researcher"):
        type_of_applicant = {"applicant_group": "researcher"}
    elif is_member(request.user, "mentor"):
        type_of_applicant = {"applicant_group": "mentor"}
    else:
        type_of_applicant = {"applicant_group": "staff"}

    if request.method == "GET":
        full_data = {}
        data = models.applicant.objects.filter(user=request.user.id).values()
        # TODO change it back to pt_student #done
        full_data = list(data)[0]
        if type_of_applicant["applicant_group"] == "pt_student":
            additional_data = models.applicant_student.objects.filter(
                applicant_additional_id=request.user.id).values()
            # print(additional_data)
            try:
                full_data.update(type_of_applicant)
                full_data.update(list(additional_data)[0])
            except IndexError:
                pass
        full_data = {k: "~" if not v else v for k, v in full_data.items()}
        # print(full_data)
        # models.applicant.objects
        full_data.update({"region_name": replace_region(full_data["region"])})
        # full_data["region"] = replace_region(full_data["region"])
        print(full_data)
        return render(request, 'personal_information.html', full_data)

    if request.method == "POST":

        user = User.objects.get(pk=request.user.id)

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('surname')

        applicant = models.applicant.objects.get(user=user)

        applicant.user = user

        if request.FILES.get('image_file') is not None:
            applicant.user_image = request.FILES.get('image_file')

        applicant.first_name = request.POST.get('first_name')
        applicant.middle_name = request.POST.get('middle_name')
        applicant.last_name = request.POST.get('surname')
        applicant.gender = request.POST.get('gender')
        applicant.email = request.POST.get('email')
        applicant.date_of_birth = request.POST.get('date_of_birth')
        applicant.nida_no = request.POST.get('nida')
        applicant.phone_no = request.POST.get('phone_number')
        applicant.region = request.POST.get('region')
        applicant.save()

        if type_of_applicant["applicant_group"] == "pt_student":

            app_stu = models.applicant_student.objects.get(
                applicant_additional_id=request.user.id)
            app_stu.program = request.POST.get('program')
            app_stu.year_study = request.POST.get("year_study")
            app_stu.student_registration_no = request.POST.get("student_id")
            app_stu.save()

        full_data = get_applicant_data(request.user.id, type_of_applicant)
        return render(request, 'personal_information.html', full_data)
    return render(request, 'personal_information.html', type_of_applicant)


@login_required(login_url='/accounts/login/')
def work_experience(request):
    applicant_instance = models.applicant.objects.get(user=request.user)
    work_data = models.work_experience.objects.filter(applicant=applicant_instance).values_list(
        "job_title", "company_name", "start_date", "end_date")

    # print(list(work_data)[0])

    # TODO make the edit as well as delete work...

    return render(request, "work_experience.html", {"applicant_work_data": list(work_data), "tooltip_edit": "Edit Work Experience", "tooltip_delete": "Delete Work Experience"})
    # return render(request, "work_experience.html")

    # if request.method == "POST": #TODO will be used for the edit and delete portions.


@login_required(login_url='/accounts/login/')
def add_work_experience(request):
    applicant_instance = models.applicant.objects.get(user=request.user)
    # if request.method == "GET":

    if request.method == "POST":

        experience = models.work_experience()
        experience.applicant = applicant_instance
        experience.company_name = request.POST.get("institution_name")
        experience.start_date = request.POST.get("start_date")
        experience.end_date = request.POST.get("end_date")
        experience.job_title = request.POST.get("job_title")
        experience.save()
        work_data = models.work_experience.objects.filter(applicant=applicant_instance).values_list(
            "job_title", "company_name", "start_date", "end_date")

        print(list(work_data))

        # data = {v:k for v,k in enumerate(list(work_data))}
        # print(data)
        return render(request, "work_experience.html", {"applicant_work_data": list(work_data)})
    # print(models.work_experience.objects.all())
    if request.method == "GET":
        return render(request, "add_work_experience.html")
    return render(request, "work_experience.html",)


@login_required(login_url='/accounts/login/')
def skills_work(request):
    applicant_instance = models.applicant.objects.get(user=request.user)
    skill_data = models.skill.objects.filter(applicant=applicant_instance).values_list(
        "skill_name", "level", "explaination")
    print(skill_data)
    print(User.objects.filter(groups__name='pt_student'))
    return render(request, "skills_work.html", {"skills_work_data": list(skill_data)})


@login_required(login_url='/accounts/login/')
def add_skills(request):
    applicant_instance = models.applicant.objects.get(user=request.user)
    if request.method == "POST":
        skill = models.skill()
        skill.applicant = applicant_instance
        skill.level = request.POST.get("skill_level")
        skill.skill_name = request.POST.get("skill_type")
        skill.explaination = request.POST.get("brief")
        skill.save()

        print(models.skill.objects.filter(
            applicant=applicant_instance).values())
        return redirect(skills_work)

    return render(request, "add_skills.html")


@login_required(login_url='/accounts/login/')
def education(request):
    applicant_instance = models.applicant.objects.get(user=request.user)
    edu_data = models.accademic.objects.filter(applicant=applicant_instance).values_list(
        "reward", "institution", "year_started", "year_finished")
    print(edu_data)
    return render(request, "educational_bg.html", {"education_data": edu_data})


@login_required(login_url='/accounts/login/')
def add_education(request):
    applicant_instance = models.applicant.objects.get(user=request.user)
    if request.method == "POST":
        academic_bg = models.accademic()
        academic_bg.applicant = applicant_instance
        academic_bg.institution = request.POST.get("institution")
        academic_bg.year_started = request.POST.get("start_date")
        academic_bg.year_finished = request.POST.get("end_date")
        academic_bg.reward = request.POST.get("education_level")
        academic_bg.save()
        print(academic_bg)
    return render(request, "add_education.html")


@login_required(login_url='/accounts/login/')
def contact_details(request):
    return render(request, "contact_details.html")

def rename_dict(d, k):
    if k in d:
        return d[k]

@login_required(login_url='/accounts/login/')
def view_attachments(request):
    # print("nipo attachement...")
    applicant_instance = models.applicant.objects.get(user=request.user)
    attachment_data = models.attachment.objects.filter(applicant=applicant_instance, status=True).values_list(
         "id", "attachment_type", "last_update")
    print(attachment_data)

    d = {
        "CV":"CV",
        "motivation":"Motivation statement",
        "nida":"NIDA",
        "nomination_letter":"Nomination letter",
        "project_references":"Project references",
        "reference_letter":"Reference Letter",
        "research_contributions":"Research contributions",
        "research_proposal":"Research Proposal",
        "university_transcript":"University Transcript",
        "other":"Other"
    }
    
    result = []
    for p in list(attachment_data):
        a = [p[0]] 
        res = rename_dict(d,p[1])
        a = [p[0],res,p[2]]
        result.append(a)
    print(result)

    return render(request, "attach.html", {"attachment_data": list(result), "page_title":"Attachments", "tool_tip_add":"Add Attachment","redirection_location":"add_attachments"})

@login_required(login_url='/accounts/login/')
def add_attachments(request):
    if request.method == "POST" and request.FILES['attachment']:
        user_id = request.user.id
        for f in request.FILES.getlist('attachment'):
            if clean_attachment(request, user_id, f):

                ext = f.name.split('.')[-1]
                file_name = "attachment_" + " {} ".format(int(user_id)) \
                    + "_ " \
                    + " {}.{}".format(uuid4().hex, ext)\


                user_dir = "user_" + str(user_id)

                save_path = os.path.join(settings.MEDIA_ROOT, user_dir)
                pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
                file_path = os.path.join(save_path, file_name)
                try:
                    save_file(f, file_path)
                    att = models.attachment()
                    # att.attachment_name = request.POST['attachname']
                    att.path_to_file = file_path
                    att.attachment_type = request.POST["attachment_type"]
                    att.applicant_id = models.applicant.objects.get(user=request.user).id
                    att.status = True
                    att.save()  
                    if request.method == "POST" and request.FILES['attachment']:
                        messages.success(request,"Attachment saved Successfully")     
                except Exception as e:
                    
                    messages.error(request,"There was a technical error, your attachment couldnt be saved")
                    print(e)      
            else:
                
                messages.error(
                request, "Your Attachment was found to have a virus. Please scan your attachments before uploading")
                return redirect(add_attachments)
        return redirect(view_attachments)
    return render(request, "attachments.html", {'pagename': "Add Attachments", "tool_tip_back":"View Attachments", "redirection_location":"view_attachments", "page_title":"Attachments"})


NORMAL_HEADER = 'Virus Found in Submitted Attachment'
ADMIN_HEADER = "A USER HAS UPLOADED A POTENTIALLY MALICIOUS ATTACHMENT"
ADMIN_EMAIL = "admin@eganet.go.tz"
CD = clamd.ClamdUnixSocket()

def clean_attachment(request, request_user_id, file):
    # print(request.FILES.getlist())
    for f in request.FILES.getlist('attachment'):
        
        # scan stream
        scan_results = CD.instream(f)
        print(scan_results)
        if (scan_results['stream'][0] == 'OK'): # TODO  change back 
            return True
        elif (scan_results['stream'][0] == 'FOUND'):
            # print("kirusi COVID19!!!!!!")
            infecting_user = User.objects.get(pk=request_user_id)
            ADMIN_SUBJECT = "The user {} {} with email {} has submitted the following file ' \
            'flagged as containing a virus: \n\n {} ".format(infecting_user.first_name, infecting_user.last_name, infecting_user.email,
                                                                f.name)
            USER_SUBJECT = "Your Attachment was found to be with a virus. \n\n Please upload virus-free attachments.  \
                \n\n\n Operations Officer, \n admin@eganet.go.tz "
            infecting_user_mail = (NORMAL_HEADER, USER_SUBJECT, "noreply@eganet.go.tz", [str(infecting_user.email)])
            admin_user_mail = (ADMIN_HEADER, ADMIN_SUBJECT, "noreply@eganet.go.tz", ["admin@eganet.go.tz"])
            
            # TODO make it true later in production
            send_mass_mail((infecting_user_mail, admin_user_mail), fail_silently=settings.FAIL_SILENTLY)
            return False
    return False

def additional_attachments(request):
    if request.method == 'POST' and request.FILES['filename']:
        user_id = request.user.id

        # infected_files = []
        cd = clamd.ClamdUnixSocket()  # TODO install clamd on unix os

        for f in request.FILES.getlist('filename'):
            # scan stream

            scan_results = cd.instream(f)
            print(scan_results)
            if (scan_results['stream'][0] == 'OK'): # TODO  change back 
            # if (scan_results['stream'][0] == 'FOUND'): # TODO delete line
                # start to create the file name
                ext = f.name.split('.')[-1]
                file_name = "attachment_" + " {} ".format(int(user_id)) \
                    + "_ " \
                    + " {}.{}".format(uuid4().hex, ext)\


                user_dir = "user_" + str(user_id)

                save_path = os.path.join(settings.MEDIA_ROOT, user_dir)
                pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
                file_path = os.path.join(save_path, file_name)
                # path = default_storage.save(save_path, request.FILES['filename'])
                save_file(f, file_path)

                attachname = request.POST['attachname']

                att = models.attachment()
                att.attachment_name = attachname
                att.path_to_file = file_path
                att.applicant_id = models.applicant.objects.get(user=request.user).id
                att.save()
                return render(request, "attachments.html", {'pagename': "Attachments Needed"})
            elif (scan_results['stream'][0] == 'FOUND'):
                # print("kirusi COVID19!!!!!!")
                print(f.name)
                infecting_user = User.objects.get(pk=request.user.id)
                ADMIN_SUBJECT = "The user {} {} with email {} has submitted the following file '{}' flagged as containing a virus: ".format(infecting_user.first_name, infecting_user.last_name, infecting_user.email,
                                                                 f.name)
                USER_SUBJECT = "Your Attachment was found to be with a virus. \n\n Please upload virus-free attachments.  \
                    \n\n\n Operations Officer, \n admin@eganet.go.tz "
                infecting_user_mail = (NORMAL_HEADER, USER_SUBJECT, "noreply@eganet.go.tz", [str(infecting_user.email)])
                admin_user_mail = (ADMIN_HEADER, ADMIN_SUBJECT, "clamd_scanner@eganet.go.tz", ["admin@eganet.go.tz"])
                messages.error(
                    request, "Your Attachment was found to have a virus. Please scan your attachments before uploading")
                # TODO make it true later in production
                send_mass_mail((infecting_user_mail, admin_user_mail), fail_silently=settings.FAIL_SILENTLY)
            return render(request, "attachments.html", {'pagename': "Attachments Needed"})
    return render(request, "attachments.html", {'pagename': "Attachments Needed"})


def save_file(file, filename):
    with open(filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)



# def additional_attachments(request):
#     if request.method == 'POST' and request.FILES['filename']:
#         save_path = os.path.join(settings.MEDIA_ROOT, str(request.FILES['filename']))
#         path = default_storage.save(save_path, request.FILES['filename'])

#         myfile = str(default_storage.path(path))
#         attachname = request.POST['attachname']

#         att = models.attachments()
#         att.attachment_name = attachname
#         att.path_to_file = myfile
#         att.applicant_id = request.session['id']
#         att.save()

#         messages.success(request, "Record saved successfully")
#         return redirect('attachment')

#     h = "True"
#     return render(request, '../htmls/application/attachments.html', {'pagename': "Attachments Needed"})


def cv_edit_skill_single_page(request, aplc_id):
    applicant_instance = models.applicant.objects.get(user=request.user)
    skill_data = models.skill.objects.filter(applicant=applicant_instance).values_list(
        "skill_name", "level", "explaination")
    aplc_id

    return NotImplementedError


def is_member(user, user_group):
    return user.groups.filter(name=user_group).exists()


def is_in_multiple_groups(user, groups):
    return user.groups.filter(name__in=groups).exists()


def replace_region(region_id):
    try:
        return regions[region_id]
    except KeyError:
        return "--Select--"


regions = {
    "23": "Arusha",
    "24": "Dar es Salaam",
    "1": "Dodoma",
    "11": "Geita",
    "2": "Iringa",
    "3": "Kagera",
    "12": "Katavi",
    "4": "Kigoma",
    "5": "Kilimanjaro",
    "6": "Lindi",
    "7": "Manyara",
    "8": "Mara",
    "9": "Mbeya",
    "14": "Morogoro",
    "15": "Mtwara",
    "16": "Mwanza",
    "10": "Njombe",
    "26": "Pemba Kaskazini",
    "27": "Pemba Kusini",
    "17": "Pwani",
    "18": "Rukwa",
    "25": "Ruvuma",
    "19": "Shinyanga",
    "13": "Simiyu",
    "20": "Singida",
    "31": "Songwe",
    "21": "Tabora",
    "22": "Tanga",
    "28": "Zanzibar Kati/Kusini ",
    "29": "Zanzibar Mjini Kaskazini",
    "30": "Zanzibar Mjini Magharibi",
}


def get_applicant_data(user_ID, type_of_applicant):
    full_data = {}
    data = models.applicant.objects.filter(user=user_ID).values()
    full_data = list(data)[0]
    print(data)
    # TODO change it back to pt_student #done
    if type_of_applicant["applicant_group"] == "pt_student":
        additional_data = models.applicant_student.objects.filter(
            applicant_additional_id=user_ID).values()
        # print(additional_data)
        try:
            # full_data = list(data)[0]
            full_data.update(type_of_applicant)
            full_data.update(list(additional_data)[0])
        except IndexError:
            pass
    full_data = {k: "~" if not v else v for k, v in full_data.items()}

    full_data.update({"region_name": replace_region(full_data["region"])})

    return full_data

# @user_passes_test(is_in_multiple_groups) --> this decorator enables users of a particular
# type to enter a view...
# https://stackoverflow.com/questions/4789021/in-django-how-do-i-check-if-a-user-is-in-a-certain-group

# additonal
# https://stackoverflow.com/questions/45782054/how-can-i-make-a-specific-login-for-specific-group-with-djangos-authenticate


# def _identify_academic_reward():
#     {
#         "":"PHd"
#     }
