# Generated by Django 4.0.5 on 2022-06-04 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_pedido_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='data_pedido',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='data_adicionado',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
