# Generated by Django 4.0 on 2022-02-23 09:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('description', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CostQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('amount', models.FloatField(blank=True)),
                ('cost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='validaciones.cost')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('description', models.CharField(blank=True, max_length=10, null=True)),
                ('amount', models.FloatField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('calculation_type', models.IntegerField(choices=[(0, 'Rebu'), (1, 'Iva')])),
                ('reference', models.CharField(max_length=15)),
                ('make', models.CharField(blank=True, choices=[(0, 'Abarth'), (1, 'Alfa Romeo'), (2, 'Aston Martin'), (3, 'Audi'), (4, 'Bentley'), (6, 'Bertone'), (5, 'BMW'), (7, 'Cadillac'), (8, 'Chevrolet'), (9, 'Chrysler'), (10, 'Citroen')], max_length=25, null=True)),
                ('model', models.CharField(max_length=50)),
                ('amount_purchase', models.FloatField()),
                ('purchase_vat', models.BooleanField(default=False)),
                ('amount_sale', models.FloatField()),
                ('sale_vat', models.BooleanField(default=False)),
                ('margin', models.FloatField(blank=True, null=True)),
                ('type', models.IntegerField(choices=[(0, 'Type A'), (1, 'Type B')])),
                ('risk', models.IntegerField(choices=[(1, '1'), (2, '2')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('costs', models.ManyToManyField(to='validaciones.CostQuantity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cost',
            name='vat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='validaciones.vat'),
        ),
    ]
