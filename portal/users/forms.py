from django.contrib.auth import get_user_model
from django import forms as django_forms
from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from cv_registration import models
User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class CustomSignupForm(django_forms.ModelForm):

    PT_STUDENT = 'pt_student'
    MENTOR = 'mentors'
    RESEARCHER = 'researcher'

    GROUPS = [
        (RESEARCHER, 'Researcher'),
        (MENTOR, 'Mentor'),
        (PT_STUDENT, 'PT Student'),
    ]

    applicant_type = django_forms.CharField(max_length=17, widget=django_forms.Select(choices=GROUPS))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', ]

    def signup(self, request, user):
        applicant_type = self.cleaned_data['applicant_type']
        # print(applicant_type)
        user.username = self.cleaned_data['email']

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # print(user.username)
        try:
            user.save()
            applicant = models.applicant()
            applicant.user = user
            applicant.first_name = self.cleaned_data['first_name']
            applicant.last_name = self.cleaned_data['last_name']
            applicant.save()
        except Exception as e:
            print(
                'Sorry something happened'
            )
        user.save()

        user_group = Group.objects.get(name=applicant_type)
        user_group.user_set.add(user)
        if user_group == "pt_student":
            applicant_std = models.applicant_student()
            applicant_std.applicant_additional = user
            applicant.save()
