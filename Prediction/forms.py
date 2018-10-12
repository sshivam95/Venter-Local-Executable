from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as f
from django.conf import settings


class UploadFileForm(forms.Form):
    """
    Author = Meet Shah
    Date:    10/05/2018
    Source:  This link helped me to write validation code
             https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
    """
    file = forms.FileField(label='Choose CSV File', widget=forms.FileInput(attrs={'accept': ".csv", "id": "filename"}))

    def clean_file(self):
        content = self.cleaned_data['file']
        filename = str(content)
        max_size = int(settings.MAX_UPLOAD_SIZE)
        upload_file_size = int(content.size)
        if filename.endswith('.csv'):
            if upload_file_size > max_size:
                raise forms.ValidationError(f('Please keep file size under %s. Current file size is %s') % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)))
        else:
            raise forms.ValidationError(f('Please Upload Csv File Only !!!'))
        return content
