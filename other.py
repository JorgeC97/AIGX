import xmlrpc.client
from datetime import datetime

from numpy import append

c_username = "hjuan@aigx.mx"
c_password = "Axone$odoo$"

url = "http://axhs.odoo.com"

db = "axonebackoffice-aigx-main-1924299"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

uid3 = common.authenticate(db, "arturo.gonzalez@faurecia.com" , "123456", {})

uid2 = common.authenticate(db, "cabralestest@aigx.mx" , "jdetest", {})

c="jdetest"

uid1 = common.authenticate(db, "hjuan@aigx.mx" , "Axone$odoo$", {})

uid = common.authenticate(db, c_username, c_password, {})

userId = models.execute_kw(db, uid, c_password,'res.partner', 'search_read',[[['user_ids','=',uid1]]])[0].get('id')
print(uid3)

print(uid)

print(userId)

project='C21027'

#rojects = models.execute_kw(db, uid2, c,
#        'project.project', 'search_read',
#        [[['message_is_follower','=',True]]],
#        {'fields': ['id','name','user_id', 'message_is_follower']})
#print(projects)

reportes = models.execute_kw(db, uid, c_password,
        'x_reporte_de_actividad', 'search_read',
        [[['x_studio_contrato', '=', project]]],
        {'fields': 
        [
            'x_studio_fecha',
            'x_studio__parte',  
            'x_studio_cantidad_inspeccionada', 
            'x_studio_cantidad_rechazada',
            'x_studio_cantidad_retrabajada',
            'x_studio_cantidad_aceptada'
            ]})

for x in reportes:
        if not x['x_studio_fecha']:
                reportes.remove(x)

hasta='2022-02-17'
desde='2022-02-10'

reportesS=[]

for x in reportes:
        if x['x_studio_fecha'] >= desde and x['x_studio_fecha'] <= hasta:
                reportesS.append(x)

reportesO = sorted(reportesS, key=lambda d: d['x_studio_fecha'])

x=len(reportesO)
numD=0
cont=0

reportesF=[]

while cont<x:
        if cont==0:
            reportesF.append({'x_studio_fecha':reportesO[cont].get('x_studio_fecha')})
            reportesF[numD]['x_studio__parte']=reportesO[cont]['x_studio__parte']
            reportesF[numD]['x_studio_cantidad_inspeccionada']=reportesO[cont]['x_studio_cantidad_inspeccionada']
            reportesF[numD]['x_studio_cantidad_rechazada']=reportesO[cont]['x_studio_cantidad_rechazada']
            reportesF[numD]['x_studio_cantidad_retrabajada']=reportesO[cont]['x_studio_cantidad_retrabajada']
            reportesF[numD]['x_studio_cantidad_aceptada']=reportesO[cont]['x_studio_cantidad_aceptada']
            cont+=1
        elif reportesO[cont].get('x_studio_fecha') != reportesO[cont-1].get('x_studio_fecha'):
            numD+=1
            reportesF.append({'x_studio_fecha':reportesO[cont].get('x_studio_fecha')})
            reportesF[numD]['x_studio__parte']=reportesO[cont]['x_studio__parte']
            reportesF[numD]['x_studio_cantidad_inspeccionada']=reportesO[cont]['x_studio_cantidad_inspeccionada']
            reportesF[numD]['x_studio_cantidad_rechazada']=reportesO[cont]['x_studio_cantidad_rechazada']
            reportesF[numD]['x_studio_cantidad_retrabajada']=reportesO[cont]['x_studio_cantidad_retrabajada']
            reportesF[numD]['x_studio_cantidad_aceptada']=reportesO[cont]['x_studio_cantidad_aceptada']
            cont+=1
        else:
            reportesF[numD]['x_studio__parte'] += ((','+reportesO[cont]['x_studio__parte']) if reportesO[cont]['x_studio__parte'] else '')
            reportesF[numD]['x_studio_cantidad_inspeccionada']+= (reportesO[cont]['x_studio_cantidad_inspeccionada'] if reportesO[cont]['x_studio__parte'] else 0)
            reportesF[numD]['x_studio_cantidad_rechazada']+= (reportesO[cont]['x_studio_cantidad_rechazada'] if reportesO[cont]['x_studio__parte'] else 0)
            reportesF[numD]['x_studio_cantidad_retrabajada']+= (reportesO[cont]['x_studio_cantidad_retrabajada'] if reportesO[cont]['x_studio__parte'] else 0)
            reportesF[numD]['x_studio_cantidad_aceptada']+= (reportesO[cont]['x_studio_cantidad_aceptada'] if reportesO[cont]['x_studio__parte'] else 0)
            cont+=1

for x in reportesO:
        print(x)
for x in reportesF:
        print(x)
        print(x['x_studio_fecha'])

#for x in nreportes:
#        print(x['x_studio_fecha'])


#@csrf_exempt
#def readProjects(request):
    
#    #uid = request.session.get('uid')
#    #password = request.session.get('password')
#    sid = request.GET.get('sid','')
#    if(sid != ''):
#        session = SessionStore(session_key=request.GET.get('sid',''))
#    else:
#        session = request.session
#    partnerId = session.get('partnerId', False)
#    if(partnerId is not False):
#       # projects = models.execute_kw(db, uid, password,
#        projects = models.execute_kw(db, master_uid, master_password,
#       # 'project.project', 'search_read',
#        [[['partner_id','=',partnerId]]],
#        #[[['message_is_follower','=',True]]],
#        {'fields': ['id','name']})
#        #{'fields': ['id','name','user_id', 'message_is_follower']})
#        print(projects)
#        projectsFound = { }
#        projectsFound['items'] = projects
#        return JsonResponse(projectsFound)
#    return HttpResponse("Not logged In")