from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    consumo_actual = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Consumo Actual"
    )
    consumo_estimado_mensual = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Consumo Estimado Mensual"
    )
    habitacion = models.IntegerField()
    analisis_emoji = models.CharField(max_length=128)
    analisis_text = models.TextField(max_length=1024)

    def __str__(self):
        return self.name
    
    
class CurrentConsumition(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    current_consumption = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Consumo Actual"
    )
    stack_increments = models.JSONField(default=list, blank=True, verbose_name="Historial de Aumentos")
    
    def __str__(self):
        return self.name
    
    
