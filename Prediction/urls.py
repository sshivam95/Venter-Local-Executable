from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('predict/', views.upload_file, name='predict'),
    path('download/', views.fileDownload, name='download_file'),
    path('McgmCategory/', TemplateView.as_view(template_name='Prediction/MCGMCATEGORY.html'), name='McgmCategory'),
    path('SpeakupCategory/', TemplateView.as_view(template_name='Prediction/SpeakupCategory.html'),
         name='SpeakupCategory'),
    path('predict/checkOutput/', views.handle_form_data, name='checkOutput'),

]
