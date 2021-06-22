from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


from app_profile.models import User, DoctorProfile, PatientProfile

from app_records.models import Record


def index(request):
    return render(request,"index.html",context={})
    # return render(request,"base.html",context={})


def sign_in(request):
    return render(request,"signin.html",context={})

def sign_out(request):
    logout(request)
    return redirect('/')


def sign_up(request):
    return render(request,"signup.html",context={})


@csrf_exempt
def sign_in_api(request):
    if request.method == "POST":
        usr = authenticate(request,email=request.POST.get('email'),password=request.POST.get('password'))
        if usr:
            login(request,usr)
            return redirect("/doctor_profile")

    return redirect("/signin")


@csrf_exempt
def sign_up_api(request):
    if request.method == "POST":
        try:
            reqData = request.POST
            usr = User(email=reqData.get("email"))
            usr.set_password(reqData.get("password"))
            usr.role = "doctor"
            usr.save()

            doc_obj = DoctorProfile(user=usr)
            doc_obj.phone = reqData.get("phone_number")
            doc_obj.name = reqData.get("name")
            doc_obj.address = reqData.get("address")
            doc_obj.qualification = reqData.get("qualification")
            doc_obj.save()
        except Exception as e:
            print(e)
            return redirect("/signup")

    return redirect("/")


def doctor_profile(request):
    #TODO
    return render(request,"doctorProfile.html",context={})


def patient_list(request):
    doc_obj = DoctorProfile.objects.get(user=request.user)
    patients_qs = PatientProfile.objects.filter(doctor=doc_obj)
    patient_lst = []
    for p in patients_qs:
        patient_lst.append({
            "p_id": p.id,
            "childName":p.name,
            "parentName":p.parent_name,
            "age": p.age,
            "phone": p.phone
        })
    return render(request,"patient.html",context={"patientList":patient_lst})


def patient_profile(request,id):
    patient_obj = PatientProfile.objects.get(id=id)
    record_list = []
    for i,r in enumerate(Record.objects.filter(patient=patient_obj)):
        record_list.append(
            {   "index": i,
                "id": r.id,
                "file": f"/media/{r.audio_file}",
                "exe": r.exercise.name if r.exercise else None,
                "comment": r.comment,
                "report": r.report
            }
        )
        print(r.report)

    context = {
        "childName": patient_obj.name,
        "parentName": patient_obj.parent_name,
        "phone": patient_obj.phone,
        "age":patient_obj.age,
        "reference": patient_obj.reference,
        "record_list": record_list,
    }
    return render(request,"patientProfile.html",context=context)


def patient_register(request):
    return render(request,"patientForm.html",context={})

@csrf_exempt
def patient_register_api(request):
    if request.method == "POST":
        reqData = request.POST
        doc_obj = DoctorProfile.objects.get(user= request.user)
        try:
            usr = User(email=reqData.get('email'))
            usr.set_password("admin")
            usr.role = "patient"
            usr.save()

            patient_obj = PatientProfile(user=usr,doctor =doc_obj)
            patient_obj.name = reqData.get('name')
            patient_obj.date_of_birth = reqData.get('dob')
            patient_obj.parent_name = reqData.get('parent_name')
            patient_obj.reference = {
                "FavCartoonCharacter": reqData.get('ref1'),
                "MostUsedWord": reqData.get('ref2'),
                "FavFood": reqData.get('ref3'),
                "FavColour": reqData.get('ref4'),
                "FearfulThing": reqData.get('ref5'),
            }
            patient_obj.save()
        except:
            redirect("/patient_register")
    return redirect("/patient_list")

