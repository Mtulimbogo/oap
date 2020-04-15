import datetime


def get_ega_footer(request):
    current_datetime = datetime.datetime.now()
    footer = "© " + str(current_datetime.year) + " e-GA . Haki zote zimehifadhiwa."

    return {
        'current_year': current_datetime.year, 'footer': footer,
    }


def user_data(request):
    if request.user.id is None:
        return {'user_name': "Anon User"}
        # user is anon user
    else:
        # user is a real user
        user_name = request.user.first_name + " " + request.user.last_name

        return {'user_name': user_name}
