"""gestion_documental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from correspondencia.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', inicio, name="inicio"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('menu', menu, name="menu"),

    path('correspondencia_entrada', correspondencia_entrada, name='correspondencia_entrada'),

    path('usuario', usuario, name='usuario'),
    path('guardar_usuario', guardar_usuario, name='guardar_usuario'),
    path('inhabilitar_usuario', inhabilitar_usuario, name='inhabilitar_usuario'),
    path('editar_usuario', editar_usuario, name='editar_usuario'),

    path('guardar_correspondencia_entrada', guardar_correspondencia_entrada, name='guardar_correspondencia_entrada'),
    path('correspondencia_radicado', correspondencia_radicado, name='correspondencia_radicado'),
    path('editar_correspondencia_entrada', editar_correspondencia_entrada, name='editar_correspondencia_entrada'),
    path('anular_correspondencia_entrada', anular_correspondencia_entrada, name='anular_correspondencia_entrada'),

    path('corresp_entrada', reporte_corresp_ent, name='rep_corresp_ent'),
    path('corresp_entrada_pdf', reporte_corresp_ent_PDF, name='rep_corresp_ent_PDF'),

    path('escaneo_documentos', escaneo_documentos, name='escaneo_documentos'),
    path('etiqueta_pdf', etiqueta_PDF, name='etiqueta_PDF'),

    path('tablas_retencion', tablas_retencion, name='tablas_retencion'),
    path('buscar_agr_documental', buscar_agr_documental, name='buscar_agr_documental'),

    #path('buscar_serie_documental', buscar_serie_documental, name='buscar_serie_documental'),
    #path('buscar_subserie_documental', buscar_subserie_documental, name='buscar_subserie_documental'),
    #path('buscar_tipo_documental_retencion', buscar_tipo_documental_retencion, name='buscar_tipo_documental_retencion'),

    path('guardar_dependencia', guardar_dependencia, name='guardar_dependencia'),
    path('guardar_serie_documental', guardar_serie_documental, name='guardar_serie_documental'),
    path('guardar_subserie_documental', guardar_subserie_documental, name='guardar_subserie_documental'),
    path('guardar_tipo_documental', guardar_tipo_documental, name='guardar_tipo_documental'),

    path('buscar_remitente', buscar_remitente, name='buscar_remitente'),
    path('guardar_remitente', guardar_remitente, name='guardar_remitente'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
