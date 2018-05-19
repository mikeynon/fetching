import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CalendarScrape.settings")
import django
django.setup()
import datetime
import re
import time
import bs4 as bs
import requests
from django.apps import AppConfig
from django.core.management.base import BaseCommand

from events.models import Event, searchBandSugg, User, band

now = time.gmtime(time.time())

#########EVENTS SCRAPERS##########
##THE KNOW WORKS
class Command(BaseCommand):
    help = 'Scrapes the for Events at The Know'

    def handle(self, *args, **options):
        self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))

    class EventsConfigKn(AppConfig):
        name = 'events'
        data = requests.get('https://www.eventbrite.com/o/the-know-14797292017')
        sauce = data.text
        soup = bs.BeautifulSoup(sauce, "html.parser")
        for i in soup.find_all("div", {"class":"list-card__body"}):
            date = i.find("time", {"class":"list-card__date"})
            dates = date.text
            strpdate = " ".join(dates.split())
            band_name = strpdate.split(" ")
            day1 = band_name[1] +" " +band_name[2]
            try:
                day = datetime.datetime.strptime(day1, '%b %d').replace(2018)
            except ValueError:
                continue
            if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
                day = day.replace(2018)
            else:
                day = day.replace(2019)
            band = i.find("div",{"class":"list-card__title"})
            act = band.text.upper()
            notes = " ".join(act.split())
            start_time = "7:00 PM PDT"
            end_time = "11:00 PM PDT"
            event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
            if created:
                print(event, 'Created')
            else:
                print(event, "Exists already")

##BOSSSANOVA BALLROOM WORKS
class Command(BaseCommand):
    help = 'Scrapes the for Events at Bossanove Ballroom'

    def handle(self, *args, **options):
        self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))

    class EventsConfigKn(AppConfig):
        name = 'events'
        data = requests.get('https://www.eventbrite.com/o/bossanova-presents-14578044956')
        sauce = data.text
        soup = bs.BeautifulSoup(sauce, "html.parser")
        for i in soup.find_all("div", {"class": "list-card__body"}):
            date = i.find("time", {"class": "list-card__date"})
            dates = date.text
            strpdate = " ".join(dates.split())
            band_name = strpdate.split(" ")
            day1 = band_name[1] + " " + band_name[2]
            try:
                day = datetime.datetime.strptime(day1, '%b %d').replace(2018)
            except ValueError:
                continue
            if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
                day = day.replace(2018)
            else:
                day = day.replace(2019)
            band = i.find("div", {"class": "list-card__title"})
            act = band.text.upper()
            note = " ".join(act.split())
            notes = note + " at Bossanova Ballroom"
            start_time = "7:00 PM PDT"
            end_time = "11:00 PM PDT"
            event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
            if created:
                print(event, 'Created')
            else:
                print(event, "Exists already")

## DOUG FIR WORKS
class EventsConfigDF(AppConfig):
    name = 'events'
    help = 'Scrapes the for Events at Doug Fir Lounge'

    data = requests.get('https://www.dougfirlounge.com/calendar')
    sauce = data.text
    soup = bs.BeautifulSoup(sauce, "html.parser")
    for i in soup.find_all("td", {"class": "has-event"}):
        start_time = "8:00 PM PDT"
        end_time = "11:00 PM PDT"
        string = i.text.upper()
        if len(string) > 10:
            name = i.find("a", {"class": "url"})
            notes = name.text + " at Doug Fir Lounge"
            stringlist = string.split()
            date = stringlist[1]
            if re.search('[a-zA-Z]', date) == True:
                pass
            else:
                dayt = date + "/2018"
            try:
                day = datetime.datetime.strptime(dayt, '%d/%m/%Y').replace(2018)
            except ValueError:
                continue
            # if int(dayt.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
            #     day = dayt.replace(2018)
            # else:
            #     day = dayt.replace(2019)
        else:
            continue
        event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
        if created:
            print(event, 'Created')
        else:
            print(event, "Exists already")

