# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ces', '0005_auto_20171011_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacao',
            name='status',
            field=models.IntegerField(blank=True, choices=[(3, 'Solicitado Devolução'), (8, 'Reserva confirmada'), (4, 'Devolvido'), (7, 'Solicitado Reserva'), (6, 'Transferência confirmada'), (5, 'Solicitado Transferência'), (2, 'Emprestado'), (1, 'Solicitado retirada')], default=0),
        ),
    ]