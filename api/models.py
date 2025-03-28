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

    def __str__(self):
        return self.name