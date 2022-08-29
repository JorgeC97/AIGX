from django.shortcuts import render, HttpResponse
from .models import Reporte
from .serializers import ReporteSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import xmlrpc.client
from django import forms
from .forms import LoginForm
from django.contrib.sessions.backends.db import SessionStore
from datetime import datetime
from numpy import append

master_uid = '13'
master_password = '07b55b55a7436eb683973fb64e0ff93d0e24c0f1'
db = "axonebackoffice-aigx-main-1924299"
url = "http://axhs.odoo.com"
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

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
    # password = "cf6550d7f13beca8556c3ed77f91ffbe53a0005a" #main
    
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
    
    uid = common.authenticate(db, username, password, {}) ## gets App's user uid
    if (uid is not False):
        partnerId = models.execute_kw(db, master_uid, master_password,'res.partner', 'search_read',[[['user_ids','=',uid]]])[0].get('id')
        request.session['uid'] = uid
        request.session['partnerId'] = partnerId
        request.session['password'] = password

        # request.session['empresa'] = getEmpresa(uid, password)
        print(partnerId)
        user = models.execute_kw(db, master_uid, master_password,
        'res.partner', 'search_read',
        [[['user_ids','=',uid]]])
        # return HttpResponse(user[0].get('name'), status=200)
        request.session.create()
        print(request.session.session_key)
        resp = {
            "name": user[0].get('name'),
            "session": request.session.session_key
        }
        print(resp)
        print(request.session['partnerId'])
        return JsonResponse(resp)
    return HttpResponse("Wrong Username or Password", status=200)

@csrf_exempt
def readUser(request):
    uid = request.session.get('uid', False)

    if(uid is not False):
        user = models.execute_kw(db, master_uid, master_password,
        'res.partner', 'search_read',
        [[['user_ids','=',uid]]])
        return HttpResponse(user[0].get('name'))
    return HttpResponse("Not logged In")

@csrf_exempt
def readProjects(request):
    #uid="53"
    #password="123456"
    
    sid = request.GET.get('sid','')
    if(sid != ''):
        session = SessionStore(session_key=request.GET.get('sid',''))
    else:
        session = request.session
    partnerId = session.get('partnerId', False)
    uid = session.get('uid',False)
    password = session.get('password',False)
    if(partnerId is not False):
        #projects = models.execute_kw(db, master_uid, master_password,
        projects = models.execute_kw(db, uid, password,
        'project.project', 'search_read',
        #[[['partner_id','=',partnerId]]],
        [[['message_is_follower','=',True]]],
        {'fields': ['id','name']})
        print(projects)
        projectsFound = { }
        projectsFound['items'] = projects
        return JsonResponse(projectsFound)
    return HttpResponse("Not logged In")

@csrf_exempt
def readTasks(request, projectId):
    partnerId = request.session.get('partnerId', False)
    if(partnerId is not False):
        projects = models.execute_kw(db, master_uid, master_password,
        'project.project', 'search_read',
        [[['id','=',projectId]]],
        {'fields': ['task_ids']})
        print(projects)
        taskIds = projects[0].get('task_ids')
        print(taskIds)
        tasks = []
        for taskId in taskIds:
            task = models.execute_kw(db, master_uid, master_password,
            'project.task', 'search_read',
            [[['id','=',taskId]]])
            print(task)
            tasks.append(task)
        return HttpResponse(tasks)
    return HttpResponse("Not logged In")

def readReporteActividad(request, activityId):
    uid = request.session.get('uid', False)
    if(uid is False):
        return HttpResponse("Not logged In")
    else:
        password = request.session.get('secret')
        
        empresa = "Aceros Trefilados de Precisión, S. de R.L. de C.V. (NUCOR), Christian Merino"
        hola=models.execute_kw(db, master_uid, master_password,
        'x_reporte_de_actividad', 'search_read',
        [[['id', '=', activityId]]])
        return HttpResponse(hola)

def getEmpresa(uid, password):
    uid = request.session.get('uid')
    password = request.session.get('secret')
    hola=models.execute_kw(db, uid, password,
        'res.partner', 'search_read',  
        [[['id', 'equals', uid]]],
        {'fields': ['name']})
    return hola


