from django.contrib import admin

from weight.models import Weight


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    pass
