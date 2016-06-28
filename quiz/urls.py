from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'quiz.views.index'),
    url(r'^vysledky$', 'quiz.views.vysledky'),
    url(r'^reset$', 'quiz.views.reset'),
    url(r'^id/(\d+)/(\w+)$', 'quiz.views.index'),
    url(r'^(\d+)$', 'quiz.views.show'),

)