from django.db import models


class Reporte(models.Model):
    id_contrato = models.CharField(max_length=50)
    id_tarea = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    cliente = models.CharField(max_length=50)
    fecha = models.DateField()
    lote = models.CharField(max_length=20)
    parte = models.CharField(max_length=20)
    cantIns = models.PositiveIntegerField()
    cantRech = models.PositiveIntegerField()
    defecto = models.CharField(max_length=20)
    cantRet = models.PositiveIntegerField()
    cantAcep = models.PositiveIntegerField()

    def __str__(self):
        return self.title

# class User(models.Model):
#     uid = models.PositiveIntegerField()
#     partnerId = models.PositiveIntegerField()

#     def __init__(self, uid):
#         self.uid = uid
    
#     def setPartnerId(self, partnerId):
#         self.partnerId = partnerId