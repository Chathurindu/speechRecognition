"""ui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
# from app_profile.views import *

from app_profile.views import index, sign_in, sign_up, sign_out, patient_list, patient_profile, patient_register, \
    doctor_profile, sign_up_api, patient_register_api, sign_in_api

from app_exercise.views import video_exercise_list, photo_exercise_list, physical_exercise_list, exercise, \
    add_physical_exercise, add_photo_exercise, add_video_exercise, add_exercise_api, realtime

from app_records.views import add_record_api, add_record
from django.views.generic import TemplateView

urlpatterns = [

    path('', index),
    path('signin', sign_in),
    path('signup', sign_up),
    path('signout', sign_out),
    path('patient_list', patient_list),
    path('doctor_profile', doctor_profile),
    path('patient_profile/<int:id>', patient_profile),
    path('patient_register', patient_register),

    path('video_exercise_list', video_exercise_list),
    path('photo_exercise_list', photo_exercise_list),
    path('physical_exercise_list', physical_exercise_list),
    path('exercise/<int:id>', exercise),
    path('realtime', realtime),
    # path('physical_exercise', physical_exercise),
    path('add_video_exercise', add_video_exercise),
    path('add_photo_exercise', add_photo_exercise),
    path('add_physical_exercise', add_physical_exercise),
    path('add_record', add_record),

    # API
    path('api/login', sign_in_api),
    path('api/sign_up', sign_up_api),
    path('api/patient_register', patient_register_api),
    path('api/add_exercise', add_exercise_api),
    path('api/add_record_api', add_record_api),

    path('guid', TemplateView.as_view(template_name='guide.html'), name='guid'),

    path('admin/', admin.site.urls),
    path('patientProfile', TemplateView.as_view(template_name='patientProfile.html'), name='patientProfile'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
