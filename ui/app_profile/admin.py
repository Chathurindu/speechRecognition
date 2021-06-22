from django.contrib import admin
from .forms import UserAdminCreationForm, UserAdminChangeForm

# Register your models here.
from .models import *


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    class Meta:
        model = User

admin.site.register(User, UserAdmin)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)