##DANTES WORKS
class Command(BaseCommand):
    help = "Scrapes the for Events at Dante's"

    def handle(self, *args, **options):
        self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))

    class EventsConfigDa(AppConfig):
        name = 'events'
        urls = ['https://danteslive.com/calendar/?cal-month=2&cal-year=2018#content',
                'https://danteslive.com/calendar/?cal-month=3&cal-year=2018#content',
                'https://danteslive.com/calendar/?cal-month=4&cal-year=2018#content',
                'https://danteslive.com/calendar/?cal-month=5&cal-year=2018#content',
                'https://danteslive.com/calendar/?cal-month=6&cal-year=2018#content',
                'https://danteslive.com/calendar/?cal-month=7&cal-year=2018#content',
                'https://danteslive.com/calendar/?cal-month=8&cal-year=2018#content',
                'https://danteslive.com/calendar/?cal-month=9&cal-year=2018#content',
                'https://danteslive.com/calendar/?cal-month=10&cal-year=2018#content',
                'https://danteslive.com/calendar/?cal-month=11&cal-year=2018#content',
                'https://danteslive.com/calendar/?cal-month=12&cal-year=2018#content'
                ]
        for i in urls:
            data = requests.get(i)
            sauce = data.text
            soup = bs.BeautifulSoup(sauce, "html.parser")
            for i in soup.find_all("div", {"class":"tw-cal-event"}):
                start_time = "7:00 PM PDT"
                end_time = "11:00 PM PDT"
                name = i.find("div", {"class": "tw-name"})
                headliner = name.text.upper()
                notes= " ".join(headliner.split()) + " at Dante's"
                twdate = i.find("span", {"class":"tw-event-date"})
                date= twdate.text
                try:
                    day = datetime.datetime.strptime(date, '%B %d, %Y').replace(2018)
                except ValueError:
                    continue
                if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
                    day = day.replace(2018)
                else:
                    day = day.replace(2019)
                event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
                if created:
                    print(event, 'Created')
                else:
                    print(event, "Exists already")

##HAWTHORNE THEATRE WORKS
class Command(BaseCommand):
    help = "Scrapes the for Events at Hawthorne Theatre"

    def handle(self, *args, **options):
        self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))

    class EventsConfigHT(AppConfig):
        name = 'events'
        url= 'https://hawthornetheatre.com/events/'
        data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        sauce = data.text
        soup = bs.BeautifulSoup(sauce, "html.parser")
        for i in soup.find_all("div", {"class":"rhino-event-center"}):
            start_time = "7:00 PM PDT"
            end_time = "11:00 PM PDT"
            name = i.find("h2", {"class": "rhino-event-header"})
            theo = name.text.upper()
            headliner = " ".join(theo.split())
            subline = i.find("h3", {"class": "rhino-event-subheader"})
            if subline == None:
                continue
            else:
                sub = subline.text
            notes= headliner +" "+ sub +" at Hawthorne Theatre"
            month = i.find("p", {"class":"rhino-event-date"})
            if month == None:
                continue
            else:
                date1 = month.text
            try:
                day = datetime.datetime.strptime(date1, '%B %d').replace(2018)
            except ValueError:
                continue
            if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
                day = day.replace(2018)
            else:
                day = day.replace(2019)
            event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
            if created:
                print(event, 'Created')
            else:
                print(event, "Exists already")

##ANALOG CAFE WORKS
class Command(BaseCommand):
    help = 'Scrapes the for Events at Analog'

    def handle(self, *args, **options):
        self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))

    class EventsConfigAn(AppConfig):
        name = 'events'
        data = requests.get('https://www.eventbrite.com/o/analog-theater-and-cafe-3308778446')
        sauce = data.text
        soup = bs.BeautifulSoup(sauce, "html.parser")
        for i in soup.find_all("div", {"class":"list-card__body"}):
            date = i.find("time", {"class":"list-card__date"})
            dates = date.text
            strpdate = " ".join(dates.split())
            band_name = strpdate.split(" ")
            day1 = band_name[1] +" " +band_name[2]
            try:
                day = datetime.datetime.strptime(day1, '%b %d').replace(2018)
            except ValueError:
                continue
            if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
                day = day.replace(2018)
            else:
                day = day.replace(2019)
            band = i.find("div",{"class":"list-card__title"})
            act = band.text.upper()
            notes = " ".join(act.split())
            start_time = "7:00 PM PDT"
            end_time = "11:00 PM PDT"
            event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
            if created:
                print(event, 'Created')
            else:
                print(event, "Exists already")

