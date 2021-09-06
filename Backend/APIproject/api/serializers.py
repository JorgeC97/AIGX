from rest_framework import serializers
from .models import Reporte

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ['id','id_contrato','id_tarea','title', 'cliente', 'fecha', 'lote', 'parte', 'cantIns', 'cantRech', 'defecto', 'cantRet', 'cantAcep']
