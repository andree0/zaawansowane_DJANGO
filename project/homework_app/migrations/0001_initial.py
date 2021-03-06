# Generated by Django 3.1.7 on 2021-03-13 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=64)),
                ('slug', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('vat', models.DecimalField(choices=[(0, '0%'), (0.05, '5%'), (0.08, '8%'), (0.23, '23%')], decimal_places=2, max_digits=3)),
                ('stock', models.PositiveIntegerField()),
                ('categories', models.ManyToManyField(to='homework_app.Category')),
            ],
        ),
    ]
