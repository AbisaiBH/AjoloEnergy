from django.shortcuts import render
from django.http import JsonResponse
from .models import Article
import random
from django.views.decorators.csrf import csrf_exempt

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
def weekly_article_consume(request):
    initial_consumption = 100
    days_of_week = ["Sábado", "Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    
    weekly_data = {
        day: max(0, initial_consumption + random.randint(-10, 10))
        for day in days_of_week
    }
    
    data = {
        "data": weekly_data
    }

    return JsonResponse(data)

@csrf_exempt
def monthly_article_consume(request):
    initial_consumption = 100
    days_in_month = [f"Día {i}" for i in range(1, 31 + 1)] 
    monthly_data = {
        day: max(0, initial_consumption + random.randint(-10, 10))
        for day in days_in_month
    }
    
    data = {
        "data": monthly_data
    }

    return JsonResponse(data)
