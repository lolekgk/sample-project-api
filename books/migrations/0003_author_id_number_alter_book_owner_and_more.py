# Generated by Django 4.2 on 2023-04-13 02:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_genre_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='id_number',
            field=models.CharField(default=1, max_length=55, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='genre',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_genre_name'),
        ),
    ]
