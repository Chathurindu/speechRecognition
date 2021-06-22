from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    url(r'^into-predict/$', IntoPredict.as_view(), name='APIintoPredict'),
    url(r'^age-predict/$', AgePredict.as_view(), name='APIagePredict'),
    url(r'^phone-predict/$', phone_predict),
]
