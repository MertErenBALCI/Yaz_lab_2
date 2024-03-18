import os
from django.http import JsonResponse
from django.shortcuts import render, redirect
from pymongo import MongoClient
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone as tzz
from django.urls import reverse

import datetime
import pytz

from django.views.decorators.csrf import csrf_exempt
import json
from bson import json_util


from bson import ObjectId

istanbulTZ = pytz.timezone("Europe/Istanbul")
# MongoDB'ye bağlan
mert = "Bursa.2001"
myclient = MongoClient("mongodb+srv://mebua2001:" + mert + "@mebua.79c6uai.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]
messagesCol = mydb["Messages"]
ilerlemeleCol = mydb["ilerleme"]
egzersizCol = mydb["Egzersizler"]

class ObjectIdEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super(ObjectIdEncoder, self).default(o)


# Create your views here.
def danisman(request):

    return render(request, 'danisman.html')

def danisman_anasayfa(request):

    userEmail = request.session["user_email"]

    
    user_data = mycol.find_one({"email": userEmail})

    return render(request, "danisman_kimlik_dogru.html", {"user": user_data})

# Giriş sayfasını gösteren view
def danisman_giris(request):
    if request.method == 'POST':
        # Formdan kullanıcı adı ve şifre al
        email = request.POST.get('email')
        
        password = request.POST.get('sifre')

        print(email+password)
        users = mycol.find_one({},{"_id":0})
        print(users)
        # MongoDB koleksiyonunda kullanıcı adı ve şifre ile sorgu yap
        user_data = mycol.find_one({"email": email, "sifre": password})
        print(user_data)

        if user_data:
            # Eğer kullanıcı verisi varsa, kimlik doğrulanmış şablonu göster
            #return redirect('danisman_kimlik_dogru')  # Kullanıcıyı doğrulama sayfasına yönlendir
            request.session["user_email"] = user_data.get("email")
            return redirect("danisman_anasayfa")
        else:
            # Eğer kullanıcı verisi yoksa, kimlik doğrulama başarısız şablonunu göster
            return redirect("danisman")
        
    # Eğer istek methodu GET ise, sadece giriş sayfasını göster
    return render(request, "danisman_giris.html")

def danisman_kaydol(request):
    if request.method == 'POST':
        # Formdan verileri al
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        dogum_tarihi = request.POST.get('dogumTarihi')
        cinsiyet = request.POST.get('cinsiyet')
        email = request.POST.get('email')
        sifre = request.POST.get('sifre')
        telefon = request.POST.get('telefon')

        # Dosya yüklemesi varsa
        if 'profilFoto' in request.FILES:
            profil_foto = request.FILES['profilFoto']

            # Dosyayı belirli bir konuma kaydet
            fs = FileSystemStorage()
            filename = fs.save(profil_foto.name, profil_foto)

            # Dosyanın tam yolunu al
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

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
            'profil_foto': filename,  # Dosya adını veritabanına kaydet
            # Gerekirse daha fazla alan ekleyebilirsin
        }

        # Belgeyi MongoDB koleksiyonuna ekle
        mycol.insert_one(user_data)

        # Başarılı bir kayıt sonrasında kullanıcıyı başka bir sayfaya yönlendir veya ek işlemler gerçekleştir
        return render(request, "danisman.html")

    # Eğer istek methodu GET ise, sadece kayıt formunu göster
    return render(request, "danisman_kaydol.html")

def danisman_forgot_password(request):
    if request.method == 'POST':
        # Formdan verileri al
        email = request.POST.get('email')
        sifre = request.POST.get('sifre')
        sifreOnay = request.POST.get('sifreOnay')

        if(sifre == sifreOnay):
            data = mycol.find({"email":email})
            if(data):
                result = mycol.update_one({"email": email}, {"$set": {"sifre": sifre}})
            else:
                print("e posta bulunamadı")

        else:
            print("sifreler eşleşmiyor")


        # Başarılı bir kayıt sonrasında kullanıcıyı başka bir sayfaya yönlendir veya ek işlemler gerçekleştir
        return render(request, "danisman_giris.html")

    # Eğer istek methodu GET ise, sadece kayıt formunu göster
    return render(request, "danisman_forgot_password.html")


def danisman_kimlik_dogru(request):


    if request.method == 'POST':
        userEmail = request.session["user_email"]
        user_data = mycol.find_one({"email": userEmail})

        print(userEmail)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        if user_data:
            user_id = user_data.get("_id")
            
            # Kullanıcıya ait MongoDB belgesini güncelle
            email = user_data.get("email")
            
            date = tzz.now().astimezone(istanbulTZ).isoformat()
            yeniVeri = {
                "email": email,
                "tarih": date,
                "kilo": body.get('kilo'),
                         "boy": body.get("boy"),
                         "vucut_yag_orani": body.get('vucut_yag_orani'),
                         "kas_kutlesi": body.get("kas_kutlesi"),
                         "vucut_kitle_indeksi": body.get("vucut_kitle_indeksi")}
            
            mycol.update_one({"_id": user_id}, {"$set": {"kilo": body.get('kilo'), "boy": body.get("boy"), "vucut_yag_orani": body.get('vucut_yag_orani'),"kas_kutlesi": body.get("kas_kutlesi"),"vucut_kitle_indeksi": body.get("vucut_kitle_indeksi")}})
            ilerlemeleCol.insert_one(yeniVeri)
        # 'user' verisini içeren şablonu göster
    return render(request, "danisman_kimlik_dogru.html", {'user': user_data, 'eee': email})
    
