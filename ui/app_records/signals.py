import json

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from app_records.models import Record


@receiver(post_save,sender=Record)
def update_report(sender,instance,**kwargs):
    if hasattr(instance, '_dirty'):
        return
    print(instance.audio_file.path)
    data = {"path":instance.audio_file.path}
    r_age = requests.post(settings.AGE_BACKEND, data=data)
    r_into = requests.post(settings.INTO_BACKEND, data=data)
    r_emo = requests.post(settings.EMO_BACKEND, data=data)
    r_phone = requests.post(settings.PHONE_BACKEND, data=data)
    record_dict = {
        "age": json.loads(r_age.text).get("age_prediction"),
        "intonation": json.loads(r_into.text).get("into_prediction"),
        "emotion": json.loads(r_emo.text).get("emotion_prediction"),
        "phone": json.loads(r_phone.text).get("phone_prediction"),
    }

    instance.report = record_dict

    try:
        instance._dirty = True
        instance.save(force_update=True)
    finally:
        del instance._dirty

    # print("IM POST")
    # file_dict = {"file_name":instance.audio_file}
    # # file_dict1 = {"file_name":instance.audio_file}
    # report = {}
    # r_age = requests.post(settings.AGE_BACKEND, files=file_dict)
    # print(json.loads(r_age.text), type(json.loads(r_age.text)))
    # # r_into = requests.post(settings.INTO_BACKEND, files=file_dict)
    # # print(r_into.text)
    # # print(json.loads(r_into.text), type(json.loads(r_into.text)))
    # # r_emo = requests.post(settings.EMO_BACKEND, files=file_dict)
    # # # # r_phone = requests.post(settings.PHONE_BACKEND, files=file_dict)
    # # # print(json.loads(r_into.text),type(json.loads(r_into.text)))
    # report["age"] = json.loads(r_age.text)['age_prediction']
    # # # # print(r_into.text)
    # # # # print(r_emo.text)
    # # # report["intonation"] = json.loads(r_into.text)['into_prediction']
    # # # # report["emotion"] = json.loads(r_emo.text)['emotion_prediction']
    # print(report)
    # # self.report = report


# @receiver(post_save,sender=Record)
# def update_report1(sender,instance,**kwargs):
#     print("IM 2")
#     file_dict = {"file_name": instance.audio_file}
#     r_into = requests.post(settings.INTO_BACKEND, files=file_dict)
#     print(r_into.text)