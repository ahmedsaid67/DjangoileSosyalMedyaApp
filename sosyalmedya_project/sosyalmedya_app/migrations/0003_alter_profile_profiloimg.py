# Generated by Django 4.0.5 on 2022-06-15 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sosyalmedya_app', '0002_alter_profile_id_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profiloimg',
            field=models.ImageField(default='blank-profil.png', upload_to='profilo_img'),
        ),
    ]
