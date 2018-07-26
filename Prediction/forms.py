'''
Author = Meet Shah
Date:    10/05/2018
Source:  This link helped me to write validation code
         https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
'''

from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
class UploadFileForm(forms.Form):

    file = forms.FileField(label='Choose CSV File', widget=forms.FileInput(attrs={'accept': ".csv", "id" : "filename"}))

    def clean_file(self):
        content = self.cleaned_data['file']
        filename = str(content)
        #content_type = content.content_type.split('/')[0]
        Max_SIZE = int(settings.MAX_UPLOAD_SIZE)
        upload_file_size = int(content._size)
        if filename.endswith('.csv'):
            if upload_file_size > Max_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('Please Upload Csv File Only !!!'))
        return content