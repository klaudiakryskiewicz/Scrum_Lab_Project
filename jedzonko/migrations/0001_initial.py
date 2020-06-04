# Generated by Django 2.2.6 on 2020-06-03 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dayname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('order', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ingredients', models.TextField()),
                ('description', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now_add=True)),
                ('preparation_time', models.IntegerField()),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Recipeplan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_name', models.CharField(max_length=255)),
                ('order', models.IntegerField()),
                ('day_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Dayname')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Plan')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='recipes',
            field=models.ManyToManyField(through='jedzonko.Recipeplan', to='jedzonko.Recipe'),
        ),
    ]
