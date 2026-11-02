from django.contrib import admin
from clinic.models import DoctorDb,AppoinmentDb

# Register your models here.
admin.site.register(DoctorDb)
admin.site.register(AppoinmentDb)
