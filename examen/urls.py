from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('boletos/', views.boletos_list, name='boletos_list'),
    path('boletos/<int:evento_id>/', views.boletos_list, name='boletos_por_evento'),
    path('eventos/', views.eventos_list, name='eventos_list'),
    path('agregar/', views.agregar_evento, name='agregar_evento'),
    path('guardar/', views.guardar_evento, name='guardar_evento'),
    path('eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('eventos_recientes/', views.eventos_recientes, name='eventos_recientes'),
    path('productos/', views.productos_list, name='productos_list'),
    path('agregar_productos/', views.agregar_productos, name='agregar_productos'),
    path('guardar_producto/', views.guardar_producto, name='guardar_producto'),
    path('productos_recientes/', views.productos_recientes, name='productos_recientes'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]