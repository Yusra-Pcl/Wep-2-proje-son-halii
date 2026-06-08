from django.urls import path
from . import views

app_name = 'kulucka'

urlpatterns = [
    path('', views.index, name='index'),
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('urun/<int:urun_id>/', views.detail, name='detail'),
    path('urun/<int:urun_id>/begen/', views.vote, name='vote'),
    
    # Düzenleme Sayfa Rotası
    path('urun/<int:urun_id>/duzenle/', views.urun_duzenle, name='urun_duzenle'),
    
    path('urun/<int:urun_id>/sepete-ekle/', views.sepete_ekle, name='sepete_ekle'),
    path('sepet/', views.sepet_goruntule, name='sepet_goruntule'),
    path('sepet/satin-al/', views.satin_al, name='satin_al'),
    
    path('profil/', views.profil, name='profil'),
    path('giris/', views.login_view, name='login'),
    path('kayit/', views.register_view, name='register'),
    path('cikis/', views.logout_view, name='logout'),
]