##CRYSTAL BALL ROOM WORKS
class Command(BaseCommand):
    help = 'Scrapes for events at Cyrstal Ballroom'

    def handle(self, *args, **options):
        self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))

    ## Scrape for Events Table
    class EventsConfigMc(AppConfig):
        name = 'events'
        data = requests.get('http://cdn.mcmenamins.com/events/search/Any?joint_name=Crystal+Ballroom&location_id=2')
        sauce = data.text
        soup = bs.BeautifulSoup(sauce, "html.parser")
        for link in soup.find_all("div", {"class":"details"}):
            start_time = "07:00 PM PDT"
            end_time = "10:00 PM PDT"
            titles = link.contents[3].text.split()
            notes = (" ".join(titles) + " at Crystal Ballroom")
            show_date = link.contents[5].text
            day = datetime.datetime.strptime(show_date, '%A, %B %d').replace(2018)
            if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
                day = day.replace(2018)
            else:
                day = day.replace(2019)
            print(day)
            event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
            if created:
                print(event, 'Created')
            else:
                print(event, "Exists already")

##WONDER BALLROOM WORKS
class Command(BaseCommand):
    help = 'Scrapes the for Events at Wonder Ballroom'

    def handle(self, *args, **options):
        self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))

    class EventsConfigWo(AppConfig):
        name = 'events'
        data = requests.get('https://www.ticketfly.com/api/events/upcoming.rss?orgId=537', headers={'User-Agent': 'Mozilla/5.0'})
        sauce = data.text
        soup = bs.BeautifulSoup(sauce, "html.parser")
        for i in soup.find_all("title"):
            band_name = i.text.upper()
            notes = (re.sub(r'(\ at W).*$', "", band_name) + " at Wonder Ballroom")
            show_date = re.sub(r'(.*(\ on ))', "", band_name)
            start_time = re.sub(r'(.*(\w018 ))', "", band_name)
            end_time = "11:00 PM PDT"
            date = re.sub(r'(\ 0).*$', "", show_date)
            try:
                day = datetime.datetime.strptime(date, '%d/%m/%Y').replace(2018)
            except ValueError:
                continue
            if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
                day = day.replace(2018)
            else:
                day = day.replace(2019)
            event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
            if created:
                print(event, 'Created')
            else:
                print(event, "Exists already")

# ##LOVECRAFT BAR BROKEN TUMBLR FORMAT SITE
# class Command(BaseCommand):
#     help = "Scrapes the for Events at LoveCraft Bar"
#
#     class EventsConfigHT(AppConfig):
#         name = 'events'
#         url= 'https://thelovecraftbar.com/specialevents'
#         data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#         sauce = data.text
#         soup = bs.BeautifulSoup(sauce, "html.parser")
#         for i in soup.find_all("section", {"class":"post"}):
#             start_time = "7:00 PM PDT"
#             end_time = "11:00 PM PDT"
#             name = i.find("header", {"class": "post-header"})
#             theo = name.text
#             notes= theo + " at LoveCraft Bar"
#             month = i.find("a", {"class": "meta-item post-date"})
#             if month == None:
#                 continue
#             else:
#                 date1 = month.text
#             try:
#                 day = datetime.datetime.strptime(date1, '%B %d, %Y').replace(2018)
#             except ValueError:
#                 continue
#             if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
#                 day = day.replace(2018)
#             else:
#                 day = day.replace(2019)
#             event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
#             if created:
#                 print(event, 'Created')
#             else:
#                 print(event, "Exists already")

# ##BLACKWATER BAR BROKEN
# class Command(BaseCommand):
#     help = "Scrapes the for Events at BlackWater Bar"
#
#     class EventsConfigRB(AppConfig):
#         name = 'events'
#         data = requests.get('http://pc-pdx.com/venues/blackwater', headers={'User-Agent': 'Mozilla/5.0'})
#         sauce = data.text
#         soup = bs.BeautifulSoup(sauce, "html.parser")
#         for i in soup.find_all("div", {"class":"show-listing show-listing-item crowdAllAges"}):
#             print(i)
            # e = i.find_all("a", {"class":"bands slider-spot "})
            # f = list(map(e.strip))
            # print(f)
            # names = " ".join(r.split())
            # print(names)
            # print(" ")
        # for i in soup:
        #     band = i.find_all("a", {"class":"bands slider-spot "})
        #     notes = band.text
        #     print(notes)
        #     name2 = name.find_all("a")
        #     notes = name2.text
        #     print(notes)
        #     date1 = i.find("ul", {"class":"list-column third-column"})
        #     date2 = date1.find("li")[1]
        #     date3 = date2.tex
        #     try:
        #         day = datetime.datetime.strptime(date3, '%A %d/%m/%Y').replace(2018)
        #     except TypeError:
        #         continue
        #     if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
        #         day = day.replace(2018)
        #     else:
        #         day = day.replace(2019)
        #     start_time = "7:00 PM PDT"
        #     end_time = "11:00 PM PDT"
        #     event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
        #     if created:
        #         print(event, 'Created')
        #     else:
        #         print(event, "Exists already")
