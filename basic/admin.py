from django.contrib import admin
from .models import Info,Service,Dentist,Schedule,Contact
# Register your models here.
class InfoAdmin(admin.ModelAdmin):
	list_display=('user_name','user_ID','user_address','user_tel','user_birth','can_manage','user_identity')
admin.site.register(Info,InfoAdmin)
class ServiceAdmin(admin.ModelAdmin):
	list_display=('name','description','price')
admin.site.register(Service,ServiceAdmin)
class DentistAdmin(admin.ModelAdmin):
	list_display=('name','list_services','list_times')
	search_fields=('name','services__name','time__time')
	filter_horizontal=('services','time')
	def list_services(self,obj):
		return ",".join([s.name for s in obj.services.all()])
	def list_times(self,obj):
		return ",".join([t.time for t in obj.time.all()])
admin.site.register(Dentist,DentistAdmin)
admin.site.register(Schedule)
class ContactAdmin(admin.ModelAdmin):
	list_display=('name','email','message','created_at')
admin.site.register(Contact,ContactAdmin)