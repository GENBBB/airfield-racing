from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils.http import urlencode
from django import forms
from django.shortcuts import redirect
from .rfid import RFID
from django.http import HttpResponseRedirect
import threading


from .models import Race, Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name",] 
        
class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = '__all__'


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    form = RaceForm
    list_display = ("race_title", "race_date", "start_race", "view_participant_link")
    def view_participant_link(self, obj):
        count = obj.participant_set.count()
        url = (
            reverse("admin:racing_participant_changelist")
            + "?"
            + urlencode({"Race__id__exact": f"{obj.id}"})
        )
        return format_html('<a href="{}"> {} Участника</a>', url, count)
    view_participant_link.short_description = "Участники"
    list_filter = ("race_date", "race_condition")
    readonly_fields = ("race_condition", )
    def save_model(self, request, obj, form, change):
        obj.race_condition = "Гонка Создана"
        super().save_model(request, obj, form, change)
    def start_race(self, obj):
        if obj.pk == None:
            return
        if obj.race_condition != "Гонка Создана":
            return format_html(obj.race_condition)
        return format_html(
            '<a class="button" href="{}">Начать Гонку</a> ',
            reverse('admin:start_race_rfid', args=[obj.pk, ])
        )
    start_race.short_description = "Состояние Гонки"
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path ('start_race_rfid/',
                  self.admin_site.admin_view(self.kos),
            ),
            path (
                'start_race_rfid/<int:pk>',
                self.admin_site.admin_view(self.start_race_rfid),
                name = 'start_race_rfid'
            ),
        ]
        return custom_urls + urls
    def kos(self, request):
        pass
    def start_race_rfid(self, request, pk):
        try:
            a = Race.objects.get(pk = pk)
        except:
            Http404("Запуск несуществующей гонки") 
        if str(a.race_condition) != "Гонка Создана":
            return redirect(reverse('admin:racing_race_changelist'))
        a.race_condition = "Гонка Запущена"
        a.save()
        b = RFID(a.id)
        print('Запуск Потока')
        race = threading.Thread(target=b.start, args=(), daemon=False)
        race.start()
        return redirect(reverse('admin:racing_race_changelist'))

    
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):    
    list_display = ("name", "race_link", "rfid", "define_card")
    def race_link(self, obj):
        url = (
            reverse("admin:racing_race_changelist")
            + "?"
            + urlencode({"id": f"{obj.Race.id}"})
        )
        return format_html('<a href="{}"> {}</a>', url, obj.Race.race_title)
    race_link.short_description = "Гонка"
    list_filter = ("Race", )
    readonly_fields = ("total_time", "laps_time", "rfid", "define_card")
    def define_card(self, obj):
        if obj.pk == None:
            return 
        return format_html(
            '<a class="button" href="{}">Назначить Карту</a> ',
            reverse('admin:load_cards', args=[obj.pk, ])
        )
    define_card.short_description = 'Назначение Карты'
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path ('load_cards/',
                  self.admin_site.admin_view(self.kos),
            ),
            path (
                'load_cards/<int:pk>',
                self.admin_site.admin_view(self.load_cards),
                name = 'load_cards'
            ),
        ]
        return custom_urls + urls
    def kos(self, request):
        pass
    
    def load_cards(self, request, pk):
        a = RFID(0)
        b = Participant.objects.get(pk = pk)
        print("Поднесите Карту")
        a.load_cards(b)
        return redirect(reverse('admin:racing_race_changelist'))