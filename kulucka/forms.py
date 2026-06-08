from django import forms
from .models import Urun, Profil

class UrunForm(forms.ModelForm):
    class Meta:
        model = Urun
        fields = ['isim', 'kategori', 'durum', 'aciklama', 'mevcut_fiyat', 'gorsel']
        widgets = {
            'isim': forms.TextInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Örn: Erken Hasat Zeytinyağı'}),
            'kategori': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'durum': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'aciklama': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 3, 'placeholder': 'Ürün detayları...'}),
            'mevcut_fiyat': forms.NumberInput(attrs={'class': 'form-control rounded-3', 'placeholder': '0.00'}),
            'gorsel': forms.FileInput(attrs={'class': 'form-control rounded-3'}),
        }

# 👤 SATICI KENDİ BİLGİLERİNİ GÜNCELLEME FORMU
class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['kullanici_tipi', 'sehir', 'telefon']
        widgets = {
            'kullanici_tipi': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'sehir': forms.TextInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Örn: Şanlıurfa'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Örn: 0505XXXXXXX'}),
        }