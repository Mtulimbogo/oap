# backend/management/commands/initgroups.py
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

from cv_registration import models

GROUPS_PERMISSIONS = {
    'mentors': {
        models.university: ['add', 'change', 'delete', 'view'],
        models.applicant: ['add', 'change', 'delete', 'view'],
        models.work_experience: ['add', 'change', 'delete', 'view'],
        models.attachment: ['add', 'change', 'delete', 'view'],
        models.skill: ['add', 'change', 'delete', 'view'],
        models.project: ['add', 'change', 'delete', 'view'],
        models.work_experience: ['add', 'change', 'delete', 'view'],
    },
    'pt_student': {
        models.university: ['add', 'change', 'delete', 'view'],
        models.applicant: ['add', 'change', 'delete', 'view'],
        models.work_experience: ['add', 'change', 'delete', 'view'],
        models.attachment: ['add', 'change', 'delete', 'view'],
        models.skill: ['add', 'change', 'delete', 'view'],
        models.project: ['add', 'change', 'delete', 'view'],
        models.applicant_student: ['add', 'change', 'delete', 'view'],
        models.work_experience: ['add', 'change', 'delete', 'view'],
    },
    'researcher': {
        models.university: ['add', 'change', 'delete', 'view'],
        models.applicant: ['add', 'change', 'delete', 'view'],
        models.work_experience: ['add', 'change', 'delete', 'view'],
        models.attachment: ['add', 'change', 'delete', 'view'],
        models.skill: ['add', 'change', 'delete', 'view'],
        models.project: ['add', 'change', 'delete', 'view'],
        models.work_experience: ['add', 'change', 'delete', 'view'],
    },
    'university_agent': {
        models.university: ['change', 'view'],
        models.applicant: ['view'],
        models.work_experience: ['view'],
        models.attachment: ['view'],
        models.skill: ['view'],
        models.project: ['view'],
    },
    'main_staff': {
        models.university: ['add', 'change', 'delete', 'view'],
        models.applicant: ['view'],
        models.work_experience: ['view'],
        models.attachment: ['view'],
        models.skill: ['view'],
        models.project: ['view'],
        models.work_experience: ['view'],
        models.university_agent: ['add', 'change', 'delete', 'view'],
    }
}


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):
        # Loop groups
        for group_name in GROUPS_PERMISSIONS:

            # Get or create group
            group, created = Group.objects.get_or_create(name=group_name)

            # Loop models in group
            for model_cls in GROUPS_PERMISSIONS[group_name]:

                # Loop permissions in group/model
                for perm_index, perm_name in \
                        enumerate(GROUPS_PERMISSIONS[group_name][model_cls]):

                    # Generate permission name as Django would generate it
                    codename = perm_name + "_" + model_cls._meta.model_name

                    try:
                        # Find permission object and add to group
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write("Adding "
                                          + codename
                                          + " to group "
                                          + group.__str__())
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
