import json, locale, datetime as dia, os, weasyprint,time
from datetime import datetime, date
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.template import RequestContext
from correspondencia.validador import *

# Create your views here.
locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
###################################################  inicio  #################################################

def inicio(request):
    if 'aviso' in request.session:
        aviso = request.session['aviso']
        del request.session['aviso']
    else:
        aviso = {'indicador':1, 'mensaje': ''}

    return render(request,'login/login.html', {'indicador':aviso['indicador'], 'respuesta':aviso['mensaje']})

def login(request):
    if request.method == 'POST':
        validador = FormLoginValidator(request.POST)
        validador.required = ['username', 'password']
        if validador.is_valid():
            auth_login(request, validador.acceso)
            return HttpResponseRedirect('menu')
        else:
            indicador = 0
            respuesta = validador.getMessage()
            request.session['respuesta'] = {'indicador':indicador, 'respuesta':respuesta}
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

@login_required(login_url="/")
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")
##############################################################################################################
###################################################  menu ####################################################
@login_required(login_url="/")
def menu(request):
    if 'aviso' in request.session:
        aviso = request.session['aviso']
        del request.session['aviso']

        indicador = aviso['indicador']
        mensaje = aviso['mensaje']
    else:
        indicador = 1
        mensaje = 'Bienvenido, seleccione una opción para continuar'

    return render(request, 'menu/menu.html', {'indicador': indicador, 'mensaje': mensaje})
##############################################################################################################
################################### correspondencia entrada ##################################################
@login_required(login_url="/")
def correspondencia_entrada(request):
    if request.method == 'GET':
        tipo_correspondencia = Tipo_correspondencia.objects.all().order_by('tipo')
        tipo_persona = Tipo_persona.objects.all().order_by('tipo')
        tipo_documento = Tipo_documento.objects.all().order_by('tipo')
        tipo_id = Tipo_id.objects.all().order_by('tipo')
        fecha = datetime.today()

        if Correspondencia_entrada.objects.all().exists():
            registros = Correspondencia_entrada.objects.filter(anulado=False, fecha_recibido=fecha).order_by('fecha_recibido')[::-1]
        else:
            registros = ''

        dependencia = Dependencia.objects.all().order_by('dependencia')

        if request.session.has_key('etiqueta_actual'):
            etiqueta_actual =request.session['etiqueta_actual']
        else:
            etiqueta_actual = "0"

        if 'dependencia' in request.session:
            del request.session['dependencia']

        if 'serie_documental' in request.session:
            del request.session['serie_documental']

        if 'aviso' in request.session:
            aviso = request.session['aviso']
            del request.session['aviso']

            indicador = aviso['indicador']
            mensaje = aviso['mensaje']
        else:
            indicador = 1
            mensaje = "Favor diligencie los campos solicitados"

        return render(request, 'correspondencia_entrada/correspondencia_entrada.html',{'indicador':indicador,'mensaje':mensaje,'etiqueta_actual':etiqueta_actual,
                                                                                       'tipo_personas':tipo_persona,'tipo_ids':tipo_id,
                                                                                       'dependencias':dependencia, 'procedencia':tipo_correspondencia,
                                                                                       'registros_correspondencia_entrada':registros, 'tipo_documento':tipo_documento,
                                                                                       'fecha_busqueda':fecha.strftime("%d de %B, de %Y")})

