import os
from uuid import uuid4
from gestion_documental.settings import MEDIA_ROOT

def generar_ruta_archivo(instance, filename):

    extension = os.path.splitext(filename)[1][1:]
    nombre = instance.numero_radicacion
    ruta = os.path.join('pdf/')

    nombre_archivo = nombre.format(uuid4().hex, extension)
    nombre_file = nombre_archivo+'.pdf'

    if os.path.exists(MEDIA_ROOT + '/' + ruta + nombre_file):
        os.remove(MEDIA_ROOT + '/' + ruta + nombre_file)

    return os.path.join(ruta, nombre_file)