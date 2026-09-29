from django.contrib import admin
from .models import Register
# Register your models here.
class RegisterAdmin(admin.ModelAdmin):
	list_display=('patient_name','dentist','service','appointment_date')
admin.site.register(Register,RegisterAdmin)