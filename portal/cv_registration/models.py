# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from portal.users.models import User as abstract_user
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# from acc.models import CustomUser
# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # the filename generates a 16bit uuid for the filename
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class university(models.Model):
    university_name = models.CharField(max_length=60)
    university_location = models.CharField(max_length=60, null=True)
    created_on = models.DateTimeField(auto_now=True, null=True)

    # def __init__(self, *arg):
    #     super(university, self).__init__()
    #     self.arg = arg

    class Meta:
        app_label = 'cv_registration'
    #     abstract = False

    def __str__(self):
        return self.university_name


class applicant(models.Model):
    # models.OneToOneField("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    user = models.OneToOneField(abstract_user, verbose_name=(
        "user"), on_delete=models.CASCADE, null=True)
    # user = models.Forei(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=40)
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    gender = models.CharField(max_length=6)
    nida_no = models.CharField(max_length=25)
    phone_no = models.CharField(max_length=22)
    created_on = models.DateTimeField(auto_now_add=True)
    # user_image = models.ImageField(_("user_image"), upload_to=user_directory_path, height_field=None,
    #                                width_field=None, max_length=None, null=True, default='11.jpg')
    user_image = ProcessedImageField(upload_to=user_directory_path,
                                     processors=[ResizeToFill(128, 128)],
                                     format='JPEG',
                                     options={'quality': 90}, null=True, default='11.jpg')
    region = models.CharField(max_length=22)
    APPROVED = 'Approved'
    DISAPPROVED = 'DisApproved'
    PENDING = 'Pending'
    SUBMITTED = 'Submitted'

    APPROVAL_CHOICES = [
        (APPROVED, 'Approved'),
        (DISAPPROVED, 'DisApproved'),
        (PENDING, 'Pending'),
        (SUBMITTED, 'Submitted'),
    ]
    application_status = models.CharField(max_length=14, choices=APPROVAL_CHOICES,
                                          default=PENDING)
    # TODO move to applicant student.  #@done

    approved_on = models.DateTimeField(default=timezone.now)
    rank_level = models.IntegerField(default=0)
    date_of_birth = models.DateField(null=True)

    # def __init__(self, *arg):
    #     super(applicant, self).__init__()
    #     self.arg = arg

    def __str__(self):
        return str(self.user.username)

    def get_data(self):
        return (
            {
                "id": self.id,
                "email": self.email,
                "first_name": self.first_name,
                "middle_name": self.middle_name,
                "last_name": self.last_name,
                "gender": self.gender,
                "nida_no": self.nida_no,
                "phone_no": self.phone_no
            }
        )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            applicant.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.applicant.save()


# Added username and password that shall enable university agent to login


class university_agent(models.Model):
    # applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, default="")
    Last_name = models.CharField(max_length=40)
    staff_id = models.CharField(max_length=20)
    position = models.CharField(max_length=25)
    email = models.EmailField(max_length=25)
    phone_no = models.CharField(max_length=22)
    university = models.ForeignKey(university, on_delete=models.CASCADE)
    username = models.CharField(max_length=40, default="")
    password = models.CharField(max_length=40, default="")
    created_on = models.DateTimeField(auto_now_add=True)
    user_image = models.ImageField(_("user_image"), upload_to=user_directory_path, height_field=None,
                                   width_field=None, max_length=None, null=True)

    # {}
    # def __init__(self, *arg):
    #     super(university_agent, self).__init__()
    #     self.arg = arg

    def __str__(self):
        return (self.first_name + str(" ") + str(self.staff_id))

#check on commented values to be added
class work_experience(models.Model):
    applicant = models.ForeignKey(applicant, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=75)
    job_title = models.CharField(max_length=60)
    # JOb description -
    # applicant = models.ForeignKey(applicant, on_delete=models.CASCADE)
    # Supervisor' contacts -
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)

    # def __init__(self, *arg):
    #     super(work_experience, self).__init__()
    #     self.arg = arg


class skill(models.Model):
    skill_name = models.CharField(max_length=50)
    applicant = models.ForeignKey(applicant, on_delete=models.CASCADE)
    level = models.CharField(max_length=75)
    explaination = models.CharField(max_length=250, null=True)

    def __str__(self):
        return (self.skill_name + str(self.applicant_id) + str(self.id))


