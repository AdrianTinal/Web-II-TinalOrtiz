from django.http import HttpResponse
from .models import Boleto
from .models import Evento
from .models import Localidad
from .models import Producto
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    eventos = Evento.objects.all()[:3]  # Obtener los primeros 3 eventos
    return render(request, 'base/index.html', {'eventos': eventos})
    
def boletos_list(request, evento_id=None):
    if evento_id:
        boletos = Boleto.objects.filter(evento_id=evento_id)
    else:
        boletos = Boleto.objects.all()
    return render(request, 'boletos/boletos_list.html', {'boletos': boletos, 'evento_id': evento_id})

def eventos_list(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/eventos_list.html', {'eventos': eventos})

def agregar_evento(request):
    localidades = Localidad.objects.all()
    eventos_recientes = Evento.objects.order_by('-fecha_inicio')[:10]
    return render(request, 'eventos/agregar_evento.html', {'localidades': localidades, 'eventos_recientes': eventos_recientes})

@csrf_exempt
def guardar_evento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        localidad_id = data.get('localidad')
        descripcion = data.get('descripcion')
        photo = data.get('photo')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        if not all([name, localidad_id, descripcion, photo, fecha_inicio, fecha_fin]):
            return JsonResponse({'error': 'Todos los campos son obligatorios.'}, status=400)

        fecha_inicio = timezone.datetime.fromisoformat(fecha_inicio)
        fecha_fin = timezone.datetime.fromisoformat(fecha_fin)

        if fecha_fin < fecha_inicio:
            return JsonResponse({'error': 'La fecha de fin no puede ser menor que la fecha de inicio.'}, status=400)

        if fecha_inicio < timezone.now():
            return JsonResponse({'error': 'La fecha de inicio debe ser mayor al día de hoy.'}, status=400)

        localidad = Localidad.objects.get(id=localidad_id)
        if Evento.objects.filter(localidad=localidad).exists():
            return JsonResponse({'error': 'No puedes agregar dos eventos seguidos de la misma localidad.'}, status=400)

        evento = Evento.objects.create(
            name=name,
            descripcion=descripcion,
            photo=photo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            localidad=localidad

        )
        return JsonResponse({'success': 'Evento guardado correctamente.'})

    return JsonResponse({'error': 'Método no permitido.'}, status=405)


@csrf_exempt
def eliminar_evento(request, evento_id):
    if request.method == 'DELETE':
        try:
            evento = Evento.objects.get(id=evento_id)
            evento.delete()
            return JsonResponse({'success': 'Evento eliminado correctamente.'})
        except Evento.DoesNotExist:
            return JsonResponse({'error': 'Evento no encontrado.'}, status=404)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def eventos_recientes(request):
    eventos = Evento.objects.order_by('-fecha_inicio')[:10]
    eventos_data = [
        {
            'id': evento.id,
            'name': evento.name,
            'fecha_inicio': evento.fecha_inicio,
            'fecha_fin': evento.fecha_fin,
            'localidad': {'name': evento.localidad.name}
        }
        for evento in eventos
    ]
    return JsonResponse({'eventos': eventos_data})

def productos_list(request):
    productos = Producto.objects.all()
    return render(request, 'productos/productos_list.html', {'productos': productos})

def agregar_productos(request):
    localidades = Localidad.objects.all()
    productos_recientes = Producto.objects.order_by('-id')[:10]
    return render(request, 'productos/agregar_productos.html', {'localidades': localidades, 'productos_recientes': productos_recientes})

@csrf_exempt
def guardar_producto(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        precio = data.get('precio')
        localidad_id = data.get('localidad')

        if not all([name, precio, localidad_id]):
            return JsonResponse({'error': 'Todos los campos son obligatorios.'}, status=400)

        if float(precio) <= 0:
            return JsonResponse({'error': 'El precio debe ser mayor a 0.'}, status=400)

        hoy = timezone.now().date()
        productos_hoy = Producto.objects.filter(fecha_inicio__date=hoy).count()
        if productos_hoy >= 10:
            return JsonResponse({'error': 'Solo se pueden agregar 10 productos por día.'}, status=400)

        localidad = Localidad.objects.get(id=localidad_id)
        fecha_inicio = timezone.now()
        fecha_fin = timezone.now()
        producto = Producto.objects.create(
            name=name,
            precio=precio,
            localidad=localidad,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        return JsonResponse({'success': 'Producto guardado correctamente.'})

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def productos_recientes(request):
    productos = Producto.objects.order_by('-id')[:10]
    productos_data = [
        {
            'id': producto.id,
            'name': producto.name,
            'fecha_inicio': producto.fecha_inicio,
            'fecha_fin': producto.fecha_fin,
            'localidad': {'name': producto.localidad.name},

        }
        for producto in productos
    ]
    return JsonResponse({'productos': productos_data})

@csrf_exempt
def eliminar_producto(request, producto_id):
    if request.method == 'DELETE':
        try:
            producto = Producto.objects.get(id=producto_id)
            producto.delete()
            return JsonResponse({'success': 'Producto eliminado correctamente.'})
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado.'}, status=404)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)