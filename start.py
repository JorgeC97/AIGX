import xmlrpc.client
from datetime import datetime

from numpy import append


#correo de juan hjuan@aigx.mx
#password de juan Axone$odoo$

username = "jcabrales@aigx.mx"

url = "http://axhs.odoo.com" #main
db = "axonebackoffice-aigx-main-1924299" #main
password = "07b55b55a7436eb683973fb64e0ff93d0e24c0f1" #main

c_username = "hjuan@aigx.mx" #"ejemplo@aigx.mx"   <-- usuario de la app
c_password = "Axone$odoo$"                            #<-- contraseña del usuario de la app

#c_username = "arturo.gonzalez@faurecia.com"
#c_password = "123456"  

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

#uid = common.authenticate(db, c_username, c_password, {})
uid = common.authenticate(db, "arturo.gonzalez@faurecia.com" , "123456", {})

#c_uid = common.authenticate(db, c_username, c_password, {})
#print(c_uid)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

print("hola")

uid = common.authenticate(db, c_username, c_password, {}) ## gets App's user uid

partnerId = models.execute_kw(db, uid, c_password,'res.partner', 'search_read',[[['user_ids','=',uid]]])[0].get('id')
userId = models.execute_kw(db, uid, c_password,'res.partner', 'search_read',[[['user_ids','=',uid]]])[0].get('id')

print(partnerId)

projects = models.execute_kw(db, uid, c_password,
        'project.project', 'search_read',
        [[['partner_id','=',partnerId]]],
        {'fields': ['id','name','user_id']})

print(projects)

uid1 = common.authenticate(db, "arturo.gonzalez@faurecia.com" , "123456", {})
partnerId1 = models.execute_kw(db, uid, c_password,'res.partner', 'search_read',[[['user_ids','=',uid1]]])[0].get('id')
projects1 = models.execute_kw(db, uid, c_password,
        'project.project', 'search_read',
        [[['partner_id','=',partnerId1]]],
        {'fields': ['id','name','user_id']})
print(projects1)
print(partnerId1)

#project=projects[0].get('name')
project='C21027'

print(project)

tasks = models.execute_kw(db, uid, c_password,
        'project.task', 'search_read',
        [[['project_id','=',project]]],
        {'fields': ['name']})

print(tasks)