@csrf_exempt
def getReportesS(request):
    sid = request.GET.get('sid','')
    if(sid != ''):
        session = SessionStore(session_key=request.GET.get('sid',''))
    else:
        return HttpResponse("Not logged In")
    project = request.GET.get('contrato','')
    reportes = models.execute_kw(db, master_uid, master_password,
        'x_reporte_de_actividad', 'search_read',
        [[['x_studio_contrato', '=', project ],['x_studio_fecha', '!=', False ]]],
        {'fields': 
        [
            'x_name',
            'x_studio_fecha',
            'x_studio_cliente', 
            'x_studio_contrato', 
            'x_studio__parte', 
            'x_studio_cantidad_inspeccionada', 
            'x_studio_cantidad_rechazada',
            'x_studio_cantidad_retrabajada',
            'x_studio_cantidad_aceptada'
            ]})

    for n in reportes:
        dia=n.get('x_studio_fecha')
        if dia:
            n['semana']= datetime.strptime(dia, '%Y-%m-%d').isocalendar()[1]
            n['year']= datetime.strptime(dia, '%Y-%m-%d').year
        else:
            print(n.get('id'))

    for x in reportes:
        if not x['x_studio_fecha']:
                reportes.remove(x)

    nreportes = sorted(reportes, key=lambda d: d['x_studio_fecha']) 

    reportesO=[]

    x=len(nreportes)
    numS=0
    cont=0

    while cont<x:
        if cont==0:
            reportesO.append({'semana':nreportes[cont].get('semana')})
            reportesO[numS]['year']=nreportes[cont]['year']
            reportesO[numS]['x_studio__parte']=nreportes[cont]['x_studio__parte']
            reportesO[numS]['x_studio_cantidad_inspeccionada']=nreportes[cont]['x_studio_cantidad_inspeccionada']
            reportesO[numS]['x_studio_cantidad_rechazada']=nreportes[cont]['x_studio_cantidad_rechazada']
            reportesO[numS]['x_studio_cantidad_retrabajada']=nreportes[cont]['x_studio_cantidad_retrabajada']
            reportesO[numS]['x_studio_cantidad_aceptada']=nreportes[cont]['x_studio_cantidad_aceptada']
            cont+=1
        elif nreportes[cont].get('semana') != nreportes[cont-1].get('semana'):
            numS+=1
            reportesO.append({'semana':nreportes[cont].get('semana')})
            reportesO[numS]['year']=nreportes[cont]['year']
            reportesO[numS]['x_studio__parte']=nreportes[cont]['x_studio__parte']
            reportesO[numS]['x_studio_cantidad_inspeccionada']=nreportes[cont]['x_studio_cantidad_inspeccionada']
            reportesO[numS]['x_studio_cantidad_rechazada']=nreportes[cont]['x_studio_cantidad_rechazada']
            reportesO[numS]['x_studio_cantidad_retrabajada']=nreportes[cont]['x_studio_cantidad_retrabajada']
            reportesO[numS]['x_studio_cantidad_aceptada']=nreportes[cont]['x_studio_cantidad_aceptada']
            cont+=1
        else:
            reportesO[numS]['x_studio__parte'] += ((','+nreportes[cont]['x_studio__parte']) if nreportes[cont]['x_studio__parte'] else '')
            reportesO[numS]['x_studio_cantidad_inspeccionada']+= (nreportes[cont]['x_studio_cantidad_inspeccionada'] if nreportes[cont]['x_studio__parte'] else 0)
            reportesO[numS]['x_studio_cantidad_rechazada']+= (nreportes[cont]['x_studio_cantidad_rechazada'] if nreportes[cont]['x_studio__parte'] else 0)
            reportesO[numS]['x_studio_cantidad_retrabajada']+= (nreportes[cont]['x_studio_cantidad_retrabajada'] if nreportes[cont]['x_studio__parte'] else 0)
            reportesO[numS]['x_studio_cantidad_aceptada']+= (nreportes[cont]['x_studio_cantidad_aceptada'] if nreportes[cont]['x_studio__parte'] else 0)
            cont+=1

    reportesS=list(reversed(reportesO))        

    temp = {}
    temp['items']=reportesS
    return  JsonResponse(temp)

