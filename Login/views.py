from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
import os
from django.conf import settings

# Create your views here.

# source implementing logout: https://www.youtube.com/watch?v=l8f-KFxw-xU
# source implementing file delete: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
# diff between os.unlink() and os.remove() => https://stackoverflow.com/questions/42636018/python-difference-between-os-remove-and-os-unlink-and-which-one-to-use
from django.urls import reverse


def user_logout(request):
    # username = request.user.username
    # folder_path = os.path.join(settings.MEDIA_ROOT, username, "CSV", "input")
    # for file_object in os.listdir(folder_path):
    #     file_object_path = os.path.join(folder_path, file_object)
    #     os.remove(file_object_path)
    logout(request)
    return HttpResponseRedirect("/login")


def EditProfile(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        if request.method == 'POST':

            message = ""
            flag = ""
            FirstName = request.POST['FirstName']
            LastName = request.POST['LastName']
            Email = request.POST['Email']
            user = request.user
            # print(FirstName, ' ', LastName, ' ', Email)
            user.first_name = FirstName
            user.last_name = LastName
            user.email = Email
            user.save()
            user = request.user
            message = "Your profile has been updated sucessfully"
            flag = "success"
            company = request.user.groups.values_list('name', flat=True)
            context = {'FirstName': user.first_name, 'LastName': user.last_name, 'UserName': request.user.username,
                       'Group': company[0], 'Email': user.email, 'Message': message, 'Flag': flag}
            return render(request, 'Login/EditProfile.html', context)

        else:
            user = request.user
            company = request.user.groups.values_list('name', flat=True)
            context = {'FirstName': user.first_name, 'LastName': user.last_name, 'UserName': request.user.username,
                       'Group': company[0], 'Email': user.email}
            print(company)
            for k in context:
                print(k, ':', context[k])
            return render(request, 'Login/EditProfile.html', context)


# def garbage(request):
#     print("IN THE GARBAGE")
#     return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
