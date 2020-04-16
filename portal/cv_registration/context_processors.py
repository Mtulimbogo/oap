from cv_registration.models import applicant


def get_applicant_image(request):

    try:
        data = applicant.objects.filter(user=request.user.id).values("user_image")
        # print(list(data)[0]["user_image"])
        if list(data)[0]["user_image"] is None:
            edit_dict = {"user_avatar": "logo.png"}
            return edit_dict
        else:
            edit_dict = {"user_avatar": list(data)[0]["user_image"]}
            return edit_dict
    except Exception as w:
        edit_dict = {"user_avatar": "logo.png"}
        return edit_dict
