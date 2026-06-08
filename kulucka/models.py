from django.db import models
from django.contrib.auth.models import User

# 👤 1. MODEL: SATICI PROFIL TABLOSU
class Profil(models.Model):
    MAGAZA_TIPLERI = (
        ('zanaatkar', 'Mikro-Girişimci / Zanaatkar'),
        ('bireysel', 'Bireysel Satıcı (İkinci El)'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    kullanici_tipi = models.CharField(max_length=20, choices=MAGAZA_TIPLERI, default='zanaatkar', verbose_name="Kullanıcı Tipi")
    sehir = models.CharField(max_length=50, blank=True, null=True, verbose_name="Şehir")
    telefon = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefon Numarası")

    def __str__(self):
        return f"{self.user.username} - {self.get_kullanici_tipi_display()}"

# 📦 2. MODEL: PAZARYERİ ÜRÜNLERİ TABLOSU
class Urun(models.Model):
    KATEGORILER = (
        ('gida', 'Doğal Gıda Ürünleri'),
        ('aksesuar', 'Tasarım Aksesuar & Zanaat'),
        ('ceyiz', 'El Yapımı & Çeyiz Ürünleri'),
        ('canta', 'Giyim & Çanta'),
        ('kitap', 'Kitap & Kültür'),
    )
    DURUM_SECENEKLERI = (
        ('sifir', 'Sıfır / El Emeği'),
        ('ikinci_el', 'İkinci El / Kullanılmış Eşya'),
    )
    sahibi = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urunler', verbose_name="Satıcı")
    isim = models.CharField(max_length=200, verbose_name="Ürün Adı")
    kategori = models.CharField(max_length=20, choices=KATEGORILER, verbose_name="Kategori")
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='sifir', verbose_name="Ürün Durumu")
    aciklama = models.TextField(verbose_name="Ürün Açıklaması")
    mevcut_fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Satış Fiyatı (TL)")
    ai_onerilen_fiyat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="AI Önerilen Fiyat (TL)")
    trend_skoru = models.IntegerField(default=0, verbose_name="Trend / Beğeni Skoru")
    gorsel = models.ImageField(upload_to='urunler/', blank=True, null=True, verbose_name="Ürün Görseli")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.isim

# 💬 3. MODEL: YORUMLAR VE SATICIYA SORULAR TABLOSU
class Yorum(models.Model):
    YORUM_TIPI = (
        ('yorum', 'Kullanıcı Yorumu'),
        ('soru', 'Satıcıya Soru'),
    )
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE, related_name='yorumlar', verbose_name="İlgili Ürün")
    yazan = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yazan Kullanıcı")
    icerik = models.TextField(verbose_name="Mesaj İçeriği")
    tip = models.CharField(max_length=10, choices=YORUM_TIPI, default='yorum', verbose_name="İçerik Tipi")
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.yazan.username} - {self.get_tip_display()}"

# 🛒 4. MODEL: SEPET TABLOSU
class SepetElemani(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sepet_elemanlari')
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE)
    adet = models.PositiveIntegerField(default=1)
    eklenme_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.urun.isim} ({self.adet})"