from django.shortcuts import render
from django.http import JsonResponse
from .models import Article, CurrentConsumition
from openai import OpenAI
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .prompts import Prompts
import random
import json
import google.generativeai as genai
import os
import time
import re
import numpy as np

voltage_mean = 100




# Load environment variables from .env file
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=key)

@csrf_exempt
def article_list_json(request):
    articles = list(Article.objects.all().values('id', 'name', 'consumo_actual', 'consumo_estimado_mensual', 'habitacion', 'analisis_emoji', 'analisis_text'))

    for article in articles:
        consumo_actual = Decimal(article['consumo_actual']) 
        consumo_actual_float = float(consumo_actual)
        variacion = consumo_actual_float * random.uniform(-0.1, 5.9)
        nuevo_consumo = max(0, consumo_actual_float + variacion) 
        article['consumo_actual'] = round(nuevo_consumo, 2)  
    return JsonResponse(articles, safe=False)

@csrf_exempt
def article_consume(request):
    global voltage_mean
    print(voltage_mean)
    mu, sigma = voltage_mean, 2 # mean and standard deviation
    s = float(np.random.normal(mu, sigma))
    updated_consumption = round(s,1)
    data = {
        "data": [updated_consumption]
    }
    return JsonResponse(data)

@csrf_exempt
def increase_consumption(request):
    global voltage_mean
    if voltage_mean == 100: voltage_mean = 150
    else: voltage_mean = 100
    return JsonResponse({"incremento": voltage_mean}, safe=False)

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
def yearly_article_consume(request):
    initial_consumption = 100
    months_of_year = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    
    yearly_data = {
        month: max(0, initial_consumption + random.randint(-10, 10))
        for month in months_of_year
    }
    
    data = {
        "data": yearly_data
    }

    return JsonResponse(data)

def update_article_analysis():
    def extraer_dos_elementos(texto):
        patron = r'(\[.*?\])'
        coincidencia = re.search(patron, texto, re.DOTALL)
        if coincidencia:
            lista_str = coincidencia.group(1)
            try:
                # Convertir el fragmento encontrado a una lista usando json.loads
                lista = json.loads(lista_str)
            except Exception:
                # En caso de error al convertir, retorna (None, None)
                return None, None
            
            # Verifica que sea una lista y que tenga exactamente dos elementos.
            if isinstance(lista, list) and len(lista) == 2:
                return lista[0], lista[1]
        
        # Si no se encontró el fragmento o la lista no tiene 2 elementos, retorna (None, None)
        return None, None

    all_articles = Article.objects.all()
    for article in all_articles:
        article_name = article.name
        article_consumo = article.consumo_actual / 7 / 12
        article_info = str( [article_name, article_consumo] )
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": Prompts.ANALYSIS_PROMPT},
                {"role": "user", "content": article_info}
            ]
        )
        
        response_text = completion.choices[0].message.content
        emoji, analisis = extraer_dos_elementos(response_text) 
        print( emoji, analisis )
        article.analisis_emoji = emoji
        article.analisis_text = analisis
        article.save()
        
@csrf_exempt
def pie_article_consume(request):
    articles = list(Article.objects.all().values('name', 'consumo_actual'))
    
    for article in articles:
        consumo_actual = Decimal(article['consumo_actual'])
        consumo_actual_float = float(consumo_actual)
        
        variacion = consumo_actual_float * random.uniform(-0.1, 0.9)
        nuevo_consumo = max(0, consumo_actual_float + variacion)
        
        article['consumo_actual'] = round(nuevo_consumo, 2)
    
    formatted_data = [
        {"nombre": article['name'], "consumo_actual": article['consumo_actual']}
        for article in articles
    ]
    
    return JsonResponse(formatted_data, safe=False)
    # Retornar el JSON con los datos formateados

@csrf_exempt
def turn_off_article(request, id):
    object_article = Article.objects.get(id=id)
    object_article.analisis_emoji = "🔴"
    object_article.save()
    print(object_article.analisis_emoji)
    
    return JsonResponse({"OK": "Artículo cambiado"})


@csrf_exempt
def rename_article(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    object_article = Article.objects.get(id=id)
    data = json.loads(request.body)
    nuevo_nombre = data.get("name", "").strip()

    if not nuevo_nombre:
        return JsonResponse({"error": "El nuevo nombre no puede estar vacío"}, status=400)

    object_article.name = nuevo_nombre
    object_article.save()

    return JsonResponse({"success": "Artículo renombrado", "new_name": nuevo_nombre})






    