from django.urls import path
from .views import reporte_list, reporte_details, login, readUser, readReporteActividad, readProjects, readTasks, getReportesS

urlpatterns = [
    path('api/reportes/', reporte_list),
    path('api/reportes/<int:pk>', reporte_details),
    path('api/login', login),
    path('api/whoami', readUser),
    path('api/proyectos', readProjects),
    path('api/proyecto/<int:projectId>', readTasks),
    path('api/reporteActividad/<int:activityId>', readReporteActividad),
    path('api/reportesS', getReportesS),
]
