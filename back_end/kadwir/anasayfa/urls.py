from django.urls import path, include
from .views import home
from .views import yonetici
from .views import antrenor
from .views import danisman
from .views import cikis
from .views import homePage
from .views import oncekiSayfa

urlpatterns = [
    path('', home, name='home'),
    # Diğer URL desenleri buraya eklenebilir,
    path('yonetici/', yonetici, name='yonetici'),
    path('antrenor/', antrenor, name='antrenor'),
    path('danisman/', danisman, name='danisman'),
    path('danisman/', include("danisman.urls")),
    path('antrenor/', include("antrenor.urls")),

    path('cikis', cikis, name="cikis"),

    path('homePage', homePage, name='homePage'),

    path('oncekiSayfa', oncekiSayfa, name="oncekiSayfa")

]
