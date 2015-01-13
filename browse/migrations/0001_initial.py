# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('sdescr', models.TextField(verbose_name=b'Short description')),
                ('ldescr', models.TextField(verbose_name=b'Long description')),
                ('type', models.CharField(blank=True, max_length=1, null=True, verbose_name=b'Type', choices=[(b's', b'String'), (b'i', b'Integer'), (b'f', b'Float'), (b'b', b'Boolean')])),
                ('constr', models.CharField(max_length=256, null=True, verbose_name=b'Constraint', blank=True)),
                ('unit', models.CharField(max_length=256, null=True, verbose_name=b'Unit', blank=True)),
                ('block', models.CharField(blank=True, max_length=2, null=True, verbose_name=b'XSAMS block', choices=[(b'at', b'Atoms'), (b'as', b'Atomic States'), (b'mo', b'Molecules'), (b'ms', b'Molecular States'), (b'mq', b'Molecular Quantum Numbers'), (b'ct', b'Collisional Transitions'), (b'rt', b'Radiative Transitions'), (b'nr', b'Non-Radiative Transitions'), (b'me', b'Methods'), (b'fu', b'Functions'), (b'en', b'Environments'), (b'so', b'Sources'), (b'sd', b'Solids'), (b'pa', b'Particles')])),
                ('datatype', models.BooleanField(default=False, verbose_name=b'DataType in XSAMS?')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Keyword',
                'verbose_name_plural': 'Keywords',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='keyword',
            name='usage',
            field=models.ManyToManyField(to='browse.Usage', null=True, blank=True),
            preserve_default=True,
        ),
    ]
