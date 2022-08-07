import socket
import datetime
from django.utils import timezone
from .models import Participant, Race
from threading import Timer
from .card_reader import card_parser


class RFID():
    def __init__(self, race_id):
        self.sock = socket.socket()
        self.port = 6000
        self.host = '192.168.1.190'
        self.race_id = race_id
        
    def card_time_list(self):
        a = Race.objects.get(id = self.race_id)
        participants = a.participant_set.all()
        card_time = []
        for i in participants:
            line = []
            line.append(i)
            line.append(i.rfid)
            for i in range(3):
                line.append(datetime.timedelta())
            line.append(0)
            line.append(False)
            line.append(False)
            card_time.append(line)
        return card_time
        
        
    def race(self, r, card_time, cards):
        r.race_condition = "Гонка Идет"
        r.save()
        self.sock.connect((self.host, self.port))
        start = timezone.now()
        while(r.race_date+datetime.timedelta(hours=r.race_time.hour, minutes=r.race_time.minute, seconds=r.race_time.second, microseconds=r.race_time.microsecond) > timezone.now()):
            data = ''
            while data == '':
                self.sock.send(b'\x04\x00\x01\xdb\x4b')
                data = self.sock.recv(64)
                data = data.hex()
                data_list = card_parser.cards(data, cards)
            for data in data_list:
                for i in card_time:
                    if (data == i[1]):
                        if i[7]:
                            if (i[2] == datetime.timedelta()):
                                i[5] += 1
                                i[2] = timezone.now()-start-i[4]
                                i[3] = timezone.now()-start-i[4]
                            elif (timezone.now()-start-i[3]-i[4] < datetime.timedelta(seconds = 2)):
                                i[3] = timezone.now()-start-i[4]
                            else:
                                x = (i[2]+i[3])/2
                                i[4] += x
                                x_time = (datetime.datetime.min + x).time()
                                a = i[0]
                                if a.laps_time != None:
                                    a.laps_time += ' ' + x_time.strftime("%H:%M:%S")
                                else:
                                    a.laps_time = x_time.strftime("%H:%M:%S")
                                if a.total_time != None:
                                    a.total_time = (datetime.timedelta(hours=a.total_time.hour, minutes=a.total_time.minute, seconds=a.total_time.second, microseconds=a.total_time.microsecond)+x+datetime.datetime.min).time()
                                else:
                                    a.total_time = x_time
                                a.save()
                                print("Save")
                                i[5] += 1
                                i[2] = timezone.now()-start-i[4]
                                i[3] = timezone.now()-start-i[4]
                            break
                        else:
                            if (i[2] == datetime.timedelta()):
                                i[2] = timezone.now()-start
                                i[3] = timezone.now()-start
                            elif (timezone.now()-start-i[3] < datetime.timedelta(seconds = 2)):
                                i[3] = timezone.now()-start
                            else:
                                i[7] = True
                                i[2] = timezone.now()-start-i[4]
                                i[3] = timezone.now()-start-i[4]
                            break
        max_circle = 0
        finish_first = False
        count_p = r.participant_set.count()
        numbers_finish = 0
        for i in card_time:
            if i[5] > max_circle:
                max_circle = i[5]
        while numbers_finish < count_p:
            data = ''
            while data == '':
                self.sock.send(b'\x04\x00\x01\xdb\x4b')
                data = self.sock.recv(64)
                data = data.hex()
                data_list = card_parser.cards(data, cards)
            for data in data_list:
                for i in card_time:
                    if (data == i[1]):
                        if (i[2] == datetime.timedelta()):
                            i[5] += 1
                            i[2] = timezone.now()-start-i[4]
                            i[3] = timezone.now()-start-i[4]
                        elif (timezone.now()-start-i[3]-i[4] < datetime.timedelta(seconds = 2)):
                            i[3] = timezone.now()-start-i[4]
                        else:
                            if not(finish_first and i[6]):
                                x = (i[2]+i[3])/2
                                i[4] += x
                                x_time = (datetime.datetime.min + x).time()
                                a = i[0]
                                if a.laps_time != None:
                                    a.laps_time += ' ' + x_time.strftime("%H:%M:%S")
                                else:
                                    a.laps_time = x_time.strftime("%H:%M:%S")
                                if a.total_time != None:
                                    a.total_time = (datetime.timedelta(hours=a.total_time.hour, minutes=a.total_time.minute, seconds=a.total_time.second, microseconds=a.total_time.microsecond)+x+datetime.datetime.min).time()
                                else:
                                    a.total_time = x_time
                                a.save()
                                i[5] += 1
                                if i[5] == max_circle+1:
                                    i[6] = True
                                    finish_first = True
                                    numbers_finish += 1
                                i[2] = timezone.now()-start-i[4]
                                i[3] = timezone.now()-start-i[4]
                        break
        for i in card_time:
            if i[2] != 0:
                x = (i[2]+i[3])/2
                x_time = (datetime.datetime.min + x).time()
                a = i[0]
                if a.laps_time != None:
                    a.laps_time += ' ' + x_time.strftime("%H:%M:%S")
                else:
                    a.laps_time = x_time.strftime("%H:%M:%S")
                if a.total_time != None:
                    a.total_time = (datetime.timedelta(hours=a.total_time.hour, minutes=a.total_time.minute, seconds=a.total_time.second, microseconds=a.total_time.microsecond)+x+datetime.datetime.min).time()
                else:
                    a.total_time = x_time
                a.save()
        self.sock.close()
        r.race_condition = "Гонка Закончилась"
        r.save()
        
    def start(self):
        print('ada')
        card_time = RFID.card_time_list(self)
        a = Race.objects.get(id = self.race_id)
        delta = a.race_date-timezone.now()
        cards = []
        participants = a.participant_set.all()
        for i in participants:
            cards.append(i.rfid)
        cards.sort(reverse=True)
        print(cards)
        t = Timer(delta.total_seconds(), RFID.race, [self, a, card_time, cards])
        t.start()
        return
    
    def load_cards(self, a):
        self.sock.connect((self.host, self.port))
        self.sock.send(b'\x04\xff\x21\x19\x95')
        data = self.sock.recv(64)
        print(data.hex())
        data = ''
        while data == '':
            self.sock.send(b'\x04\x00\x01\xdb\x4b')
            data = self.sock.recv(64)
            data = data.hex()
            data = card_parser.card(data)
        print(data)
        self.sock.close()
        a.rfid = data
        a.save()