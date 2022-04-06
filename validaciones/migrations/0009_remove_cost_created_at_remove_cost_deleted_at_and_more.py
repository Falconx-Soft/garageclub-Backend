# Generated by Django 4.0 on 2022-04-06 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validaciones', '0008_costquantity_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cost',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='cost',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='cost',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='costquantity',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='costquantity',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='costquantity',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='vat',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='vat',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='vat',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='validation',
            name='risk',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2)], null=True),
        ),
        migrations.AlterField(
            model_name='validation',
            name='type',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2)]),
        ),
    ]
