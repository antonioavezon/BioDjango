from django.contrib import admin
from django.urls import path
from index import views as index_views  # Importa las vistas de la aplicación 'index'
from aplicaciones import views as aplicaciones_views  # Importa las vistas de la aplicación 'aplicaciones'
from acercade import views as acercade_views  # Importa las vistas de la aplicación 'acercade'
from resultado import views as resultado_views  # Importa las vistas de la aplicación 'resultado'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_views.index, name='index'),
    path('aplicaciones/', aplicaciones_views.aplicaciones, name='aplicaciones'),
    path('aplicaciones/blast', aplicaciones_views.blast, name='blast'),  # Nueva ruta para BLAST
    path('sobre_nosotros/', acercade_views.acercade, name='sobre_nosotros'),
    path('resultado/', resultado_views.resultado, name='resultado'),
    # ... otras rutas
]

