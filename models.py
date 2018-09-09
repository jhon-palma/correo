# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AgrupacionTablasRetencion(models.Model):
    dependencia = models.ForeignKey('DependenciaAlcaldia', models.DO_NOTHING)
    serie_documental = models.ForeignKey('SerieDocumentalRetencion', models.DO_NOTHING)
    subserie_documental = models.ForeignKey('SubserieDocumentalRetencion', models.DO_NOTHING)
    tipo_documental = models.ForeignKey('TipoDocumentalRetencion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'AGRUPACION_TABLAS_RETENCION'


class Consecutivo(models.Model):
    correspondencia_x_oficina = models.CharField(max_length=3)
    consecutivo = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'CONSECUTIVO'


class CopiaCorrespondencia(models.Model):
    correspondencia = models.ForeignKey('CorrespondenciaEntrada', models.DO_NOTHING)
    dependencia = models.ForeignKey('DependenciaAlcaldia', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'COPIA_CORRESPONDENCIA'


class CorrespondenciaEntrada(models.Model):
    fecha_recibido = models.DateField()
    hora_recibido = models.TimeField()
    numero_radicacion = models.CharField(max_length=30)
    correspondencia_x_oficina = models.CharField(max_length=2)
    asunto = models.CharField(max_length=200)
    observacion = models.TextField(blank=True, null=True)
    fecha_documento_radicado = models.DateField()
    numero_folios_documento = models.CharField(max_length=4)
    archivo_digital = models.CharField(max_length=100)
    visualizado = models.IntegerField()
    anulado = models.IntegerField()
    dependencia = models.ForeignKey('DependenciaAlcaldia', models.DO_NOTHING)
    dependencia_origen = models.ForeignKey('DependenciaOrigen', models.DO_NOTHING, blank=True, null=True)
    remitente = models.ForeignKey('Persona', models.DO_NOTHING)
    serie_documental = models.ForeignKey('SerieDocumentalRetencion', models.DO_NOTHING)
    subserie_documental = models.ForeignKey('SubserieDocumentalRetencion', models.DO_NOTHING, blank=True, null=True)
    tipo_correspondencia = models.ForeignKey('TipoCorrespondencia', models.DO_NOTHING)
    tipo_documental = models.ForeignKey('TipoDocumentalRetencion', models.DO_NOTHING, blank=True, null=True)
    tipo_documento = models.ForeignKey('TipoDocumento', models.DO_NOTHING)
    usuario = models.ForeignKey('AuthUser', models.DO_NOTHING)
    copia = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'CORRESPONDENCIA_ENTRADA'


class CorrespondenciaSalida(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    fecha_documento = models.DateField()
    fecha_envio = models.DateField()
    asunto = models.CharField(max_length=200)
    observacion = models.TextField(blank=True, null=True)
    numero_folios_documento = models.CharField(max_length=4)
    numero_guia = models.CharField(max_length=30)
    archivo_adjunto = models.CharField(max_length=100)
    dependencia = models.ForeignKey('DependenciaAlcaldia', models.DO_NOTHING)
    empresa_mensajeria = models.ForeignKey('EmpresaMensajeria', models.DO_NOTHING)
    persona = models.ForeignKey('Persona', models.DO_NOTHING)
    serie_documental = models.ForeignKey('SerieDocumentalRetencion', models.DO_NOTHING)
    subserie_documental = models.ForeignKey('SubserieDocumentalRetencion', models.DO_NOTHING, blank=True, null=True)
    tipo_correspondencia = models.ForeignKey('TipoCorrespondencia', models.DO_NOTHING)
    tipo_documental = models.ForeignKey('TipoDocumentalRetencion', models.DO_NOTHING, blank=True, null=True)
    tipo_documento = models.ForeignKey('TipoDocumento', models.DO_NOTHING)
    usuario = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'CORRESPONDENCIA_SALIDA'


class DependenciaAlcaldia(models.Model):
    codigo = models.CharField(max_length=4)
    dependencia = models.TextField()

    class Meta:
        managed = False
        db_table = 'DEPENDENCIA_ALCALDIA'


class DependenciaOrigen(models.Model):
    dependencia = models.ForeignKey(DependenciaAlcaldia, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'DEPENDENCIA_ORIGEN'


class EmpresaMensajeria(models.Model):
    nombre = models.CharField(max_length=120)
    numero_id = models.CharField(max_length=20)
    direccion = models.TextField()
    telefono = models.CharField(max_length=100)
    pagina_web = models.CharField(max_length=20)
    tipo_id = models.ForeignKey('TipoId', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'EMPRESA_MENSAJERIA'


class EventoCorrespondenciaEntrada(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    evento_realizado = models.CharField(max_length=100)
    correspondencia = models.ForeignKey(CorrespondenciaEntrada, models.DO_NOTHING)
    usuario = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'EVENTO_CORRESPONDENCIA_ENTRADA'


class LecturaCorrespondencia(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    documento_fisico = models.IntegerField()
    documento_virtual = models.IntegerField()
    observacion = models.TextField()
    correspondencia = models.ForeignKey(CorrespondenciaEntrada, models.DO_NOTHING)
    usuario = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'LECTURA_CORRESPONDENCIA'


class OficinaRecepcionCorrespondencia(models.Model):
    codigo = models.CharField(max_length=3)
    oficina = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'OFICINA_RECEPCION_CORRESPONDENCIA'


class Persona(models.Model):
    nombre = models.CharField(max_length=120)
    numero_id = models.CharField(unique=True, max_length=20)
    direccion = models.TextField()
    telefono = models.CharField(max_length=18)
    email = models.CharField(max_length=254)
    tipo_id = models.ForeignKey('TipoId', models.DO_NOTHING)
    tipo_persona = models.ForeignKey('TipoPersona', models.DO_NOTHING)
    usuario = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'PERSONA'


class SerieDocumentalRetencion(models.Model):
    codigo = models.CharField(max_length=4)
    serie_documental = models.TextField()

    class Meta:
        managed = False
        db_table = 'SERIE_DOCUMENTAL_RETENCION'


class SubserieDocumentalRetencion(models.Model):
    codigo = models.CharField(max_length=4)
    subserie_documental = models.TextField()

    class Meta:
        managed = False
        db_table = 'SUBSERIE_DOCUMENTAL_RETENCION'


class TipoCorrespondencia(models.Model):
    codigo = models.CharField(max_length=3)
    tipo = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'TIPO_CORRESPONDENCIA'


class TipoDocumentalRetencion(models.Model):
    tipo_documental = models.TextField()

    class Meta:
        managed = False
        db_table = 'TIPO_DOCUMENTAL_RETENCION'


class TipoDocumento(models.Model):
    tipo = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'TIPO_DOCUMENTO'


class TipoId(models.Model):
    tipo = models.CharField(max_length=4)
    detalle = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'TIPO_ID'


class TipoPersona(models.Model):
    tipo = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'TIPO_PERSONA'


class UsuarioXOficinaCorrespondencia(models.Model):
    oficina = models.ForeignKey(OficinaRecepcionCorrespondencia, models.DO_NOTHING)
    usuario = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'USUARIO_X_OFICINA_CORRESPONDENCIA'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