@login_required(login_url='/')
def guardar_correspondencia_entrada(request):
    if request.method == 'POST':
        try:
            nuevo_registro = Correspondencia_entrada()

            if 'dependencia_origen' in request.POST:
                if request.POST['dependencia_origen'] == 'Interna':
                    new_dep_origen = Dependencia_origen()
                    new_dep_origen.dependencia = Dependencia.objects.get(id= request.POST['dependencia_origen'])
                    new_dep_origen.save()

                    nuevo_registro.dependencia_origen = new_dep_origen

            nuevo_registro.fecha_recibido = date.today()
            nuevo_registro.hora_recibido = time.strftime("%H:%M:%S")
            nuevo_registro.tipo_correspondencia_id = request.POST['procedencia']
            nuevo_registro.remitente = Persona.objects.get(numero_id=request.POST['numero_id'])
            nuevo_registro.dependencia_id = request.POST['dependencia']
            nuevo_registro.serie_documental_id = request.POST['serie_documental']

            if 'subserie_documental' in request.POST:
                nuevo_registro.subserie_documental_id = request.POST['subserie_documental']
            if 'tipo_documental_retencion' in request.POST:
                nuevo_registro.tipo_documental_id = request.POST['tipo_documental_retencion']
            nuevo_registro.asunto = request.POST['asunto']
            if 'observacion' in request.POST:
                nuevo_registro.observacion = request.POST['observacion']

            nuevo_registro.tipo_documento = Tipo_documento.objects.get(id=request.POST['tipo_documento'])
            nuevo_registro.fecha_documento_radicado = request.POST['fecha_documento']
            nuevo_registro.numero_folios_documento = request.POST['numero_folios']

            oficinas = Usuario_x_oficina.objects.filter(usuario_id=request.user.id)

            if oficinas.exists():
                oficina = oficinas[0].oficina.oficina
                hoy = str(dia.date.today()).replace("-","")
                co = str(oficina[0])+str(nuevo_registro.tipo_correspondencia.tipo[0])
                verificacion_codigo = Consecutivo.objects.filter(correspondencia_x_oficina=co)
                if verificacion_codigo.exists():
                    consecutivo = int(verificacion_codigo[0].consecutivo) + 1
                else:
                    consecutivo = 1
                    nuevo_co = Consecutivo()
                    nuevo_co.correspondencia_x_oficina = co
                    nuevo_co.consecutivo = ''
                    nuevo_co.save()

                codigo_radicacion = str(hoy) + "-" + str(co) + str(consecutivo).zfill(8)
                nuevo_registro.numero_radicacion = codigo_radicacion

                if 'adjunto' in request.FILES:
                    nuevo_registro.archivo_digital = request.FILES['adjunto']

                nuevo_registro.usuario = Usuario.objects.get(username=request.user)
                nuevo_registro.save()

                consecutivo_agr = Consecutivo.objects.get(correspondencia_x_oficina=co)
                consecutivo_agr.consecutivo = consecutivo
                consecutivo_agr.save()

                request.session['etiqueta_actual'] = str(nuevo_registro.id)

                indicador = 2
                mensaje = "El registro ha sido guardado correctamente"
                request.session['aviso'] = {'indicador': indicador, 'mensaje': mensaje}
                return HttpResponseRedirect('correspondencia_entrada')
            else:
                indicador = 0
                mensaje = "El usuario no puede realizar registros de correspondencia, no tiene oficina asignada"
                request.session['aviso'] = {'indicador': indicador, 'mensaje': mensaje}
                return HttpResponseRedirect('correspondencia_entrada')
        except:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"
            request.session['aviso'] = {'indicador': indicador, 'mensaje': mensaje}
            return HttpResponseRedirect('correspondencia_entrada')

@login_required(login_url='/')
def correspondencia_radicado(request):
    if request.method == 'GET':
        if 'codigo_radicado' in request.GET:
            request.session['respuesta'] = {'codigo_radicado':request.GET['codigo_radicado']}
            data = {'indicador':1, 'mensaje':'La cosulta se realizo con exito'}
            return HttpResponse(json.dumps(data), content_type="application/json")

        elif 'numero_identificacion' in request.GET:
            numero_id = request.GET['numero_identificacion']
            correspondencia_entrada = Correspondencia_entrada.objects.filter(remitente__numero_id=numero_id)

            if correspondencia_entrada.exists():
                results = []
                for c in correspondencia_entrada:
                    datos ={'nombre':c.remitente.nombre,'identificacion':c.remitente.tipo_id.tipo +'. '+ c.remitente.numero_id,
                            'fecha':str(datetime.strftime(c.fecha_documento_radicado,'%d/%m/%Y')), 'asunto': c.asunto, 'codigoRadicado': c.numero_radicacion}
                    results.append(datos)
                data = {'indicador': 1, 'mensaje':'La cosulta se realizo con exito', 'registros':results}
            else:
                data = {'indicador': 0, 'mensaje': 'No se encontraton datos asociados a ese número de identificación'}

            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            if 'respuesta' in request.session:
                codigo_radicado = request.session['respuesta']
                del request.session['respuesta']

                consulta = Correspondencia_entrada.objects.filter(numero_radicacion=codigo_radicado['codigo_radicado'])
                if consulta.exists():
                    correspondencia_entrada = consulta[0]
                    indicador = 2
                    mensaje = 'La consulta se ha realizado correctamente'
                else:
                    correspondencia_entrada = ""
                    indicador = 0
                    mensaje = 'No se han encontrado registros con ese número de radicado'
            else:
                indicador = 1
                mensaje = 'Favor ingrese uno de los dos datos solicitados para realizar la consulta'
                correspondencia_entrada = ""

            return render(request, 'correspondencia_entrada/correspondencia_radicado.html',{'indicador':indicador,'mensaje':mensaje,
                                                                                  'registro':correspondencia_entrada})
    else:
        HttpResponseRedirect('menu')

