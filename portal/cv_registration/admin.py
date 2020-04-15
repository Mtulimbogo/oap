from django.contrib import admin
from cv_registration import models
admin.site.register(models.accademic)
admin.site.register(models.applicant)
admin.site.register(models.applicant_student)
admin.site.register(models.project)
admin.site.register(models.attachment)
admin.site.register(models.skill)
admin.site.register(models.work_experience)
admin.site.register(models.university)
admin.site.register(models.university_agent)  # Register your models here.