def bilgiGuncelle(request):
    
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            userEmail = request.session["user_email"]
            user_data = mycol.find_one({"email": userEmail})
            
            if user_data:
                user_id = user_data.get("_id")
                # Kullanıcıya ait MongoDB belgesini güncelle
                email = user_data.get("email")
                yeniVeri = {
                    "ad": body.get("ad"),
                    "soyad": body.get("soyad"),
                    "dogum_tarihi": body.get("dogum_tarihi"),
                    "cinsiyet": body.get("cinsiyet"),
                    "email": body.get("email"),
                    "telefon": body.get("telefon"),
                    "profil_foto": body.get("profil_foto")  # Yeni eklendi
                }
                user_data["ad"] = yeniVeri["ad"]
                user_data["profil_foto"] = yeniVeri["profil_foto"]
                mycol.update_one({"_id": user_id}, {"$set": yeniVeri})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # 'user' verisini içeren şablonu göster
    return render(request, "danisman_kimlik_dogru.html", {'user': user_data})

def mesajYaz(request):
    global user_data

    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            userEmail = request.session["user_email"]
            user_data = mycol.find_one({"email": userEmail})
            
            if user_data:
                # Kullanıcıya ait MongoDB belgesini güncelle
                email = user_data.get("email")
                ad = user_data.get("ad")
                soyad = user_data.get("soyad")

                date = tzz.now().astimezone(istanbulTZ).isoformat()

                yeniVeri = {
                    "tarih": date,
                    "gonderici": email,
                    "gondericiAdi": ad,
                    "gondericiSoyadi": soyad,
                    "alici": body.get("mesajAlici"),
                    "mesaj": body.get("mesajText")
                }

                messagesCol.insert_one(yeniVeri)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # 'user' verisini içeren şablonu göster
    return render(request, "danisman_kimlik_dogru.html", {'user': user_data})

def mesajAl(request):
    
    email = request.session["user_email"]
    gonderilenMesajlar = messagesCol.find({"gonderici": email})
    alinanMesajlar = messagesCol.find({"alici": email})

    birlesikVeri = {"alinanMesajlar": alinanMesajlar, "gonderilenMesajlar": gonderilenMesajlar}
    
    json_data = json_util.dumps(birlesikVeri)

    return JsonResponse(json_data, safe=False, json_dumps_params={'default': json_util.default})
    #return render(request, "danisman_kimlik_dogru.html", kadwir)

def gecmisVeriAl(request):
    userEmail = request.session["user_email"]
    user_data = mycol.find_one({"email": userEmail})
    email = user_data.get("email")
    gecmisVeri = ilerlemeleCol.find({"email": email})

    
    json_data = json_util.dumps(gecmisVeri)

    return JsonResponse(json_data, safe=False, json_dumps_params={'default': json_util.default})

def egzersizAl(request):
    userEmail = request.session["user_email"]
    user_data = mycol.find_one({"email": userEmail})
    email = user_data.get("email")
    egzersizVeri = egzersizCol.find({"email": email})
    print(email)
    
    json_data = json_util.dumps(egzersizVeri)

    return JsonResponse(json_data, safe=False, json_dumps_params={'default': json_util.default})
    #return render(request, "danisman_kimlik_dogru.html", kadwir)

def danisman_cikis(request):
    request.session.clear()
    return redirect('danisman')

"""
@csrf_exempt
def danisman_kimlik_dogru(request):
    global user_data
    if request.method == "POST" and request.is_ajax():
        user_id = request.session.get('user_data')
        
        if user_id:
            user_data = mycol.find_one({"_id": ObjectId(user_id)})

            if user_data:
                # Güncelleme verilerini al
                updated_kilo = request.POST.get('kilo')
                updated_boy = request.POST.get('boy')
                # Diğer alanları ihtiyaca göre ekleyin

                # Kullanıcıya ait MongoDB belgesini güncelle
                mycol.update_one({"_id": user_data["_id"]}, {"$set": {"kilo": updated_kilo, "boy": updated_boy}})

                # Güncelleme işlemi tamamlandıktan sonra kullanıcı bilgilerini JSON formatında döndür
                response_data = {"success": True, "user": {"kilo": updated_kilo, "boy": updated_boy}}
                return JsonResponse(response_data)
                
    # Diğer durumlarda, normal sayfayı göster
    return render(request, "danisman_kimlik_dogru.html", {'user': user_data})"""