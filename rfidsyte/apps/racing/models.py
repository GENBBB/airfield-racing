from django.db import models

class Race(models.Model):
    CONDITIONS = [
        ('Гонка Создана', 'Гонка Создана'),
        ('Гонка Запущена', 'Гонка Запущена'),
        ('Гонка Идет', 'Гонка Идет'),
        ('Гонка Закончилась', 'Гонка Закончилась')
    ]
    race_title = models.CharField('Название гонки', max_length = 100)
    race_date = models.DateTimeField('Дата и время начала гонки')
    race_time = models.TimeField('Время гонки')
    race_condition = models.CharField('Состояние Гонки', choices=CONDITIONS, max_length = 20)
    
    def __str__(self):
        return self.race_title
    
    class Meta:
        verbose_name = 'Гонка'
        verbose_name_plural = 'Гонки'
        ordering = ("race_date", "race_title")
    
class Participant(models.Model):
    Race = models.ForeignKey(Race, verbose_name="Гонка", blank=True, on_delete=models.CASCADE)
    name = models.CharField('ФИО участника', max_length = 100)
    total_time = models.TimeField('Общее время', blank=True, null=True)
    laps_time = models.TextField('Время прохождения круга', blank=True, null=True)
    rfid = models.CharField('Id Карточки', null=True, max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'