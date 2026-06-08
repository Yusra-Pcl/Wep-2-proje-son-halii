from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import JsonResponse
from .models import Urun, Profil, Yorum, SepetElemani
from .forms import UrunForm, ProfilForm

# 🌐 ANA VİTRİN
def index(request):
    secilen_kategori = request.GET.get('kategori', 'genel')
    if secilen_kategori == 'genel' or not secilen_kategori:
        en_son_urunler = Urun.objects.all().order_by('-olusturulma_tarihi')
    else:
        en_son_urunler = Urun.objects.filter(kategori=secilen_kategori).order_by('-olusturulma_tarihi')
    return render(request, 'kulucka/index.html', {'en_son_urunler': en_son_urunler, 'secilen_kategori': secilen_kategori})

# 📜 HAKKIMIZDA
def hakkimizda(request):
    return render(request, 'kulucka/hakkimizda.html')

# 📸 ÜRÜN İNCELEME KISMI
def detail(request, urun_id):
    urun = get_object_or_404(Urun, pk=urun_id)
    urun_yorumlari = urun.yorumlar.filter(tip='yorum').order_by('-olusturulma_tarihi')
    urun_sorulari = urun.yorumlar.filter(tip='soru').order_by('-olusturulma_tarihi')
    
    if request.method == 'POST':
        icerik = request.POST.get('icerik')
        tip = request.POST.get('tip', 'yorum')
        if icerik:
            yazan_kullanici = request.user if request.user.is_authenticated else None
            if not yazan_kullanici:
                from django.contrib.auth.models import User
                yazan_kullanici = User.objects.first()
            Yorum.objects.create(urun=urun, yazan=yazan_kullanici, icerik=icerik, tip=tip)
            return redirect('kulucka:detail', urun_id=urun.id)
            
    context = {
        'urun': urun,
        'yorumlar': urun_yorumlari,
        'sorular': urun_sorulari,
    }
    return render(request, 'kulucka/detail.html', context)

# ❤️ BEĞENİ
def vote(request, urun_id):
    urun = get_object_or_404(Urun, pk=urun_id)
    urun.trend_skoru += 1
    if urun.mevcut_fiyat:
        artis_orani = 1 + (urun.trend_skoru * 0.02)
        urun.ai_onerilen_fiyat = round(float(urun.mevcut_fiyat) * artis_orani, 2)
    urun.save()
    return JsonResponse({
        'status': 'ok',
        'yeni_skor': urun.trend_skoru,
        'yeni_ai_fiyat': str(urun.ai_onerilen_fiyat if urun.ai_onerilen_fiyat else urun.mevcut_fiyat)
    })

# 🛒 SEPETE EKLEME
def sepete_ekle(request, urun_id):
    urun = get_object_or_404(Urun, pk=urun_id)
    sepet_sahibi = request.user if request.user.is_authenticated else None
    if not sepet_sahibi:
        from django.contrib.auth.models import User
        sepet_sahibi = User.objects.first()
    sepet_ogesi, created = SepetElemani.objects.get_or_create(user=sepet_sahibi, urun=urun)
    if not created:
        sepet_ogesi.adet += 1
        sepet_ogesi.save()
    return redirect('kulucka:sepet_goruntule')

# 🛍️ SEPETİ GÖRÜNTÜLEME
def sepet_goruntule(request):
    sepet_sahibi = request.user if request.user.is_authenticated else None
    if not sepet_sahibi:
        from django.contrib.auth.models import User
        sepet_sahibi = User.objects.first()
    sepet = SepetElemani.objects.filter(user=sepet_sahibi)
    toplam_tutar = sum(item.urun.mevcut_fiyat * item.adet for item in sepet)
    return render(request, 'kulucka/sepet.html', {'sepet': sepet, 'toplam_tutar': toplam_tutar})

# 💳 SATIN ALMA
def satin_al(request):
    sepet_sahibi = request.user if request.user.is_authenticated else None
    if not sepet_sahibi:
        from django.contrib.auth.models import User
        sepet_sahibi = User.objects.first()
    if request.method == 'POST':
        SepetElemani.objects.filter(user=sepet_sahibi).delete()
        return render(request, 'kulucka/basarili.html')
    return redirect('kulucka:sepet_goruntule')

# 👤 SATICI ÖZEL PANELİ
@login_required
def profil(request):
    profil_obj, created = Profil.objects.get_or_create(user=request.user)
    kullanici_urunleri = Urun.objects.filter(sahibi=request.user).order_by('-olusturulma_tarihi')
    toplam_ilgi = sum(u.trend_skoru for u in kullanici_urunleri)

    if request.method == 'POST':
        if 'urun_ekle' in request.POST:
            urun_form = UrunForm(request.POST, request.FILES)
            if urun_form.is_valid():
                yeni_urun = urun_form.save(commit=False)
                yeni_urun.sahibi = request.user
                yeni_urun.save()
                return redirect('kulucka:profil')
        elif 'profil_guncelle' in request.POST:
            profil_form = ProfilForm(request.POST, instance=profil_obj)
            if profil_form.is_valid():
                profil_form.save()
                return redirect('kulucka:profil')
    
    context = {
        'urunler': kullanici_urunleri,
        'profil': profil_obj,
        'urun_form': UrunForm(),
        'profil_form': ProfilForm(instance=profil_obj),
        'toplam_ilgi': toplam_ilgi,
    }
    return render(request, 'kulucka/profil.html', context)

# ✏️ YENİ EKLENEN ÜRÜN İSMİ DÜZENLEME MANTIĞI
@login_required
def urun_duzenle(request, urun_id):
    urun = get_object_or_404(Urun, pk=urun_id, sahibi=request.user)
    if request.method == 'POST':
        form = UrunForm(request.POST, request.FILES, instance=urun)
        if form.is_valid():
            form.save()
            return redirect('kulucka:profil')
    else:
        form = UrunForm(instance=urun)
    return render(request, 'kulucka/urun_duzenle.html', {'form': form, 'urun': urun})

# 🔑 GİRİŞ / KAYIT / ÇIKIŞ
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('kulucka:profil')
    else:
        form = AuthenticationForm()
    return render(request, 'kulucka/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            auth_login(request, form.save())
            return redirect('kulucka:profil')
    else:
        form = UserCreationForm()
    return render(request, 'kulucka/kayit.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('kulucka:index')
