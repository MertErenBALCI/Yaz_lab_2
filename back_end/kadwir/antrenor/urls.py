from django.urls import path

from .views import antrenor_giris
from .views import antrenor_kimlik_dogru
from .views import antrenor_kimlik_yanlis
from .views import antrenor_anasayfa
from .views import antrenorBilgiGuncelle
from .views import danismanAl
from .views import antrenorEgzersizAl
from .views import antrenorEgzersizKaldir
from .views import egzersizEkle
from .views import antrenorVeriAl
from .views import antrenorMesajAl
from .views import antrenorMesajYaz
from .views import forgot_password


urlpatterns = [
   
    # Diğer URL desenleri buraya eklenebilir,
    path('antrenor_giris', antrenor_giris, name='antrenor_giris'),
    path('antrenor_anasayfa', antrenor_anasayfa, name="antrenor_anasayfa"),
    path('antrenor_kimlik_dogru', antrenor_kimlik_dogru, name='antrenor_kimlik_dogru'),
    path('antrenor_kimlik_yanlis', antrenor_kimlik_yanlis, name='antrenor_kimlik_yanlis'),
    path('forgot_password', forgot_password, name='forgot_password'),

    

    path('antrenorBilgiGuncelle', antrenorBilgiGuncelle, name="antrenorBilgiGuncelle"),

    path('danismanAl', danismanAl, name="danismanAl"),

    path('antrenorEgzersizAl', antrenorEgzersizAl, name="antrenorEgzersizAl"),

    path('antrenorEgzersizKaldir', antrenorEgzersizKaldir, name="antrenorEgzersizKaldir"),

    path('egzersizEkle', egzersizEkle, name="egzersizEkle"),

    path('antrenorVeriAl', antrenorVeriAl, name="antrenorVeriAl"),

    path('antrenorMesajAl', antrenorMesajAl, name='antrenorMesajAl'),

    path('antrenorMesajYaz', antrenorMesajYaz, name="antrenorMesajYaz")
]