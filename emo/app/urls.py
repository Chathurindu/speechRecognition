from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    url(r'^emo-predict/$', EmotionPredict.as_view(), name='APIEmoPredict'),
]
