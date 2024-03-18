from django.shortcuts import render, redirect
from pymongo import MongoClient
from django.http import HttpResponse, JsonResponse
from django.utils import timezone as tzz
import json
from bson import json_util

import pytz

istanbulTZ = pytz.timezone("Europe/Istanbul")
# MongoDB'ye bağlan
mert = "Bursa.2001"
myclient = MongoClient("mongodb+srv://mebua2001:" + mert + "@mebua.79c6uai.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
userCol = mydb["customers"]
messagesCol = mydb["Messages"]
ilerlemeCol = mydb["ilerleme"]
egzersizCol = mydb["Egzersizler"]
antrenorCol = mydb["antrenor"]



def forgot_password(request):
    if request.method == 'POST':
        # Formdan verileri al
        email = request.POST.get('email')
        sifre = request.POST.get('sifre')
        sifreOnay = request.POST.get('sifreOnay')

        if(sifre == sifreOnay):
            data = antrenorCol.find({"email":email})
            if(data):
                result = antrenorCol.update_one({"email": email}, {"$set": {"sifre": sifre}})
            else:
                print("e posta bulunamadı")

        else:
            print("sifreler eşleşmiyor")


        # Başarılı bir kayıt sonrasında kullanıcıyı başka bir sayfaya yönlendir veya ek işlemler gerçekleştir
        return render(request, "antrenor.html")

    # Eğer istek methodu GET ise, sadece kayıt formunu göster
    return render(request, "forgot_password.html")





# Giriş sayfasını gösteren view
def antrenor_giris(request):

    global user_data
    if request.method == 'POST':
        # Formdan kullanıcı adı ve şifre al
        email = request.POST.get('email')
        
        password = request.POST.get('sifre')
        users = antrenorCol.find_one({},{"_id":0})
        print(users)
        # MongoDB koleksiyonunda kullanıcı adı ve şifre ile sorgu yap
        user_data = antrenorCol.find_one({"email": email, "sifre": password})
        print(user_data)

        if user_data:
            # Eğer kullanıcı verisi varsa, kimlik doğrulanmış şablonu göster
            #return redirect('danisman_kimlik_dogru')  # Kullanıcıyı doğrulama sayfasına yönlendir
            request.session["antrenorEmail"] = email
            return redirect("antrenor_anasayfa")
        else:
            # Eğer kullanıcı verisi yoksa, kimlik doğrulama başarısız şablonunu göster
            return redirect("antrenor_giris")

    # Eğer istek methodu GET ise, sadece giriş sayfasını göster
    return render(request, "antrenor.html")

def antrenor_anasayfa(request):
    antrenorEmail = request.session["antrenorEmail"]

    antrenor_data = antrenorCol.find_one({"email": antrenorEmail})

    return render(request, "antrenor_anasayfa.html", {"antrenor": antrenor_data})

def antrenorBilgiGuncelle(request):
    
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            email = request.session["antrenorEmail"]
            antrenor_data = antrenorCol.find_one({"email": email})
            if antrenor_data:
                # Kullanıcıya ait MongoDB belgesini güncelle
                email = antrenor_data.get("email")
                yeniVeri = {
                    "ad": body.get("ad"),
                    "soyad": body.get("soyad"),
                    "email": body.get("email"),
                    "deneyim": body.get("deneyim"),
                    "uzmanlik": body.get("uzmanlik"),
                    "telefon": body.get("telefon"),
                    "profil_foto": body.get("profil_foto")  # Yeni eklendi
                }

                antrenor_data["ad"] = yeniVeri["ad"]
                antrenor_data["profil_foto"] = yeniVeri["profil_foto"]
                antrenorCol.update_one({"email": email}, {"$set": yeniVeri})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # 'user' verisini içeren şablonu göster
    return render(request, "antrenor_anasayfa.html")

def danismanAl(request): 
    antrenorEmail = request.session["antrenorEmail"]
    user_data = antrenorCol.find_one({"email": antrenorEmail})
    email = user_data.get("email")

    danisanlar = user_data.get("danisanlar")
    veri = []
    for danisanEmail in danisanlar:
        veri.append(userCol.find({"email": danisanEmail}))

    json_data = json_util.dumps(veri)

    return JsonResponse(json_data, safe=False, json_dumps_params={'default': json_util.default})
    #return render(request, "antrenor_anasayfa.html")

def antrenorEgzersizAl(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            email = body.get("egzersizEmail")
            
            egzersizler = egzersizCol.find({"email": email})

            json_data = json_util.dumps(egzersizler)

            return JsonResponse(json_data, safe=False, json_dumps_params={'default': json_util.default})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # 'user' verisini içeren şablonu göster
    return JsonResponse(None, safe=False, json_dumps_params={'default': json_util.default})

def antrenorEgzersizKaldir(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            ad = body.get("ad")
            email = body.get("email")

            
            aa = egzersizCol.delete_one({"egzersiz_adi": ad, "email": email})


            return render(request, "antrenor_anasayfa.html")
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # 'user' verisini içeren şablonu göster
    return render(request, "antrenor_anasayfa.html")

def egzersizEkle(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            

            yeniVeri = {
                    "email": body.get("email"),
                    "egzersiz_adi": body.get("egzersiz_adi"),
                    "hedef": body.get("hedef"),
                    "tekrar": body.get("tekrar"),
                    "video": body.get("video"),
                    "sure": body.get("sure"),
                    "tarih": body.get("tarih"),
                }   

            egzersizCol.insert_one(yeniVeri)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # 'user' verisini içeren şablonu göster
    return render(request, "antrenor_anasayfa.html")

def antrenorVeriAl(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            email = body.get("egzersizEmail")
            
            gecmisVeri = ilerlemeCol.find({"email": email})

            json_data = json_util.dumps(gecmisVeri)

            return JsonResponse(json_data, safe=False, json_dumps_params={'default': json_util.default})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # 'user' verisini içeren şablonu göster
    return JsonResponse(None, safe=False, json_dumps_params={'default': json_util.default})

def antrenorMesajAl(request):
    
    email = request.session["antrenorEmail"]
    gonderilenMesajlar = messagesCol.find({"gonderici": email})
    alinanMesajlar = messagesCol.find({"alici": email})

    birlesikVeri = {"alinanMesajlar": alinanMesajlar, "gonderilenMesajlar": gonderilenMesajlar}
    
    json_data = json_util.dumps(birlesikVeri)

    return JsonResponse(json_data, safe=False, json_dumps_params={'default': json_util.default})

def antrenorMesajYaz(request):
    global user_data

    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            userEmail = request.session["antrenorEmail"]
            user_data = antrenorCol.find_one({"email": userEmail})
            
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

def antrenor_kimlik_dogru(request):
    return render(request)

def antrenor_kimlik_yanlis(request):
    return render(request)