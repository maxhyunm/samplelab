from django.contrib import admin
from testapp.models import Data


class DataAdmin(admin.ModelAdmin):
    list_display = ('idx', 'up_date')


admin.site.register(Data, DataAdmin)