reportes = models.execute_kw(db, uid, c_password,
        'x_reporte_de_actividad', 'search_read',
        [[['x_studio_contrato', '=', project]]],
        {'fields': 
        [
            'x_name',
            'x_studio_fecha',
            'x_studio_cliente', 
            'x_studio_contrato', 
            'x_studio_fecha', 
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

for x in nreportes:
        print(x['x_studio_fecha'])


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

yyy=list(reversed(reportesO))

for x in reportesO:
        print(x)
        
for x in yyy:
        print(x)



#print (
#    models.execute_kw(db, c_uid, c_password,       #despliega si tiene permisos de acceso el usuario
#    'res.partner', 'check_access_rights',
#    ['read'], {'raise_exception': False})
#)

#print(
#    models.execute_kw(db, uid, password,
#    'res.partner', 'search',
#    [[['id', '=', "3"]]])
#)

#ids = models.execute_kw(db, uid, password,
#    'x_reporte_de_actividad', 'search',
#    [[['x_studio_cantidad_aceptada', '!=', ""]]],
#    {'limit': 1})
#[record] = models.execute_kw(db, uid, password,
#    'x_reporte_de_actividad', 'read', 
#    [ids] , {'fields': ['x_studio_cantidad_aceptada', 'x_name', 'x_studio__parte']})

#print ([record])
#empresa = "Aceros Trefilados de Precisión, S. de R.L. de C.V. (NUCOR), Christian Merino"
#empresa= "SKF DE MEXICO S.A. DE C.V."
#partner_id = 2679
#sujeto = "Christian Merino"

#projects = models.execute_kw(db, uid, password,
#        'project.project', 'search_read',
#        [[['partner_id','=', partner_id]]],
#        {'fields': ['id','name']})

#print(projects)

#print(uid)

#hola=models.execute_kw(db, uid, password,
#        'res.users', 'search_read',  
#        [[['id', '=', uid]]])

#partner_id=models.execute_kw(db,uid, password,
#         'res.partner', 'search_read',
#         [[['id','=','2552']]],
#         {'fields': ['parent_id']})[0].get('parent_id')[0]
#print(partner_id)

#class user:
#    def __init__(self, datos):
#        self.user_partner_id = datos

#class subtask:
#
#    def __init__(self, datos):
#        self.task_id = datos[0]
#
#    def update(self, datos):
#        self.name = datos.get('name')
#        self.reports = datos.get('x_studio_reporte_de_actividad_diaria')

#hola=models.execute_kw(db, uid, password,
#        'res.partner', 'search_read',
#        [[['user_ids','=',c_uid]]])
#appUser = user(hola[0].get('id'))
#print(appUser.user_partner_id)
#hola=models.execute_kw(db, uid, password,
#        'project.project', 'search_read',
#        [[['partner_id','like',appUser.user_partner_id]]]) ## <-- id de usuario en la app
#          {'fields': ['subtask_project_id']})

#if len(hola) != 0:
#    task = subtask(hola[0].get('task_ids'))
#    print('task id:')
#    print(task.task_id)
    
#    hola=models.execute_kw(db, uid, password,
#        'project.task', 'search_read',
#        [[['id','=',task.task_id]]])
#    task.update(hola[0])
#    print(task.reports)
#    hola=models.execute_kw(db, uid, password,
#        'x_reporte_de_actividad', 'search_read',
#        [[['id','in',task.reports]]])

#    for ho in hola:
#        print(ho.get('x_studio_fecha'))
#hola="" # limpiar output

# hola=models.execute_kw(db, uid, password,
#      'x_reporte_de_actividad', 'search_read',
#      [[['x_studio_cliente', '=', empresa]]])

# hola=models.execute_kw(db, uid, password,
#      'x_reporte_de_actividad', 'search_read',
#      [[['x_studio_cliente', 'like', empresa]]],
#      {'fields': []})

# hola=models.execute_kw(db, uid, password,
#      'x_reporte_de_actividad', 'search_read',
#      [[['x_studio_cliente', 'like', empresa]]],
#      {'fields': ['x_studio_cliente', 'x_studio_fecha', 'x_studio__parte', 'x_studio_cantidad_inspeccionada', 'x_studio_cantidad_aceptada', 'message_partner_ids']})

# hola = models.execute_kw(db, uid, password,
#      'project', 'search_read',
#      [[['message_partner_ids', 'like' , partner_id]]],
#      {'fields': ['display_name', 'partner_city', 'partner_id']})

# hola = models.execute_kw(db, uid, password,
#     'res.partner', 'search_read',
#     [[['name', 'like', empresa]]],
#     {'fields': ['name', 'id', 'comment', 'message_partner_ids']})

#print(hola)

#repAct=hola
#reporte=[]
#campos=['x_studio_cliente','x_studio_fecha', 'x_studio__parte', 'x_studio_cantidad_inspeccionada', 'x_studio_cantidad_aceptada' , 'message_partner_ids']
#campos=['display_name', 'partner_city', 'partner_id']
#campos=['name', 'id', 'comment', 'message_partner_ids']

#for x in repAct:
#    print(x)
#    reporte.append(list(map(x.get, campos)))

#print (reporte)
#print (models.execute_kw(
#    db, uid, password, 'project.task', 'fields_get',
#    [], {'attributes': ['string', 'help', 'type']}))

#hol=models.execute_kw(db, uid, password,
#    'x_reporte_de_actividad', 'search_read',
#    [[['x_studio_cliente', 'like', "4PL CALIDAD Y LOGÍSTICA DE MÉXICO S.A. DE C.V."]]],
#    {'fields': [ 'x_name', 'x_studio__parte'], 'limit': 5})
#s
#print (hol)



# url = "https://axonebackoffice-client-app-test-1924357.dev.odoo.com" #test
# db = "axonebackoffice-client-app-test-1924357" #test
# password = "63154da9232fcc0ee54cf7bc466b3c09682c0630" #test

#info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
#url, db, username, password = \
#    info['host'], info['database'], info['user'], info['password']

#print (
#    models.execute_kw(db, uid, password,
#    'res.partner', 'check_access_rights',
#    ['read'], {'raise_exception': False})
#)