#
# ## ROSELAND THEATER BROKEN
# class Command(BaseCommand):
#     help = "Scrapes the for Events at Roseland Theater"
#
#     def handle(self, *args, **options):
#         self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))
#
#     class EventsConfigHT(AppConfig):
#         cafile = 'wpengine.com'
#         name = 'events'
#         url= 'https://www.songkick.com/venues/32177-roseland-theater/calendar'
#         data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#         sauce = data.text
#         soup = bs.BeautifulSoup(sauce, "html.parser")
#         for i in soup.find_all("li"):
#             start_time = "7:00 PM PDT"
#             end_time = "11:00 PM PDT"
#             name = i.find("p", {"class": "artists summary"})
#             if name == None:
#                 continue
#             else:
#                 theo = name.text
#             notes = " ".join(theo.split())
#             month = i.time
#             if month == None:
#                 continue
#             else:
#                 date1 = month.text
#             if len(date1) < 38:
#                 try:
#                     day = datetime.datetime.strptime(date1, '<time datetime="%Y-%m-%d"></time>').replace(2018)
#                     print(day)
#                 except ValueError:
#                     continue
#                 if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
#                     day = day.replace(2018)
#                 else:
#                     day = day.replace(2019)
#
#                     event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes,
#                                                                  day=day)
#                     if created:
#                         print(event, 'Created')
#                     else:
#                         print(event, "Exists already")
#             else:
#                 try:
#                     day = datetime.datetime.strptime(date1, '<time datetime="%Y-%m-%dT%H:%M:%S-%z"></time>').replace(2018)
#                 except ValueError:
#                     continue
#                 if int(day.strftime('%m')) >= int(datetime.datetime.now().strftime('%m')) <= 12:
#                     day = day.replace(2018)
#                 else:
#                     day = day.replace(2019)
#
#                     event, created = Event.objects.get_or_create(start_time=start_time, end_time=end_time, notes=notes, day=day)
#                     if created:
#                         print(event, 'Created')
#                     else:
#                         print(event, "Exists already")
#

# # ## Populate Background for each div in Bands Page ##
# # class BandPic(AppConfig):
# #     urls = ['https://ruinedit.bandcamp.com/',
# #             'https://trustissuespdx.bandcamp.com/',
# #             'https://deadcountrypdx.bandcamp.com',
# #             'https://braveinthegrave.bandcamp.com',
# #             'https://iced-hc.bandcamp.com/',
# #             'https://deadwitch.bandcamp.com',
# #             'https://worws.bandcamp.com',
# #             'https://cuttingthrough.bandcamp.com',
# #             'https://machoboys.bandcamp.com',
# #             ]
# #     for data in urls:
# #         first = requests.get(data)
# #         sauce = first.text
# #         soup = bs.BeautifulSoup(sauce, "html.parser")
# #         img = soup.findAll(name="img")
# #         try:
# #             pics = str((img)[3])
# #         except IndexError:
# #             pics = str((img)[0])
# #         parsed = (re.search(r'(?<=https)(.*)(?=.jpg)', pics)[1])
# #         bandpic = ("https" + parsed + ".jpg")
# #         picture, created = band.objects.get_or_create(bandpic=bandpic)
# #         if created:
# #             print(picture, 'Created')
# #         else:
# #             print(picture, "Exists already")




eventslist = Event.objects.all()
bandslist = searchBandSugg.objects.all()
for i in eventslist:
    if i.day < datetime.date.today():
        i.delete()
    # elif i.notes not in bandslist:
    #     i.delete()
    else:
        pass