@login_required(login_url='/')
def editar_correspondencia_entrada(request):
    if request.method == 'GET':
        try:
            registro = Correspondencia_entrada.objects.filter(id=request.GET['registro'])

            if registro.exists():
                ids = registro[0].id
                procedencia = registro[0].tipo_correspondencia.id
                dependencia = registro[0].dependencia.id
                id_serie_documental = registro[0].serie_documental.id
                nombre_serie_documental = registro[0].serie_documental.serie_documental
                id_subserie_documental = registro[0].subserie_documental.id
                nombre_subserie_documental = registro[0].subserie_documental.subserie_documental
                if registro[0].tipo_documental != None:
                    id_tipo_documental = registro[0].tipo_documental.id
                    nombre_tipo_documental = registro[0].tipo_documental.tipo_documental
                else:
                    id_tipo_documental = ""
                    nombre_tipo_documental = ""
                asunto = registro[0].asunto
                observacion = registro[0].observacion
                tipo_docuento = registro[0].tipo_documento.id
                fecha_documento = str(registro[0].fecha_documento_radicado.strftime('%Y-%m-%d'))
                folios = registro[0].numero_folios_documento

            indicador = 1
            data = {'ids':ids,'indicador': indicador,'procedencia': procedencia, 'dependencia': dependencia,
                    'idSerieDocumental': id_serie_documental,'nombreSerieDocumental':nombre_serie_documental,
                    'idSubserieDocumental':id_subserie_documental,'nombreSubserieDocuental':nombre_subserie_documental,
                    'idTipoDocumental':id_tipo_documental,'nombreTipoDocumental':nombre_tipo_documental,'asunto':asunto,
                    'observacion':observacion,'tipo_documento':tipo_docuento, 'fecha_documento':fecha_documento,
                    'folios':folios}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"
            data = {'indicador': indicador, 'mensaje': mensaje}
            return HttpResponse(json.dumps(data), content_type="application/json")

    if request.method == 'POST':
        try:
            registro = Correspondencia_entrada.objects.filter(id=request.POST['editar_correspondencia_entrada'])

            if registro.exists():
                editar_entrada = Correspondencia_entrada.objects.get(id=request.POST['editar_correspondencia_entrada'])

                editar_entrada.tipo_correspondencia.id = request.POST['editar_procedencia']
                editar_entrada.dependencia = Dependencia.objects.get(id=request.POST['editar_dependencia'])
                if 'editar_serie_documental' in request.POST:
                    editar_entrada.serie_documental = Serie_documental_Retencion.objects.get(id=request.POST['editar_serie_documental'])
                if 'editar_subserie_documental' in request.POST:
                    editar_entrada.subserie_documental = Subserie_documental_Retencion.objects.get(id=request.POST['editar_subserie_documental'])
                if 'editar_tipo_documental_retencion' in request.POST:
                    editar_entrada.tipo_documental = Tipo_documental_Retencion.objects.get(id=request.POST['editar_tipo_documental_retencion'])
                editar_entrada.asunto = request.POST['editar_asunto']
                editar_entrada.observacion = request.POST['editar_observacion']
                editar_entrada.tipo_documento = Tipo_documento.objects.get(id=request.POST['editar_tipo_documento'])
                editar_entrada.fecha_documento = request.POST['editar_fecha_documento']
                editar_entrada.numero_folios_documento = request.POST['editar_numero_folios']
                editar_entrada.save()

                indicador = 2
                mensaje = "El regitro ha sido modificado exitosamente"
            else:
                indicador = 0
                mensaje = "El registro ya no se encuentra disponible para su edición"

        except:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"

        request.session['aviso'] = {'indicador': indicador, 'mensaje': mensaje}
        return HttpResponseRedirect('correspondencia_entrada')

@login_required(login_url='/')
def anular_correspondencia_entrada(request):
    if request.method == 'GET':
        try:
            correspondencia = Correspondencia_entrada.objects.filter(id=request.GET['registro'], anulado=False)

            if correspondencia.exists():
                correspondencia_act = correspondencia[0]
                correspondencia_act.anulado = True
                correspondencia_act.save()

                data = {'indicador':2, 'mensaje':"El registro ha sido anulado correctamente"}
            else:
                data = {'indicador':0, 'mensaje':"El registro ya ha sido anulado"}
        except:
            data = {'indicador': 0, 'mensaje':"Ha ocurrido un error interno en el servidor"}

        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required(login_url='/')
