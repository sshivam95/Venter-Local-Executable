"""
 This view will render a simple html form if the request is GET. If request is POST then will collect the
 uploaded csv file and save it in appropriate user account.

 ps: write documentation of user group
"""
from django.shortcuts import redirect
# from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse

from .forms import UploadFileForm
from django.conf import settings
from .EditCsvFile import CSV_FILE
from django.http import HttpResponse, HttpResponseRedirect
import os

# Create your views here.
from Prediction import quickstart

def upload_file(request):
    if not request.user.is_authenticated:
        return render(request, 'Prediction/predict_complaint.html')
    else:
        query_set = Group.objects.filter(user=request.user)
        query_set_size = query_set.count()
        Error_dict = {'error': "Please Contact Admin to add you in group"}
        if query_set_size == 0:
            return render(request, 'Prediction/error_message.html', Error_dict)
        else:
            company = str(query_set.all()[0])
            # print(company)
            request.session['company'] = company

        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            user_name = request.user.username
            file_name = str(request.FILES['file'].name)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'], user_name, file_name)
                Csv = CSV_FILE(file_name, user_name, company)
                Header_flag, CATEGORY_LIST = Csv.check_csvfile_header()
                if Header_flag:
                    Dict_List, rows = Csv.Read_file()
                    context = {'dict_list': Dict_List, 'category_list': CATEGORY_LIST, 'rows': rows}
                    request.session['Rows'] = rows
                    request.session['filename'] = file_name
                    return render(request, 'Prediction/check_output.html', context)
                else:
                    Csv.delete()
                    form = UploadFileForm()
                    return render(request, 'Prediction/predict_complaint.html',
                                  {'form': form, 'Error': "Please Submit Csv File With Valid Headers !!!"})
        else:
            form = UploadFileForm()
        return render(request, 'Prediction/predict_complaint.html', {'form': form})


def Handle_Form_Data(request):
    # print("Handle form data called")
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        rows = request.session['Rows']
        correct_category = []
        company = request.session['company']
        if request.method == 'POST':
            file_name = request.session['filename']
            user_name = request.user.username

            for i in range(rows):
                print(request.POST.getlist('select_category' + str(i)+'[]'))
                # if request.POST.getlist('select_category' + str(i)+'[]') != "['Other']":
                try:
                    if request.POST.getlist('other_category'+ str(i)+ '[]') is not None:
                        tuple = (request.POST.getlist('select_category' + str(i)+'[]'), request.POST['other_category' + str(i)])
                        correct_category.append(tuple)
                        print(correct_category)
                except:
                    correct_category.append(request.POST.getlist('select_category' + str(i)+'[]'))
                    print(correct_category)

            Csv = CSV_FILE(file_name, user_name, company)
            Csv.write_file(correct_category)

            if request.POST['radio'] != "no":
                path_folder = request.user.username + "/CSV/output/"
                path_file = 'MEDIA/' + request.user.username + "/CSV/output/" + request.session['filename']
                path_file_diff = 'MEDIA/' + request.user.username + "/CSV/output/Difference of " + request.session['filename']
                quickstart.upload_to_drive(path_folder, 'results of ' + request.session['filename'], "Difference of " + request.session['filename'] ,path_file,path_file_diff)
        return redirect("/download")


def fileDownload(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        path = os.path.join(settings.MEDIA_ROOT, request.user.username, "CSV", "output", request.session['filename'])

        # print(path)
        with open(path, 'rb') as csv:
            response = HttpResponse(csv.read())
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = 'attachment;filename=results of ' + request.session['filename']
        return response


def handle_uploaded_file(f, username, filename):
    DATA_Directory_root = settings.MEDIA_ROOT
    path = os.path.join(DATA_Directory_root, username, "CSV", "input", filename)
    path2 = os.path.join(DATA_Directory_root, username, "CSV", "input")
    if not os.path.exists(path2):
        os.makedirs(path2)

    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
