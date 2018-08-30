from django.db import models
from django.contrib.auth.models import User
from correspondencia.carga_archivos import generar_ruta_archivo as archivo

# Create your models here.

class Consecutivo(models.Model):
    correspondencia_x_oficina = models.CharField(max_length=3)
    consecutivo = models.CharField(max_length=10)

    class Meta:
        db_table = 'CONSECUTIVO'

class Dependencia(models.Model):
    codigo = models.CharField(max_length=4)
    dependencia = models.TextField()

    class Meta:
        db_table = 'DEPENDENCIA_ALCALDIA'

# ---------------------------------- modelos segun tablas de retencion documental -----------------------------------

class Serie_documental_Retencion(models.Model):
    codigo = models.CharField(max_length=4)
    serie_documental = models.TextField()

    class Meta:
        db_table = 'SERIE_DOCUMENTAL_RETENCION'

class Subserie_documental_Retencion(models.Model):
    codigo = models.CharField(max_length=4)
    subserie_documental = models.TextField()

    class Meta:
        db_table = 'SUBSERIE_DOCUMENTAL_RETENCION'

class Tipo_documental_Retencion(models.Model):
    tipo_documental = models.TextField()

    class Meta:
        db_table = 'TIPO_DOCUMENTAL_RETENCION'

class Agr_retencion_documental(models.Model):
    dependencia = models.ForeignKey('Dependencia', models.DO_NOTHING)
    subserie_documental = models.ForeignKey('Subserie_documental_Retencion', models.DO_NOTHING)
    serie_documental = models.ForeignKey('Serie_documental_Retencion', models.DO_NOTHING)
    tipo_documental = models.ForeignKey('Tipo_documental_Retencion', models.DO_NOTHING)

    class Meta:
        db_table = 'AGRUPACION_TABLAS_RETENCION'

# ---------------------------------- modelos de radicacion de correspondencia -----------------------------------

class Oficina(models.Model):
    codigo = models.CharField(max_length=3)
    oficina = models.CharField(max_length=10)

    class Meta:
        db_table = 'OFICINA_RECEPCION_CORRESPONDENCIA'

class Tipo_correspondencia(models.Model):
    codigo = models.CharField(max_length=3)
    tipo = models.CharField(max_length=60)

    class Meta:
        db_table = 'TIPO_CORRESPONDENCIA'

class Tipo_documento(models.Model):
    tipo = models.CharField(max_length=10)

    class Meta:
        db_table = 'TIPO_DOCUMENTO'

class Tipo_id(models.Model):
    tipo = models.CharField(max_length=4)
    detalle = models.CharField(max_length=50)

    class Meta:
        db_table = 'TIPO_ID'

class Tipo_persona(models.Model):
    tipo = models.CharField(max_length=20)

    class Meta:
        db_table = 'TIPO_PERSONA'


class Empresa_mensajeria(models.Model):
    nombre = models.CharField(max_length=120)
    tipo_id = models.ForeignKey('Tipo_id', models.DO_NOTHING)
    numero_id = models.CharField(max_length=20)
    direccion = models.TextField()
    telefono = models.CharField(max_length=100)
    pagina_web = models.CharField(max_length=20)

    class Meta:
        db_table = 'EMPRESA_MENSAJERIA'

class Persona(models.Model):
    nombre = models.CharField(max_length=120)
    tipo_persona = models.ForeignKey('Tipo_persona', models.DO_NOTHING)
    tipo_id = models.ForeignKey('Tipo_id', models.DO_NOTHING)
    numero_id = models.CharField(max_length=20, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=18)
    email = models.EmailField()
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)

    class Meta:
        db_table = 'PERSONA'

class Dependencia_origen(models.Model):
    dependencia = models.ForeignKey('Dependencia', models.DO_NOTHING)

    class Meta:
        db_table = 'DEPENDENCIA_ORIGEN'


class Correspondencia_entrada(models.Model):
    fecha_recibido = models.DateField()
    hora_recibido = models.TimeField()
    numero_radicacion = models.CharField(max_length=30)
    correspondencia_x_oficina = models.CharField(max_length=2)
    remitente = models.ForeignKey('Persona', models.DO_NOTHING)
    dependencia_origen = models.ForeignKey('Dependencia_origen', models.DO_NOTHING,null=True)
    dependencia = models.ForeignKey('Dependencia', models.DO_NOTHING)
    serie_documental = models.ForeignKey('Serie_documental_Retencion', models.DO_NOTHING)
    subserie_documental = models.ForeignKey('Subserie_documental_Retencion', models.DO_NOTHING, null=True)
    tipo_documental = models.ForeignKey('Tipo_documental_Retencion', models.DO_NOTHING, null=True)
    asunto = models.CharField(max_length=200)
    observacion = models.TextField(null=True)
    fecha_documento_radicado = models.DateField()
    numero_folios_documento = models.CharField(max_length=4)
    archivo_digital = models.FileField(upload_to=archivo, blank=True)
    tipo_documento = models.ForeignKey('Tipo_documento', models.DO_NOTHING)
    tipo_correspondencia = models.ForeignKey('Tipo_correspondencia', models.DO_NOTHING)
    visualizado = models.BooleanField(default=False)
    anulado = models.BooleanField(default=False)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)

    class Meta:
        db_table = 'CORRESPONDENCIA_ENTRADA'

class Correspondencia_salida(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    fecha_documento = models.DateField()
    fecha_envio = models.DateField()
    asunto = models.CharField(max_length=200)
    observacion = models.TextField(null=True)
    numero_folios_documento = models.CharField(max_length=4)
    numero_guia = models.CharField(max_length=30)
    archivo_adjunto = models.FileField(upload_to=archivo, blank=True)
    persona = models.ForeignKey('Persona', models.DO_NOTHING)
    dependencia = models.ForeignKey('Dependencia', models.DO_NOTHING)
    serie_documental = models.ForeignKey('Serie_documental_Retencion', models.DO_NOTHING)
    subserie_documental = models.ForeignKey('Subserie_documental_Retencion', models.DO_NOTHING, null=True)
    tipo_documental = models.ForeignKey('Tipo_documental_Retencion', models.DO_NOTHING, null=True)
    tipo_documento = models.ForeignKey('Tipo_documento', models.DO_NOTHING)
    tipo_correspondencia = models.ForeignKey('Tipo_correspondencia', models.DO_NOTHING)
    empresa_mensajeria = models.ForeignKey('Empresa_mensajeria', models.DO_NOTHING)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)

    class Meta:
        db_table = 'CORRESPONDENCIA_SALIDA'

class Lectura_correspondencia(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    documento_fisico = models.BooleanField()
    documento_virtual = models.BooleanField()
    observacion = models.TextField()
    correspondencia = models.ForeignKey('Correspondencia_entrada', models.DO_NOTHING)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)

    class Meta:
        db_table = 'LECTURA_CORRESPONDENCIA'

class Evento_correspondencia_entrada(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    evento_realizado = models.CharField(max_length=100)
    correspondencia = models.ForeignKey('Correspondencia_entrada', models.DO_NOTHING)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)

    class Meta:
        db_table = 'EVENTO_CORRESPONDENCIA_ENTRADA'

class Usuario_x_oficina(models.Model):
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    oficina = models.ForeignKey('Oficina', models.DO_NOTHING)

    class Meta:
        db_table = 'USUARIO_X_OFICINA_CORRESPONDENCIA'

class Usuario(User):

    class Meta:
        proxy = True
