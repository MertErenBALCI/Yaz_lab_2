from django.urls import path

from .views import danisman
from .views import danisman_giris
from .views import danisman_kaydol
from .views import danisman_kimlik_dogru
from .views import bilgiGuncelle
from .views import mesajYaz
from .views import mesajAl
from .views import gecmisVeriAl
from .views import egzersizAl
from .views import danisman_anasayfa
from .views import danisman_cikis
from .views import danisman_forgot_password


urlpatterns = [
   
    # Diğer URL desenleri buraya eklenebilir,
    #path('danisman', danisman, name='danisman'),

     # Diğer URL desenleri buraya eklenebilir,
    path('danisman_giris/', danisman_giris, name='danisman_giris'),
    path('danisman_forgot_password/', danisman_forgot_password, name='danisman_forgot_password'),


     # Diğer URL desenleri buraya eklenebilir,
    path('danisman_kaydol/', danisman_kaydol, name='danisman_kaydol'),

    path('danisman_kimlik_dogru/', danisman_kimlik_dogru, name='danisman_kimlik_dogru'),

    path('bilgiGuncelle/', bilgiGuncelle, name='bilgiGuncelle'),

    path('mesajYaz/', mesajYaz, name="mesajYaz"),

    path('mesajAl/', mesajAl, name="mesajAl"),

    path('gecmisVeriAl/', gecmisVeriAl, name="gecmisVeriAl"),

    path('egzersizAl/', egzersizAl, name="egzersizAl"),

    path('danisman_anasayfa/', danisman_anasayfa, name="danisman_anasayfa"),

    path('danisman_cikis', danisman_cikis, name="danisman_cikis")
    
]