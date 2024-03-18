import os
from django.conf import settings
from django.shortcuts import render
from flask import redirect
from pymongo import MongoClient
import pytz

istanbulTZ = pytz.timezone("Europe/Istanbul")
# MongoDB'ye bağlan
mert = "Bursa.2001"
myclient = MongoClient("mongodb+srv://mebua2001:" + mert + "@mebua.79c6uai.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]
messagesCol = mydb["Messages"]
ilerlemeleCol = mydb["ilerleme"]
egzersizCol = mydb["Egzersizler"]
antrenorCol = mydb["antrenor"]

# Giriş sayfasını gösteren view
def yonetici(request):
    if request.method == 'POST':
        # Formdan kullanıcı adı ve şifre al
        email = request.POST.get('email')
        
        password = request.POST.get('sifre')
        users = mycol.find_one({},{"_id":0})
        print(users)

        # MongoDB koleksiyonunda kullanıcı adı ve şifre ile sorgu yap
        user_data = mycol.find_one({"email": email, "sifre": password})
        print(user_data)

        if user_data:
            # Eğer kullanıcı verisi varsa, kimlik doğrulanmış şablonu göster
            users = mycol.find()
            coachs = antrenorCol.find()


            context = {
                'user': users,
                'coach': coachs
             }

            request.session["user_email"] = user_data.get("email")
            return render(request, "kimlikdogru.html", context)
        else:
            # Eğer kullanıcı verisi yoksa, kimlik doğrulama başarısız şablonunu göster
            return render(request, "kimlikyanlis.html")

    # Eğer istek methodu GET ise, sadece giriş sayfasını göster
    return render(request, "admin.html")


def danisman_ekle(request):
    if request.method == 'POST':
        # Formdan verileri al
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        dogum_tarihi = request.POST.get('dogumTarihi')
        cinsiyet = request.POST.get('cinsiyet')
        email = request.POST.get('email')
        sifre = request.POST.get('sifre')
        telefon = request.POST.get('telefon')

       

        # MongoDB'ye eklemek üzere bir belge oluştur
        user_data = {
            'ad': ad,
            'soyad': soyad,
            'dogum_tarihi': dogum_tarihi,
            'cinsiyet': cinsiyet,
            'email': email,
            'sifre': sifre,
            'telefon': telefon,
           
        }

        # Belgeyi MongoDB koleksiyonuna ekle
        mycol.insert_one(user_data)

        # Başarılı bir kayıt sonrasında kullanıcıyı başka bir sayfaya yönlendir veya ek işlemler gerçekleştir
        users = mycol.find()
        coachs = antrenorCol.find()


        context = {
            'user': users,
            'coach': coachs
        }

        request.session["user_email"] = user_data.get("email")
        return render(request, "kimlikdogru.html", context)

    users = mycol.find()
    coachs = antrenorCol.find()
    context = {
        'user': users,            
        'coach': coachs
    }

    request.session["user_email"] = user_data.get("email")
    return render(request, "kimlikdogru.html", context)



def koc_ekle(request):
    if request.method == 'POST':
        # Formdan verileri al
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        dogum_tarihi = request.POST.get('dogumTarihi')
        cinsiyet = request.POST.get('cinsiyet')
        email = request.POST.get('email')
        sifre = request.POST.get('sifre')
        telefon = request.POST.get('telefon')
        uzmanlik_alani = request.POST.get('uzmanlik_alani')
        deneyim = request.POST.get('deneyim')

            # Başka işlemler gerçekleştirilebilir, örneğin dosya adını veritabanına kaydet

        # MongoDB'ye eklemek üzere bir belge oluştur
        user_data = {
            'ad': ad,
            'soyad': soyad,
            'dogum_tarihi': dogum_tarihi,
            'cinsiyet': cinsiyet,
            'email': email,
            'sifre': sifre,
            'telefon': telefon,
            'uzmanlik_alani': uzmanlik_alani,
            'deneyim': deneyim,

        }

        # Belgeyi MongoDB koleksiyonuna ekle
        antrenorCol.insert_one(user_data)
        users = mycol.find()
        coachs = antrenorCol.find()


        context = {
            'user': users,
            'coach': coachs
        }

        request.session["user_email"] = user_data.get("email")
        return render(request, "kimlikdogru.html", context)
    # Eğer istek methodu GET ise, sadece kayıt formunu göster
    users = mycol.find()
    coachs = antrenorCol.find()


    context = {
        'user': users,
        'coach': coachs
    }

    request.session["user_email"] = user_data.get("email")
    return render(request, "kimlikdogru.html", context)