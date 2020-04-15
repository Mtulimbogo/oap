from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.shortcuts import redirect
User = get_user_model()


# def login_spana(request):
#     # return reverse("account_signup")
    # return redirect("/university/")


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        print(self.request.user.username)
        type_of_applicant = "pt_student"
        if is_member(self.request.user, "pt_student"):
            type_of_applicant = "pt_student"
            # return redirect('cv_registration.views.personalinfo')
        if is_member(self.request.user, "researcher"):
            type_of_applicant = "researcher"
            # return redirect('cv_registration.views.personalinfo')
        if is_member(self.request.user, "mentor"):
            type_of_applicant = "mentor"
            # return redirect('cv_registration.views.personalinfo')
        if is_member(self.request.user, "university_agent"):
            type_of_applicant = "university_agent"
            # return redirect('university_regulator.views.home')
        if is_member(self.request.user, "main_staff"):
            type_of_applicant = "main_staff"
            # return redirect('ega_org.views.home')

        return reverse('users:user_redirect_to_page', kwargs={"applicant_group": type_of_applicant})

        # return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def user_redirect_to_page(request, **kwargs):
    print(kwargs["applicant_group"])
    if kwargs["applicant_group"] == "pt_student":
        return redirect("/info_registration/")

    if kwargs["applicant_group"] == "mentors":
        return redirect("/info_registration/")

    if kwargs["applicant_group"] == "researcher":
        return redirect("/info_registration/")

    if kwargs["applicant_group"] == "main_staff":
        return redirect("/ega/")

    if kwargs["applicant_group"] == "university_agent":
        return redirect("/university/")

    # return redirect("account_logout")


def is_member(user, user_group):
    return user.groups.filter(name=user_group).exists()