class attachment(models.Model):

    CV="CV"
    motivation="Motivation statement"
    nida="NIDA"
    nomination_letter="Nomination letter"
    project_references="Project references"
    reference_letter="Reference Letter"
    research_contributions="Research contributions"
    research_proposal="Research Proposal"
    university_transcript="University Transcript"
    other="Other"

    
    
    ATTACHMENT_CHOICES = [
        (CV,"CV"),
        (motivation,"Motivation Statement"),
        (nida,"NIDA"),
        (nomination_letter,"nomination_letter"),
        (project_references,"Project References"),
        (reference_letter,"Reference Letter"),
        (research_contributions,"Research Contributions"),
        (research_proposal,"research_proposal"),
        (university_transcript,"university_transcript"),
        (other,"Other"),
    ]

    # attachment_name = models.CharField(max_length=50)
    applicant = models.ForeignKey(applicant, on_delete=models.CASCADE)
    path_to_file = models.CharField(max_length=255)
    last_update = models.DateTimeField(auto_now_add=True)
    attachment_type = models.CharField(max_length=14, choices=ATTACHMENT_CHOICES,
                                            default=other)
    status = models.BooleanField(default=True)

    def __str__(self):
        return (self.attachment_type+ "_" + str(self.last_update))
        # return (self.attachment_name + str(self.id))


class application(models.Model):
    application_type = models.IntegerField()
    applicant = models.ForeignKey(
        applicant, on_delete=models.CASCADE, null=True)
    # if application status is 1 ==> sent
    application_status = models.IntegerField()

    created_on = models.DateTimeField(auto_now_add=True)

    def __init__(self, *arg):
        super(application, self).__init__()
        self.arg = arg


class accademic(models.Model):
    applicant = models.ForeignKey(applicant, on_delete=models.CASCADE)
    # Education level - to be added i.e Degree / A-level / O-level
    # Programme  - Bsc. / Science /
    institution = models.CharField(max_length=50)
    reward = models.CharField(max_length=50)
    # Attachement -
    year_started = models.DateField(auto_now=False, auto_now_add=False)
    year_finished = models.DateField(
        auto_now=False, auto_now_add=False, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.applicant.first_name + str("_") + self.applicant.last_name + str("_") + str(self.created_on))


class project(models.Model):
    applicant = models.ForeignKey(applicant, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=50)
    Link = models.CharField(max_length=400)
    role = models.CharField(max_length=50)
    yeard = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __init__(self, *arg):
        super(project, self).__init__()
        self.arg = arg


class applicant_student(models.Model):

    APPROVED = 'Approved'
    DISAPPROVED = 'DisApproved'
    PENDING = 'Pending'
    NOT_SUBMITTED = "not_submitted"
    APPROVAL_CHOICES = [
        (APPROVED, 'Approved'),
        (DISAPPROVED, 'DisApproved'),
        (PENDING, 'Pending'),
        (NOT_SUBMITTED, "not_submitted"),
    ]

    applicant_additional = models.OneToOneField(
        abstract_user, on_delete=models.CASCADE, null=True)
    university = models.ForeignKey(
        university, on_delete=models.CASCADE, null=True)
    university_agent = models.ForeignKey(
        university_agent, on_delete=models.CASCADE, null=True
    )
    university_appvoment = models.CharField(max_length=14, choices=APPROVAL_CHOICES,
                                            default=NOT_SUBMITTED)
    program = models.CharField(max_length=50)
    year_study = models.CharField(max_length=50)
    recommendation = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    student_registration_no = models.CharField(max_length=50, null=False)

    # def __init__(self, *arg):
    #     super(applicant_student, self).__init__()
    #     self.arg = arg

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         applicant_student.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.applicant_student.save()


# class university_Personal(models.Model):
#     parsonal_university=models.ForeignKey(Univesity, on_delete=models.CASCADE)
#     firstname=models.CharField(max_length=60)
#     lastname=models.CharField(max_length=60)
#     parsonal_position=models.CharField(max_length=60)
#     parsonal_email=models.EmailField(max_length=70)
#     parsonal_phone=models.CharField(max_length=13)
#     parsonal_password=models.CharField(max_length=70)
#     staff_id=models.CharField(max_length=20)
#     def __init__(self, *arg):
#         super(university_Personal, self).__init__()
#         self.arg = arg
