# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ces', '0004_movimentacao_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacao',
            name='status',
            field=models.IntegerField(blank=True, choices=[(2, 'Emprestado'), (1, 'Solicitado retirada'), (7, 'Solicitado Reserva'), (4, 'Devolvido'), (3, 'Solicitado Devolução'), (6, 'Transferência confirmada'), (5, 'Solicitado Transferência'), (8, 'Reserva confirmada')], default=0),
        ),
    ]
