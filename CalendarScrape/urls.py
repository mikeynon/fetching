"""CalendarScrape URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from events import views

urlpatterns = [
                  url(r'^$', views.home, name='home'),
                  url(r'^signup/$', views.signup_view, name='signup'),
                  url(r'^admin/', admin.site.urls, name='admin'),
                  url(r'^login/$', auth_views.login, {'template_name': 'front/registration/login.html'}, name='login'),
                  url(r'^logout/$', auth_views.logout,  {'next_page': 'home'},name="logout"),
                # path('shows/', TemplateView.as_view(template_name="front/community.html")),
                  url(r'^shows/$', views.shows, name='shows'),
                  # url(r'^createBand/$', views.createBand, name='createBand'),
                  url(r'^livepics/$', views.livepics, name='livepics'),
                  url(r'^bands/$', views.bands, name='bands'),
                  url(r'^venues/$', views.venues, name='venues'),
                # url(r'^addband/$', views.createBand, name='addBand'),
                  url(r'^promoter/$', views.calendar, name='promoter'),
                  url(r'^add_attending/$', views.addLike, name="add_attending")
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





