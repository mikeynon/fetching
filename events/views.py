import datetime

from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import UserForm, bandForm, DocumentForm, UserCreationForm
from .models import ContestCalendar, searchBandSugg, Document
from .models import Event
from calendar import monthrange
from operator import and_
from django.db.models import Q
from functools import reduce

# Create your views here.
def home(request):
    return render(request, 'front/index.html')

def bands(request):
    return render(request, 'front/bands.html')

def community(request):
    return render(request, 'front/community.html')

def livepics(request):
    doc = Document.objects.all()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'front/livepics.html', {
        'form': form,
        'doc': doc
    })

def venues(request):
    return render(request, 'front/venues.html')

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return render(request, 'front/community.html', {"username": username})
    else:
        # Return an 'invalid login' error message.
        # <script>alert("Login Invalid")</script>
        return render(request, 'front/index.html')

def logout_view(request):
    return render(request, 'front/index.html')

# def createBand(request):
#     # if request.POST:
#     #     form = bandForm(request.POST)
#     #     if form.is_valid():
#     #         # band = form.save(commit=False)
#     #         # band.user = request.User
#     #         form.save()
#     #         return redirect('front/community.html')
#     #     form = bandForm(request.POST)
#     else:
#         form = bandForm()
#     return render(request, 'front/community.html', {'form': form})

def shows(request):
    bandSug = []

    x = Event.objects.order_by('day')
    notes = ' // '.join(list(Event.objects.values_list('notes', flat=True))).split(' // ')

    # bandSug = searchBandSugg.objects.filter(reduce(and_, [Q(name__in=c) for c in notes]))
    #
    #
    # print(bandSug)
    form = bandForm(request.POST or None)
    context = {'Event': x, 'form': form, 'Bands': bandSug}
    if request.POST:
        if form.is_valid():
            band = form.save(commit=False)
            band.username = request.user
            band.save()
    return render(request, 'front/community.html', context)

def genpop(request):
    # bandSug = []

    x = Event.objects.order_by('day')
    notes = ' // '.join(list(Event.objects.values_list('notes', flat=True))).split(' // ')

    # bandSug = searchBandSugg.objects.filter(reduce(and_, [Q(name__in=c) for c in notes]))
    #
    #
    # print(bandSug)
    form = bandForm(request.POST or None)
    context = {'Event': x, 'form': form,
               # 'Bands': bandSug
               }
    if request.POST:
        if form.is_valid():
            band = form.save(commit=False)
            band.username = request.user
            band.save()
    return render(request, 'front/gencommun.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('shows')
    else:
        form = UserCreationForm()
    return render(request, 'front/signup.html', {'form': form})

def UserFormView(request):
    form_class = UserForm
    template_name = 'signup.html'
    form = UserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('community')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')

    return render(request, 'front/signup.html', {'form': form})

def addLike(request):
    if request.method =='POST':
        likes = Event.objects.get(pk=request.POST.get('id'))
        likes.likes += 1
        likes.save()
        return JsonResponse({'id':likes.likes})


def named_month(pMonthNumber):
    """
    Return the name of the month, given the month number
    """
    return datetime.date(1900, pMonthNumber, 1).strftime('%B')

def promoter(request):
    """
    Show calendar of events this month
    """
    lToday = datetime.datetime.now()
    return calendar(request, lToday.year, lToday.month)

def calendar(request, pYear, pMonth):
    """
    Show calendar of events for specified month and year
    """
    lYear = int(pYear)
    lMonth = int(pMonth)
    lCalendarFromMonth = datetime(lYear, lMonth, 1)
    lCalendarToMonth = datetime(lYear, lMonth, monthrange(lYear, lMonth)[1])
    lContestEvents = Event.objects.filter(date_of_event__gte=lCalendarFromMonth, date_of_event__lte=lCalendarToMonth)
    lCalendar = ContestCalendar(lContestEvents).formatmonth(lYear, lMonth)
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    lYearAfterThis = lYear + 1
    lYearBeforeThis = lYear - 1

    return render(request, 'front/promoter.html', {'Calendar' : mark_safe(lCalendar),
                                                   'Month' : lMonth,
                                                   'MonthName' : named_month(lMonth),
                                                   'Year' : lYear,
                                                   'PreviousMonth' : lPreviousMonth,
                                                   'PreviousMonthName' : named_month(lPreviousMonth),
                                                   'PreviousYear' : lPreviousYear,
                                                   'NextMonth' : lNextMonth,
                                                   'NextMonthName' : named_month(lNextMonth),
                                                   'NextYear' : lNextYear,
                                                   'YearBeforeThis' : lYearBeforeThis,
                                                   'YearAfterThis' : lYearAfterThis,
                                               })