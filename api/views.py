from django.shortcuts import render
from django.http import JsonResponse
from .models import Article
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def article_list_json(request):
    # Obtenemos los artículos y seleccionamos los campos deseados
    articles = list(Article.objects.all().values('id', 'name', 'consumo_actual', 'consumo_estimado_mensual'))
    # Retornamos los datos en formato JSON. 'safe=False' permite retornar una lista.
    return JsonResponse(articles, safe=False)