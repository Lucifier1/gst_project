# Generated by Django 5.1.6 on 2025-03-07 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0006_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='rate',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
