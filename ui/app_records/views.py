from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app_profile.models import PatientProfile, DoctorProfile
from app_records.models import Record


def add_record(request):
    doc_obj = DoctorProfile.objects.get(user=request.user)
    patient_list = PatientProfile.objects.filter(doctor=doc_obj).values("id","name")

    return render(request, "manual_record.html", context={"patient_list":patient_list})

@csrf_exempt
def add_record_api(request):
    if request.method == "POST":
        try:
            p = PatientProfile.objects.get(id=request.POST.get('patient'))
            rec = Record()
            rec.audio_file = request.FILES.get("file")
            rec.patient = p
            rec.comment = request.POST.get('comment')
            rec.save()
        except:
            return JsonResponse(status=400)
    return JsonResponse({"report":rec.report},status=200)