def escaneo_documentos(request):
    if request.method == 'POST':
        if 'fecha' in request.POST:
            fecha = request.POST['fecha']
            correspondencia_entrada = Correspondencia_entrada.objects.filter(fecha_recibido=fecha, archivo_digital='', anulado=False)

            indicador = 2
            if len(correspondencia_entrada) == 1:
                mensaje = 'Se han encontrado ' + str(len(correspondencia_entrada)) + ' registro, sin adjunto'
            elif len(correspondencia_entrada) == 0:
                indicador = 0
                mensaje = 'No se han encontrado registros, con esta fecha'
            else:
                mensaje = 'Se han encontrado ' + str(len(correspondencia_entrada)) + ' registros, sin adjunto'

        elif 'adjunto' in request.FILES and 'adjunto_id' in request.POST:
            corresp_entrada = Correspondencia_entrada.objects.get(id=request.POST['adjunto_id'])
            corresp_entrada.archivo_digital = request.FILES['adjunto']
            corresp_entrada.save()

            data = {'indicador': 2,'mensaje': "El archivo ha sido subido correctamente"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {'indicador': 0, 'mensaje': "no se han obtenido datos para su almacenamiento, comuniquese con el área de sistemas"}
            return HttpResponse(json.dumps(data), content_type="application/json")

    elif request.method == 'GET':
        correspondencia_entrada = ""
        indicador = 1
        mensaje = "Escaneo de documentos radicados, BIENVENIDO"
    else:
        HttpResponseRedirect('')

    return render(request, 'correspondencia_entrada/escaneo_documentos.html',{'indicador':indicador,'mensaje':mensaje,
                                                                              'registros':correspondencia_entrada})

@login_required(login_url='/')
def etiqueta_PDF(request):
    dato = None
    if request.method == 'GET':
        if 'id_registro' in request.GET:
            id_registro = request.GET['id_registro']
            consulta = Correspondencia_entrada.objects.filter(id=id_registro)

            if consulta.exists():
                dato = consulta[0]

                fecha_recibido = datetime.strptime(str(dato.fecha_recibido), "%Y-%m-%d").strftime("%d/%m/%Y")
                fecha_documento = datetime.strptime(str(dato.fecha_documento_radicado), "%Y-%m-%d").strftime("%d/%m/%Y")

                template = get_template('correspondencia_entrada/etiqueta.html')
                context = {'fecha_recibido':fecha_recibido,'hora_recibido':(dato.hora_recibido),
                           'numero_radicacion':dato.numero_radicacion,'remitente':dato.remitente.nombre,'numero_id':dato.remitente.numero_id,
                           'dependencia':dato.dependencia.dependencia,'asunto':dato.asunto,'fecha_documento': fecha_documento,
                           'tipo_documento':(dato.tipo_documento.tipo), 'folios':str(dato.numero_folios_documento), 'tipo_correspondencia':dato.tipo_correspondencia.tipo}
                html = template.render(context)
                response = HttpResponse(content_type='application/pdf')
                weasyprint.HTML(string=html,base_url=request.build_absolute_uri()).write_pdf(response)

                return response
            else:
                indicador = 0
                mensaje = 'La etiqueta no puede ser generada, favor use el boton de la tabla'
                request.session['respuesta'] = {'indicador': indicador, 'mensaje': mensaje}
                return HttpResponseRedirect('correspondencia_entrada')
        else:
            indicador = 0
            mensaje = 'EL registro ya no esta disponible, actualice la pagina para continuar'
            request.session['respuesta'] = {'indicador': indicador, 'mensaje': mensaje}
            return HttpResponseRedirect('correspondencia_entrada')
    else:
        indicador = 0
        mensaje = 'No se ha relizado un registro para generar la etiqueta'
        request.session['respuesta'] = {'indicador':indicador, 'mensaje':mensaje}
        return HttpResponseRedirect('correspondencia_entrada')
##############################################################################################################
################################################ reportes ####################################################
@login_required(login_url='/')
def reporte_corresp_ent(request):
    if request.method == 'GET':
        dependencia = Dependencia.objects.all().order_by('dependencia')
        fecha = ''

        if 'aviso' in request.session:
            aviso = request.session['aviso']
        else:
            aviso = {'indicador':1,'mensaje':"Seleccione un rago de fechas para realizar la busqueda"}

        if 'fecha' in request.GET and 'dependencia' in request.GET:
            registros = Correspondencia_entrada.objects.filter(fecha_recibido=request.GET['fecha'],anulado=False, dependencia=request.GET['dependencia'])
            if registros.exists():
                request.session['reporte_corresp_ent'] = {'fecha':request.GET['fecha'],'dependencia':request.GET['dependencia']}
                fecha = datetime.strptime(request.GET['fecha'],"%Y-%m-%d").strftime("%-d de %B, de %Y")
                aviso = {'indicador': 2, 'mensaje': "La consulta se ha realizado correctamente"}
            else:
                aviso = {'indicador': 0, 'mensaje': "No se encontraron registros con las fechas seleccionadas"}
        else:
            registros = ""

        return render(request, 'reportes/reporte_corresp_ent_dep.html',{'indicador':aviso['indicador'],'mensaje':aviso['mensaje'], 'registros':registros, 'dependencia':dependencia, 'fecha':fecha})

@login_required(login_url='/')
def reporte_corresp_ent_PDF(request):
    dato = None
    if request.method == 'GET':
        if 'reporte_corresp_ent' in request.session:
            datos = request.session['reporte_corresp_ent']
            del request.session['reporte_corresp_ent']
            registros = Correspondencia_entrada.objects.filter(fecha_recibido=(datos['fecha']),
                                                                          anulado=False, dependencia=datos['dependencia'])
            dependencia = registros[0].dependencia.dependencia

            if registros.exists():
                fecha_hoy = datetime.now()
                fecha_reporte = datetime.strptime(datos['fecha'], "%Y-%m-%d").strftime("%B %-d de %Y")

                template = get_template('reportes/report_corresp_ent_pdf.html')
                context = {'fecha_hoy':fecha_hoy,'fecha_reporte': fecha_reporte,'registros':registros,'dependencia':dependencia}
                html = template.render(context)
                response = HttpResponse(content_type='application/pdf')
                weasyprint.HTML(string=html,base_url=request.build_absolute_uri()).write_pdf(response)

                return response
            else:
                request.session['aviso'] = {'indicador': 0, 'mensaje': 'No se enviaron datos para generar el reporte, por favor actualice la página'}
                return HttpResponseRedirect('corresp_entrada')
        else:
            request.session['aviso'] = {'indicador': 0,
                                        'mensaje': 'No se enviaron datos para generar el reporte, por favor actualice la página'}
            return HttpResponseRedirect('corresp_entrada')
    else:
        return HttpResponseRedirect('menu')

###############################################################################################################
################################################ usuario ######################################################
@login_required(login_url='/')
def usuario(request):
    usuarios = Usuario.objects.all().order_by('username').exclude(username='administrador')
    perfil = Group.objects.all().order_by('name')
    oficina = Oficina.objects.all().order_by('oficina')

    if 'aviso' in request.session:
        aviso = request.session['aviso']
        del request.session['aviso']

        indicador = aviso['indicador']
        mensaje = aviso['mensaje']
    else:
        indicador = 1
        mensaje = "Gestión de usuarios, por favor diligencie todos los campos"

    return render(request, 'sistema/crear_usuarios.html',
                  {'perfil': perfil, 'indicador': indicador, 'mensaje': mensaje, 'usuarios': usuarios, 'oficina':oficina})

@login_required(login_url='/')
def guardar_usuario(request):
    if request.method == 'POST':
        try:
            validator = FormRegistroValidator(request.POST)
            validator.required = ['username', 'email', 'password', 'perfil']
            import pdb; pdb.set_trace()
            if validator.is_valid():
                usuario = User()
                usuario.first_name = request.POST['firstname'].title()
                usuario.last_name = request.POST['lastname'].title()
                usuario.username = request.POST['username']
                usuario.email = request.POST['email']
                usuario.password = make_password(request.POST['password'])
                usuario.is_active = True
                perfil = Group.objects.get(id=request.POST['perfil'])
                usuario.save()
                usuario.groups.add(perfil)
                usuario.save()

                usuario_x_oficina = Usuario_x_oficina()
                usuario_x_oficina.usuario_id = usuario.id
                if request.POST['oficina'] != '':
                    usuario_x_oficina.oficina_id = request.POST['oficina']
                else:
                    usuario_x_oficina.oficina_id = 1
                usuario_x_oficina.save()

                indicador = 1
                mensaje = "El usuario ha sido Guardado exitosamente"
                request.session['aviso'] = {'indicador': indicador, 'mensaje': mensaje}
                return HttpResponseRedirect('usuario')
            else:
                indicador = 0
                mensaje = validator.getMessage()
                request.session['aviso'] = {'indicador': indicador, 'mensaje': mensaje}
                return HttpResponseRedirect('usuario')
        except:
            indicador = 0
            mensaje = 'Ha ocuurido un error en el sistema, comuniquese con el área de informatica'
            request.session['respuesta'] = {'indicador': indicador, 'mensaje': mensaje}
            return HttpResponseRedirect('menu')
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/')
def editar_usuario(request):
    if request.method == 'GET':
        try:
            obj = get_object_or_404(User,id=request.GET['id'])
            ids = obj.id
            username = obj.username
            nombres = obj.first_name
            apellidos = obj.last_name
            email = obj.email
            perfil = obj.groups.through.objects.get(user_id=obj.id)
            oficina = Usuario_x_oficina.objects.get(usuario_id=obj.id)
            data = {'ids':ids, 'username':username, 'nombres': nombres, 'apellidos':apellidos,
                    'email':email, 'perfil':perfil.group.id,'oficina': oficina.oficina.id}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"
            data = {'indicador': indicador, 'mensaje': mensaje}
            return HttpResponse(json.dumps(data), content_type="application/json")

    if request.method == 'POST':
        try:
            usuario = get_object_or_404(User,id=request.POST['editar_usuario'])
            usuario.first_name = request.POST['editar_nombres']
            usuario.last_name = request.POST['editar_apellidos']
            usuario.email = request.POST['editar_email']
            usuario.save()
            usuario.groups.through.objects.filter(user_id=usuario.id).delete()
            usuario.groups.add(Group.objects.get(pk = request.POST['editar_perfil']))
            Usuario_x_oficina.objects.filter(usuario_id=usuario.id).delete()
            usuario_x_oficina = Usuario_x_oficina()
            usuario_x_oficina.usuario_id = usuario.id
            usuario_x_oficina.oficina_id = request.POST['editar_oficina']
            usuario_x_oficina.save()
            indicador = 2
            mensaje = "El regitro ha sido modificado exitosamente"
        except:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"

        request.session['aviso'] = {'indicador': indicador, 'mensaje': mensaje}
        return HttpResponseRedirect('usuario')

@login_required(login_url='/')
def inhabilitar_usuario(request):
    if request.method == 'GET':
        if 'id_usuario' in request.GET:
            usuario = Usuario.objects.get(id=request.GET['id_usuario'])
            usuario.is_active = False
            usuario.save()

            data = {'indicador':2, 'mensaje':'El usuario ha sido inhabilitado'}
        else:
            data = {'indicador': 0, 'mensaje': 'No se han encontrado datos para realizar la consulta, por favor actualice la pagina'}

        return HttpResponse(json.dumps(data), content_type="application/json")

    else:
        request.session['aviso'] = {'indicador': 0,
                                    'mensaje': 'Se ha detectado un error, por favor actualice la página'}
        return HttpResponseRedirect('menu')

##############################################################################################################
####################################### tablas de retencion ##################################################
@login_required(login_url='/')
def tablas_retencion(request):
    dependencia = Dependencia.objects.all().order_by('dependencia')
    series = Serie_documental_Retencion.objects.all().values_list('id','codigo','serie_documental').order_by('serie_documental')
    subseries = Subserie_documental_Retencion.objects.all().values_list('id', 'codigo','subserie_documental').order_by('subserie_documental')
    tipos = Tipo_documental_Retencion.objects.all().values_list('id','tipo_documental').order_by('tipo_documental')
    agrupaciones = Agr_retencion_documental.objects.all()\
        .values_list('id','dependencia__dependencia','serie_documental__serie_documental','subserie_documental__subserie_documental', 'tipo_documental__tipo_documental').order_by('dependencia')

    if 'aviso' in request.session:
        aviso = request.session['aviso']
        del request.session['aviso']

        indicador = aviso['indicador']
        mensaje = aviso['mensaje']
    else:
        indicador = 1
        mensaje = "Bienvenido a la pagina de administación de los datos de retención documental"

    return render(request, 'sistema/tablas_retencion.html',{'indicador':indicador,'mensaje':mensaje,'series':series,
                                                             'dependencias':dependencia, 'subseries':subseries,
                                                             'tipos':tipos, 'agrupaciones':agrupaciones})

@login_required(login_url='/')
def buscar_agr_documental(request):
    if request.method == 'GET':
        if 'dependencia' in request.GET:
            dependencia = request.GET['dependencia']
            serie_documental = Agr_retencion_documental.objects.filter(dependencia_id=dependencia)\
                .values_list('serie_documental', 'serie_documental__codigo', 'serie_documental__serie_documental').distinct()

            list = []
            for i in serie_documental:
                    list.append({'id': i[0], 'codigo':i[1],'nombre': i[2]})

            cont = len(serie_documental)
            request.session['dependencia'] = dependencia

        elif 'serie_documental' in request.GET:
            serie_documental = request.GET['serie_documental']

            if 'dependencia' in request.session:
                subserie_documental = Agr_retencion_documental.objects.filter\
                    (dependencia_id=request.session['dependencia'],serie_documental_id=serie_documental) \
                    .values_list('subserie_documental__id', 'subserie_documental__codigo',
                                 'subserie_documental__subserie_documental').distinct()
            else:
                subserie_documental = ""

            list = []
            for i in subserie_documental:
                list.append({'id': i[0], 'codigo': i[1], 'nombre': i[2]})

            cont = len(serie_documental)
            request.session['serie_documental'] = serie_documental

        elif 'subserie_documental' in request.GET:
            subserie_documental = request.GET['subserie_documental']

            if 'serie_documental' in request.session:
                tipo_documental = Agr_retencion_documental.objects.filter\
                    (dependencia_id=request.session['dependencia'],serie_documental_id=request.session['serie_documental'], subserie_documental_id=subserie_documental) \
                    .values_list('tipo_documental__id', 'tipo_documental__tipo_documental').distinct()
            else:
                tipo_documental = ""

            list = []
            for i in tipo_documental:
                list.append({'id': i[0], 'nombre': i[1]})

            cont = len(tipo_documental)
        else:
            list = []
            cont = len(list)

        if cont == 0:
            indicador = 0
            mensaje = "Error en el servidor, comuniquese con el área de sistemas"
        else:
            indicador = 1
            mensaje = ""

        output = {'indicador': indicador, 'mensaje':mensaje, 'list': list}
        return HttpResponse(json.dumps(output), content_type="application/json")

@login_required(login_url='/')
@transaction.atomic
def guardar_dependencia(request):
    if request.method == 'POST':
        try:
            codigo = request.POST['codigo_dependencia']
            dependencia = request.POST['agr_dependencia'].title()

            if not Dependencia.objects.filter(codigo=codigo).exists() and not Dependencia.objects.filter(dependencia=dependencia).exists():
                agr_dependencia = Dependencia()
                agr_dependencia.codigo = codigo
                agr_dependencia.dependencia = dependencia
                agr_dependencia.save()

                indicador = 2
                mensaje = "La dependencia se ha guardado exitosamente"
                return respuesta_tablas_retencion(indicador, mensaje, request)
            else:
                indicador = 0
                mensaje = "Los datos ingresados encuentran registrados en la base de datos"
                return respuesta_tablas_retencion(indicador, mensaje, request)
        except:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"
            return respuesta_tablas_retencion(indicador, mensaje, request)


@login_required(login_url='/')
@transaction.atomic
def guardar_serie_documental(request):
    if request.method == 'POST':
        try:
            codigo = request.POST['codigo_serie_documental']
            serie_documental = request.POST['agr_serie_documental'].title()

            if not Serie_documental_Retencion.objects.filter(serie_documental=serie_documental).exists() or \
                    not Serie_documental_Retencion.objects.filter(codigo=codigo).exists():
                agr_serie_documental = Serie_documental_Retencion()
                agr_serie_documental.codigo = codigo
                agr_serie_documental.serie_documental = serie_documental
                agr_serie_documental.save()

                indicador = 2
                mensaje = "La serie documental se ha guardado exitosamente"

            else:
                indicador = 0
                mensaje = "Los datos ingresados se encuentran registrados en la base de datos"

        except:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"

        return respuesta_tablas_retencion(indicador, mensaje, request)

@login_required(login_url='/')
@transaction.atomic
def guardar_subserie_documental(request):
    if request.method == 'POST':
        try:
            codigo = request.POST['codigo']
            subserie_documental = request.POST['agr_subserie_documental']

            if not Subserie_documental_Retencion.objects.filter(subserie_documental=subserie_documental).exists():
                agr_subserie_documental = Subserie_documental_Retencion()
                agr_subserie_documental.codigo = codigo
                agr_subserie_documental.subserie_documental = subserie_documental
                agr_subserie_documental.save()

                indicador = 2
                mensaje = "La subserie documental se ha guardado exitosamente"
            else:
                indicador = 0
                mensaje = "Los datos ingresados se encuentran registrados en la base de datos"

        except:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"

        return respuesta_tablas_retencion(indicador, mensaje, request)

@login_required(login_url='/')
@transaction.atomic
def guardar_tipo_documental(request):
    if request.method == 'POST':
        try:
            tipo_documental = request.POST['agr_tipo_documental']

            if not Tipo_documental_Retencion.objects.filter(tipo_documental = tipo_documental).exists():
                agr_tipo_documental = Tipo_documental_Retencion()
                agr_tipo_documental.tipo_documental = tipo_documental
                agr_tipo_documental.save()

                indicador = 2
                mensaje = "El tipo documental se ha guardado exitosamente"
            else:
                indicador = 0
                mensaje = "Los datos ingresados encuentran registrados en la base de datos"

        except:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"

        return respuesta_tablas_retencion(indicador, mensaje, request)


def respuesta_tablas_retencion(indicador, mensaje, request):
    request.session['aviso'] = {'indicador': indicador, 'mensaje': mensaje}
    return HttpResponseRedirect('tablas_retencion')
##############################################################################################################
############################################## remitente #####################################################
@login_required(login_url='/')
def buscar_remitente(request):
    try:
        if 'numero_id' in request.GET:
            numero_id = request.GET['numero_id']
            remitente = Persona.objects.get(numero_id=numero_id)
            tipo_id = remitente.tipo_id.tipo
            tipo_persona = str(remitente.tipo_persona.tipo).title()
            indicador = 1
        elif 'identificador' in request.GET:
            id = request.GET['identificador']
            remitente = Persona.objects.get(id=id)
            tipo_id = remitente.tipo_id.id
            tipo_persona = remitente.tipo_persona.id
            indicador = 3
        else:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"
            output = {'indicador': indicador, 'mensaje': mensaje}
            return HttpResponse(json.dumps(output), content_type="application/json")

        output = {'indicador':indicador, 'id':remitente.id, 'nombre': remitente.nombre, 'tipo_persona':tipo_persona,
                   'tipo_id':tipo_id, 'numero_id':remitente.numero_id,
                   'telefono': remitente.telefono, 'direccion':str(remitente.direccion).title(), 'email':remitente.email}
        return HttpResponse(json.dumps(output),  content_type="application/json")

    except Persona.DoesNotExist:
        indicador = 0
        mensaje = "Favor diligenciar los campos para continuar"
        output = {'indicador': indicador, 'mensaje':mensaje}
        return HttpResponse(json.dumps(output),  content_type="application/json")

@login_required(login_url='/')
@transaction.atomic
def guardar_remitente(request):
    if request.method == 'POST':
        try:
            if request.POST['tipo_operacion'] == 'edicion' and 'edicion_id' in request.POST:
                if request.POST['edicion_id'] != "":
                    nuevo = Persona.objects.get(id=request.POST['edicion_id'])
                    mensaje = "Los datos de la persona han sido editados correctamente"
                else:
                    output = {'indicador': 0, 'mensaje': "Se ha encontrado un error, por favor actualice la página"}
                    return HttpResponse(json.dumps(output), content_type="application/json")
            elif request.POST['tipo_operacion'] == 'nuevo' and Persona.objects.filter(numero_id=request.POST['numero_id_remitente']).exists():
                output = {'indicador': 0, 'mensaje': "La persona ya existe en la base de datos"}
                return HttpResponse(json.dumps(output), content_type="application/json")
            elif request.POST['tipo_operacion'] == 'nuevo' and not Persona.objects.filter(numero_id=request.POST['numero_id_remitente']).exists():
                nuevo = Persona()
                mensaje = "La persona ha sido creada correctamente"
            else:
                output = {'indicador': 0, 'mensaje': "Se ha encontrado un error, por favor actualice la página"}
                return HttpResponse(json.dumps(output), content_type="application/json")

            nuevo.nombre = request.POST['nombre_remitente']
            nuevo.tipo_persona_id = request.POST['tipo_persona_remitente']
            nuevo.tipo_id_id = request.POST['tipo_id_remitente']
            nuevo.numero_id = request.POST['numero_id_remitente']
            nuevo.direccion = request.POST['direccion_remitente']
            nuevo.telefono = request.POST['telefono_remitente']
            nuevo.email = request.POST['email_remitente']
            nuevo.usuario_id = request.user.id
            nuevo.save()

            indicador = 2
            output = {'indicador': indicador, 'mensaje': mensaje}
            return HttpResponse(json.dumps(output), content_type="application/json")
        except:
            indicador = 0
            mensaje = "Ha ocurrido un error interno en el servidor"
            output = {'indicador': indicador, 'mensaje': mensaje}
            return HttpResponse(json.dumps(output), content_type="application/json")
    else:
        return HttpResponseRedirect('menu')
##############################################################################################################
