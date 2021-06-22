import json

from django.db import models
import requests

# Create your models here.
from app_exercise.models import Exercise
from app_profile.models import PatientProfile
from django.db.models import JSONField
from django.conf import settings


class Record(models.Model):
    patient = models.ForeignKey(PatientProfile,on_delete=models.CASCADE)
    audio_file = models.FileField()
    exercise = models.ForeignKey(Exercise,on_delete=models.SET_NULL,null=True,blank=True)
    comment = models.CharField(max_length=1000,null=True,blank=True)
    report = JSONField(null=True,blank=True)

    # def save(self,*args, **kwargs):
    #     data = {"path": self.audio_file.path}
    #     r_age = requests.post(settings.AGE_BACKEND, data=data)
    #     r_into = requests.post(settings.INTO_BACKEND, data=data)
    #     r_emo = requests.post(settings.EMO_BACKEND, data=data)
    #     record_dict = {
    #         "age": json.loads(r_age.text).get("age_prediction"),
    #         "intonation": json.loads(r_into.text).get("into_prediction"),
    #         "emotion": json.loads(r_emo.text).get("emotion_prediction"),
    #     }
    #     print(record_dict)
    #     self.report= record_dict
    #     super(Record, self).save(*args, **kwargs)

