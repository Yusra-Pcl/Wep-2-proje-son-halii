from django.contrib import admin
from .models import Profil, Urun

admin.site.site_header = "Zanaat-AI Hub Yönetim Paneli"
admin.site.site_title = "Zanaat-AI Admin"
admin.site.index_title = "Platform Girişim ve Ürün Yönetimi"

@admin.register(Urun)
class UrunAdmin(admin.ModelAdmin):
    list_display = ('isim', 'kategori', 'mevcut_fiyat', 'ai_onerilen_fiyat', 'trend_skoru', 'sahibi')
    list_filter = ('kategori', 'trend_skoru')
    search_fields = ('isim', 'aciklama')

    # Üretici ürün eklerken sahibini otomatik giriş yapan kullanıcı yapar
    def save_model(self, request, obj, form, change):
        if not change:
            obj.sahibi = request.user
        super().save_model(request, obj, form, change)

    # Her üretici sadece kendi ürününü görür
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sahibi=request.user)


# 📞 PROFİL ALANINI ADMIN PANELİNDE GÖRÜNÜR YAPIYORUZ
@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    # Listeleme ekranında görünecek sütunlar
    list_display = ('user', 'kullanici_tipi', 'sehir', 'telefon')
    # Düzenleme ekranında görünecek alanlar (Telefonu buraya ekledik)
    fields = ('user', 'kullanici_tipi', 'sehir', 'biyografi', 'telefon')
