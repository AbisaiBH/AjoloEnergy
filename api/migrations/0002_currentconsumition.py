# Generated by Django 5.1.7 on 2025-03-29 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentConsumition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('current_consumption', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Consumo Actual')),
                ('stack_increments', models.JSONField(blank=True, default=list, verbose_name='Historial de Aumentos')),
            ],
        ),
    ]
