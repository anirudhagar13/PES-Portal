from django.contrib import admin
from .models import *

# Register your models here.
#class Eventadmin(admin.ModelAdmin):
#	list_display = ["id","club_id","event_id","event_name","event_date","venue","no_part","no_reg","contact_info","event_desc","own_form","timestamp"]
admin.site.register(Event)#,Eventadmin)
admin.site.register(Signup)
admin.site.register(Register)





