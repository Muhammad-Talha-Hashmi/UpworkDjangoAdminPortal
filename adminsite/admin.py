from django.contrib import admin
from .models import ResearchesList, Users, Journals



# Register your models here.
admin.site.register(Journals)
admin.site.register(Users)
admin.site.register(ResearchesList)