#
# ####Band Name Database Scrapers
#
# class BandConfigRe(AppConfig):
#     name = 'bands'
#     data = requests.get('https://store.relapse.com/bands', headers={'User-Agent': 'Mozilla/5.0'})
#     sauce = data.text
#     soup = bs.BeautifulSoup(sauce, "html.parser")
#     for i in soup.find_all("ul", {"class":"mp-productfilter-list"}):
#         for j in i.find_all("a"):
#             yhyh = j.text
#             name = " ".join(yhyh.split())
#             username = None
#             band, created = searchBandSugg.objects.get_or_create(name=name, username=username)
#             if created:
#                 print(band, 'Created')
#             else:
#                 print(band, "Exists already")
#
# class BandConfigBBB(AppConfig):
#     name = 'bands'
#     data = requests.get('http://www.triple-brecords.com/index/')
#     sauce = data.text
#     soup = bs.BeautifulSoup(sauce, "html.parser")
#     for i in soup.find_all("h2", {"class": "project-title"}):
#         yhyh = i.text
#         name = " ".join(yhyh.split())
#         username = None
#         band, created = searchBandSugg.objects.get_or_create(name=name,username=username)
#         if created:
#             print(band, 'Created')
#         else:
#             print(band, "Exists already")
# class BandConfigDW(AppConfig):
#     name = 'bands'
#     data = requests.get('https://deathwishinc.bandcamp.com/artists')
#     sauce = data.text
#     soup = bs.BeautifulSoup(sauce, "html.parser")
#     for i in soup.find_all("div", {"class":"artists-grid-name"}):
#         yhyh = i.text
#         name = " ".join(yhyh.split())
#         username = None
#         band, created = searchBandSugg.objects.get_or_create(name=name, username=username)
#         if created:
#             print(band, 'Created')
#         else:
#             print(band, "Exists already")
#
# class BandConfigRR(AppConfig):
#     name = 'bands'
#     data = requests.get('http://www.roadrunnerrecords.com/artists')
#     sauce = data.text
#     soup = bs.BeautifulSoup(sauce, "html.parser")
#     for i in soup.find_all("a", {"class": "artistname"}):
#         yhyh = i.text
#         name = " ".join(yhyh.split())
#         username = None
#         band, created = searchBandSugg.objects.get_or_create(name=name, username=username)
#         if created:
#             print(band, 'Created')
#         else:
#             print(band, "Exists already")
#
#
# class BandConfigEV(AppConfig):
#     name = 'bands'
#     data = requests.get('http://www.equalvision.com/artists/')
#     sauce = data.text
#     soup = bs.BeautifulSoup(sauce, "html.parser")
#     for i in soup.find_all("h3"):
#         yhyh = i.text
#         name = " ".join(yhyh.split())
#         username = None
#         band, created = searchBandSugg.objects.get_or_create(name=name, username=username)
#         if created:
#             print(band, 'Created')
#         else:
#             print(band, "Exists already")
#
# class BandConfigRise(AppConfig):
#     name = 'bands'
#     data = requests.get('http://www.riserecords.com/artists.php')
#     sauce = data.text
#     soup = bs.BeautifulSoup(sauce, "html.parser")
#     for i in soup.find_all("p"):
#         yhyh = i.text
#         name= " ".join(yhyh.split())
#         username = None
#         band, created = searchBandSugg.objects.get_or_create(name=name, username=username)
#         if created:
#             print(band, 'Created')
#         else:
#             print(band, "Exists already")

class BandConfigRR(AppConfig):
    name = 'bands'
    for i in range(201):  # Number of pages plus one
        url = "https://bandcamp.com/?g=metal&s=top&p={}&gn=0&f=all&t=hardcore#discover".format(i)
        r = requests.get(url)
        sauce = r.text
        soup = bs.BeautifulSoup(sauce, "html.parser")
        for i in soup.find_all("div", {"class": "col col-3-12 discover-item"}):
            for j in i.find("a", {"class": "item-artist"}):
                yhyh = j.text
                name = " ".join(yhyh.split())
                username = None
                band, created = searchBandSugg.objects.get_or_create(name=name, username=username)
                if created:
                    print(band, 'Created')
                else:
                    print(band, "Exists already")