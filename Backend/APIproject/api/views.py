from django.shortcuts import render, HttpResponse
from .models import Reporte
from .serializers import ReporteSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import xmlrpc.client
from django import forms
from .forms import LoginForm

# Create your views here.
@csrf_exempt
def reporte_list(request):
    if request.method == 'GET':
        reportes = Reporte.objects.all()
        serializer = ReporteSerializer(reportes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReporteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
##contrato->Tarea->Reporte

@csrf_exempt
def get_list_contratos():
    uid = request.session.get('uid')
    password = request.session.get('secret')
    empresa = getEmpresa(uid, password)


@csrf_exempt
def get_list_reportes(tarea):
    uid = request.session.get('uid')
    password = request.session.get('secret')
    reportes=models.execute_kw(db, uid, password,
        'x_reporte_de_actividad', 'search_read',
        [[['x_studio_cliente', 'like', tarea]]],
        {'fields': 
        [
            'x_nombre',
            'x_studio_cliente', 
            'x_studio_fecha', 
            'x_studio__parte', 
            'x_studio_cantidad_inspeccionada', 
            'x_studio_cantidad_rechazada', 
            'x_studio_cantidad_aceptada'
            ]})

    # id_contrato = models.CharField(max_length=50)
    # id_tarea = models.CharField(max_length=50)
    # title = models.CharField(max_length=50)
    # cliente = models.CharField(max_length=50)
    # fecha = models.DateField()
    # lote = models.CharField(max_length=20)
    # parte = models.CharField(max_length=20)
    # cantIns = models.PositiveIntegerField()
    # cantRech = models.PositiveIntegerField()
    # defecto = models.CharField(max_length=20)
    # cantRet = models.PositiveIntegerField()
    # cantAcep = models.PositiveIntegerField()


@csrf_exempt
def reporte_details(request, pk):
    try:
        reporte = Reporte.objects.get(pk=pk)
    
    except Reporte.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ReporteSerializer(reporte)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ReporteSerializer(reporte, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        reporte.delete()
        return HttpResponse(status=204)

@csrf_exempt
def login(request):
    # username = "jcabrales@aigx.mx"
    # url = "https://axhs.odoo.com" #main
    # db = "axonebackoffice-aigx-main-1924299" #main
    # password = "cf6550d7f13beca8556c3ed77f91ffbe53a0005" #main
    # common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    if request.method == 'POST':
        request.session.flush()
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
    elif request.method == 'GET':
        request.session.flush()
        form = LoginForm(request.GET)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
    else:
        return HttpResponse("Wrong Method") #redirect somewhere else
    
    uid = common.authenticate(db, username, password, {})
    if (uid is not False):
        request.session['uid'] = uid
        request.session['secret'] = password
        request.session['empresa'] = getEmpresa(uid, password)
        print(uid)
        return HttpResponse(uid, status=200)
    return HttpResponse("Wrong Username or Password", status=200)

@csrf_exempt
def readUser(request):
    uid = request.session.get('uid', False)

    if(uid is not False):
        return HttpResponse(uid)
    return HttpResponse("Not logged In")

def readReporteActividad(request):
    uid = request.session.get('uid', False)
    if(uid is False):
        return HttpResponse("Not logged In")
    else:
        password = request.session.get('secret')
        
        empresa = "Aceros Trefilados de Precisión, S. de R.L. de C.V. (NUCOR), Christian Merino"
        hola=models.execute_kw(db, uid, password,
        'x_reporte_de_actividad', 'search_read',
        [[['x_studio_cliente', 'like', empresa]]],
        {'fields': ['x_studio_cliente', 'x_studio_fecha', 'x_studio__parte', 'x_studio_cantidad_inspeccionada', 'x_studio_cantidad_aceptada']})
        return HttpResponse(hola)

def getEmpresa(uid, password):
    uid = request.session.get('uid')
    password = request.session.get('secret')
    hola=models.execute_kw(db, uid, password,
        'res.partner', 'search_read',  
        [[['id', 'equals', uid]]],
        {'fields': ['name']})
    return hola
