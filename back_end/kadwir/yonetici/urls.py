from django.urls import path

from .views import yonetici
from .views import danisman_ekle
from .views import koc_ekle


urlpatterns = [
    # Example URL pattern in urls.py
    path('yonetici', yonetici, name='yonetici'),
    path('danisman_ekle', danisman_ekle, name='danisman_ekle'),
    path('koc_ekle', koc_ekle, name='koc_ekle'),



    # Diğer URL desenleri buraya eklenebilir,
    

]