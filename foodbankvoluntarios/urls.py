"""
Configuración de URL para el proyecto foodbankvoluntarios.

La lista 'urlpatterns' dirige las URL a las vistas. Para obtener más información, consulte:
https://docs.djangoproject.com/en/5.2/topics/http/urls/
Ejemplos:
Vistas de funciones
1. Añadir una importación: desde my_app vistas de importación
2. Añade una URL a urlpatterns: path('', views.home, name='home')
Vistas basadas en clases
1. Añadir una importación: desde other_app.views importar Inicio
2. Añade una URL a urlpatterns: path('', Home.as_view(), name='home')
Incluyendo otra URLconf
1. Importe la función include(): desde django.urls importar inclusión, ruta
2. Añade una URL a urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
