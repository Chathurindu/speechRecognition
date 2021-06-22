from django.db import models

from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin)

# Create your models here.
# Create your models here.
from django.db.models import JSONField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None,is_active=True, is_admin=False,is_staff=False,is_customer=False):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self,email,password=None):
        superuser =self.create_user(email,password=password,is_admin=True,is_staff=True)
        return superuser

    def create_staffuser(self,email,password=None):
        staffuser= self.create_user(email,password=password,is_staff=True)
        return staffuser


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    user_type = models.CharField(choices=(("abs","abs"),("doctor","doctor"),("patient","patient"),),max_length=15,default="abs")

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_email(self):
        return self.email


    # @property
    # def is_active(self):
    #     return self.active

    @property
    def is_admin(self):
        return self.admin
    @property
    def is_staff(self):
        return self.staff


class DoctorProfile(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    # TODO:
    #   add other attributes

class PatientProfile(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True) # future use
    doctor = models.ForeignKey(DoctorProfile,on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    parent_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, null=True, blank=True)
    reference = JSONField()

    @property
    def age(self):
        #todo
        return 3

