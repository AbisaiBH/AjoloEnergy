from django.shortcuts import render
from django.http import JsonResponse
from .models import Article, CurrentConsumition
import random
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

@csrf_exempt
def article_list_json(request):
    # Obtenemos los artículos y seleccionamos los campos deseados
    articles = list(Article.objects.all().values('id', 'name', 'consumo_actual', 'consumo_estimado_mensual'))
    # Retornamos los datos en formato JSON. 'safe=False' permite retornar una lista.
    return JsonResponse(articles, safe=False)

@csrf_exempt
def article_consume(request):
    initial_consumption = 100
    variation = random.randint(-10, 10)  # Variación aleatoria entre -10 y 10
    updated_consumption = max(0, initial_consumption + variation)  # Asegura que no sea menor que 0
    data = {
        "data": [updated_consumption]
    }
    return JsonResponse(data)

@csrf_exempt
def increase_consumption(request):
    # Obtener o crear el registro "default" con consumo inicial 0 (como Decimal)
    consumicion, created = CurrentConsumition.objects.get_or_create(
        name='default',
        defaults={'current_consumption': Decimal('0.00')}
    )
    # Generar un incremento aleatorio entre 0.5 y 1.2 y redondearlo a 2 decimales (como float)
    incremento_float = round(random.uniform(0.5, 1.2), 2)
    # Convertir el float a Decimal usando str para mantener la precisión
    incremento = Decimal(str(incremento_float))
    # Incrementar el consumo actual
    consumicion.current_consumption += incremento
    # Agregar el incremento al stack. Se guarda el valor float para que sea serializable en JSON.
    stack = consumicion.stack_increments  
    stack.append(incremento_float)
    consumicion.stack_increments = stack
    consumicion.save()
    return JsonResponse(consumicion.current_consumption, safe=False)

def decrement_last_increase(request):
    consumicion = CurrentConsumition.objects.get(name='default')
    
    # Verificar si el stack de aumentos no está vacío
    if not consumicion.stack_increments:
        return JsonResponse({"error": "No hay incrementos para restar."}, status=400)
    # Extraer (pop) el último incremento y restarlo al consumo actual
    ultimo_incremento = consumicion.stack_increments.pop()
    consumicion.current_consumption -= Decimal(str(ultimo_incremento))
    consumicion.save()
    
    contexto = {
        'consumicion': consumicion,
        'decremento': ultimo_incremento,
        'stack_restante': consumicion.stack_increments
    }
    
    return JsonResponse(consumicion.current_consumption, safe=False)
def get_consumicion(request):
    consumicion, created = CurrentConsumition.objects.get_or_create(
        name='default',
        defaults={'current_consumption': 0}
    )
    return JsonResponse({
        'current_consumption': consumicion.current_consumption
    })