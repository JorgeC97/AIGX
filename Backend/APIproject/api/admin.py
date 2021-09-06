from django.contrib import admin
from .models import Reporte

# Register your models here.

#admin.site.register(Reporte)

@admin.register(Reporte)
class ReporteModel(admin.ModelAdmin):
    list_filter = ('title', 'cliente', 'fecha','lote','parte')
    list_display = ('title','fecha')