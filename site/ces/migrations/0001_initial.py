# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminWeb',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movimentacao',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('retirada', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('devolucao', models.DateTimeField(default=datetime.datetime.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Objeto',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permissao_Objeto_x_PerfilUsuario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('perfilUsuario_id', models.ForeignKey(to='ces.PerfilUsuario')),
            ],
        ),
        migrations.CreateModel(
            name='Permissao_Objeto_x_Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('objeto_id', models.ForeignKey(to='ces.Objeto')),
            ],
        ),
        migrations.CreateModel(
            name='TipoObjeto',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=250, null=True, blank=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('senha', models.TextField()),
                ('perfilUsuario_id', models.ForeignKey(to='ces.PerfilUsuario')),
            ],
        ),
        migrations.AddField(
            model_name='permissao_objeto_x_usuario',
            name='usuario_id',
            field=models.ForeignKey(to='ces.Usuario'),
        ),
        migrations.AddField(
            model_name='permissao_objeto_x_perfilusuario',
            name='tipoObjeto_id',
            field=models.ForeignKey(to='ces.TipoObjeto'),
        ),
        migrations.AddField(
            model_name='objeto',
            name='tipoObjeto_id',
            field=models.ForeignKey(to='ces.TipoObjeto'),
        ),
        migrations.AddField(
            model_name='movimentacao',
            name='objeto_id',
            field=models.ForeignKey(to='ces.Objeto'),
        ),
        migrations.AddField(
            model_name='movimentacao',
            name='usuario_id',
            field=models.ForeignKey(to='ces.Usuario'),
        ),
        migrations.AddField(
            model_name='adminweb',
            name='tipoObjeto_id',
            field=models.ForeignKey(to='ces.TipoObjeto'),
        ),
        migrations.AddField(
            model_name='adminweb',
            name='usuario_id',
            field=models.ForeignKey(to='ces.Usuario'),
        ),
    ]
