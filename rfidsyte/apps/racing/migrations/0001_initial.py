# Generated by Django 4.0.4 on 2022-07-22 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_title', models.CharField(max_length=100, verbose_name='Название гонки')),
                ('race_date', models.DateTimeField(verbose_name='Дата и время начала гонки')),
                ('race_time', models.TimeField(verbose_name='Время гонки')),
                ('race_condition', models.CharField(choices=[('Гонка Создана', 'Гонка Создана'), ('Гонка Запущена', 'Гонка Запущена'), ('Гонка Идет', 'Гонка Идет'), ('Гонка Закончилась', 'Гонка Закончилась')], max_length=20, verbose_name='Состояние Гонки')),
            ],
            options={
                'verbose_name': 'Гонка',
                'verbose_name_plural': 'Гонки',
                'ordering': ('race_date', 'race_title'),
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='ФИО участника')),
                ('total_time', models.TimeField(blank=True, null=True, verbose_name='Общее время')),
                ('laps_time', models.TextField(blank=True, null=True, verbose_name='Время прохождения круга')),
                ('rfid', models.CharField(max_length=50, null=True, verbose_name='Id Карточки')),
                ('Race', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='racing.race', verbose_name='Гонка')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
            },
        ),
    ]
