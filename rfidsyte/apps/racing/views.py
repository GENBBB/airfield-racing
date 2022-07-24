from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
import datetime
import threading
from .rfid import RFID
from .models import Race, Participant

def main(request):
    all_race_list = Race.objects.all()
    date_list = []
    for i in all_race_list:
        date_list.append(i.race_date.date())
    date_list = list(set(date_list))
    date_list.sort()
    date_list.reverse()
    race_date = datetime.date.today()
    print(date_list)
    if date_list.count(race_date) == 0 and len(date_list) != 0:
        race_date = date_list[0]
    race_date = race_date.strftime('%Y-%m-%d')
    return index(request, race_date)
    

def index(request, race_date):
    race_date = datetime.datetime.strptime(race_date, '%Y-%m-%d')
    race_date = race_date.date()
    top_race_list = Race.objects.filter(race_date__gte=timezone.now())
    top_race_list = top_race_list[:5]
    all_race_list = Race.objects.all()
    date_list = []
    for i in all_race_list:
        date_list.append(i.race_date.date())
    date_list = list(set(date_list))
    date_list.sort()
    date_list.reverse()
    race_list = Race.objects.filter(race_date__gte=race_date).filter(race_date__lte=race_date+datetime.timedelta(days=1))
    table_race =[]
    class line_table():
        def __init__(self, count, race):
            self.number_of_participant = count
            self.race = race
    for i in race_list:
        a = line_table(i.participant_set.count(), i)
        table_race.append(a)
    return render(request, 'racing/list.html', {'race_list': table_race, 'top_race_list': top_race_list, 'date_list': date_list, 'date': race_date})

def detail(request, race_id):
    try:
        a = Race.objects.get(id = race_id)
    except:
        Http404("Гонка не найдена")
    race_list = Race.objects.filter(race_date__gte=a.race_date.date()).filter(race_date__lte=a.race_date.date()+datetime.timedelta(days=1))
    race_list = race_list[:5]
    all_participant = a.participant_set.all()
    header = ['Имя участника', 'Общее время']
    rows = []
    number_of_participant = a.participant_set.count()
    max_laps = 0
    for i in all_participant:
        line = ['-_-', ]
        if i.laps_time != None:
            line = i.laps_time.split()
        if (len(line) > max_laps):
            max_laps = len(line)
        if (i.total_time == None):
            line.insert(0, '-_-')
        else:
            line.insert(0, i.total_time.strftime("%H:%M:%S"))
        line.insert(0, i.name)
        rows.append(line)
    for i in range(max_laps):
            header.append(str(i+1)+' круг')
    for i in rows:
        for j in range(max_laps+2-len(i)):
            i.append('-_-')
    return render(request, 'racing/detail.html', {'race': a, 'header': header, 'rows': rows, 'top_race_list': race_list, 'number_of_participant': number_of_participant})