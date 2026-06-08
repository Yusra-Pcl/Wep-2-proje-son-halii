from django.test import TestCase
from django.contrib.auth.models import User
from .models import Urun

class UrunYapayZekaTesti(TestCase):

    def setUp(self):
        """Test başlamadan önce geçici bir kullanıcı ve ürün oluşturur"""
        self.test_user = User.objects.create_user(username='testzanaatkar', password='password123')
        self.urun = Urun.objects.create(
            sahibi=self.test_user,
            isim="Test Ürünü",
            aciklama="Açıklama",
            mevcut_fiyat=100.00,
            trend_skoru=0
        )

    def test_baslangic_ai_fiyati(self):
        """Ürün ilk eklendiğinde AI fiyatının boş olduğunu doğrular"""
        self.assertIsNone(self.urun.ai_onerilen_fiyat)

    def test_dusuk_trend_ai_fiyat_artisi(self):
        """Trend skoru 10 ve altındayken AI fiyatının %5 fazla hesaplandığını test eder"""
        # Kullanıcı detay sayfasına girdi ve "Destekle" butonuna bastı (vote view simülasyonu)
        response = self.client.post(f'/{self.urun.id}/vote/')
        
        # Ürünü veri tabanından güncel haliyle çekiyoruz
        self.urun.refresh_from_db()
        
        # Trend 1 oldu (10'dan küçük), fiyat 100 TL'den 105 TL olmalı
        self.assertEqual(float(self.urun.ai_onerilen_fiyat), 105.00)

    def test_yuksek_trend_ai_fiyat_artisi(self):
        """Trend skoru 10'un üzerine çıktığında AI fiyatının %15 fazla hesaplandığını test eder"""
        # Ürünün trend skorunu yapay olarak 11 yapıyoruz
        self.urun.trend_skoru = 11
        self.urun.save()
        
        # Tekrar butona basma tetiklemesi yapıyoruz
        self.client.post(f'/{self.urun.id}/vote/')
        self.urun.refresh_from_db()
        
        # Trend 10'dan büyük olduğu için fiyat %15 artıp 115 TL olmalı
        self.assertEqual(float(self.urun.ai_onerilen_fiyat), 115.00)
