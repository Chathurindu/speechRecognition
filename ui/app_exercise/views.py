from django.shortcuts import render, redirect

# Create your views here.
from app_exercise.models import Exercise
from django.views.decorators.csrf import csrf_exempt

from app_profile.models import DoctorProfile, PatientProfile



def video_exercise_list(request):
    doc_obj = DoctorProfile.objects.get(user=request.user)
    video_qs = Exercise.objects.filter(exercise_type="video",doctor=doc_obj)
    video_list = []
    for v in video_qs:
        video_list.append({
            "id":v.id,
            "title": v.name,
            "category": v.category,
            "age": v.target_age,
            "emotion": v.emotion,
            "intonation": v.intonations,
            "phoneme": v.phoneme,
            "file":v.file_uri
        })
    return render(request, "index-video.html", context={"videoList":video_list})

def photo_exercise_list(request):
    doc_obj = DoctorProfile.objects.get(user=request.user)
    qs = Exercise.objects.filter(exercise_type="photo",doctor=doc_obj)
    photo_list = []
    for v in qs:
        photo_list.append({
            "id":v.id,
            "title": v.name,
            "category": v.category,
            "age": v.target_age,
            "emotion": v.emotion,
            "intonation": v.intonations,
            "phoneme": v.phoneme,
            "file":v.file_uri
        })
    return render(request, "index-photo.html", context={"photoList":photo_list})

def physical_exercise_list(request):
    return render(request, "index.html", context={})

def add_video_exercise(request):
    return render(request, "videoForm.html", context={})

@csrf_exempt
def add_exercise_api(request):
    if request.method =="POST":
        try:
            doc_obj = DoctorProfile.objects.get(user= request.user)
            reqData = request.POST
            type = request.GET.get("type","video")
            ex = Exercise(exercise_type=type,doctor =doc_obj)
            ex.name = reqData.get("name")
            ex.category = reqData.get("category")
            ex.target_age = reqData.get("age")
            ex.emotion = reqData.get("emotion")
            ex.intonations = reqData.get("intonations")
            ex.phoneme  = reqData.get("phoneme")
            ex.file = request.FILES.get("file")

            ex.save()
        except Exception as e:
            print(e)
            return redirect("/add_video_exercise")

    return redirect("/photo_exercise_list")

def add_photo_exercise(request):
    return render(request, "photoForm.html", context={})

def add_physical_exercise(request):
    return render(request, "index.html", context={})

def exercise(request,id):
    if request.GET.get("patient"):
        return redirect(f"/patient_profile/{request.GET.get('patient')}")


    exercise_obj = Exercise.objects.get(id=id)
    doc_obj = DoctorProfile.objects.get(user=request.user)
    patient_list = PatientProfile.objects.filter(doctor=doc_obj).values("id","name")
    context = {
        "file":exercise_obj.file_uri,
        "patient_list": patient_list,
        "exeId": id,

               }
    if exercise_obj.exercise_type == "video":
        return render(request, "video_play.html", context=context)
    else:
        return render(request, "photo_display.html", context=context)

def realtime(request):
    doc_obj = DoctorProfile.objects.get(user=request.user)
    patient_list = PatientProfile.objects.filter(doctor=doc_obj).values("id","name")
    context = {"patient_list": patient_list}
    return render(request, "realtime_record.html", context=context)

# def photo_exercise(request,id):
#     return render(request, "index.html", context={})
#
# def physical_exercise(request,id):
#     return render(request, "index.html", context={})

