AKADEMIK KAZIMA  
YOK Akademik Veri Toplama Sistemi  
--------------------------------------------------  

PROJE ACIKLAMASI  
Bu proje, Kirikkale Universitesi akademisyenlerinin YOK Akademik sayfasindaki bilgilerini otomatik olarak cekerek JSON formatinda kaydeden bir web scraping uygulamasidir. Kitaplar, tezler ve makaleler gibi akademik calismalari duzenli bir sekilde toplar.  

KULLANILAN TEKNOLOJILER  
- Python 3  
- Selenium (Tarayici otomasyonu)  
- BeautifulSoup (HTML veri analizi)  
- webdriver-manager (ChromeDriver yonetimi)  
- JSON (Veri saklama)  

KURULUM  
1. Gerekli kutuphaneleri yukleyin:  
   pip install selenium beautifulsoup4 webdriver-manager  

2. Kodu calistirin:  
   python akademik_kazima.py  

KULLANIM  
- Cikti Dosyasi: tum_akademik_veriler.json  
- Veri Yapisi Ornegi:  
  {  
    "unvan": "Prof. Dr.",  
    "ad_soyad": "Ornek Akademisyen",  
    "bolum": "Bilgisayar Muhendisligi",  
    "kitaplar": [{"kitap_adi": "...", "basim_yili": "2022"}],  
    "tezler": [{"universite": "...", "yil": "2020", "hazirlayan": "...", "tez_adi": "..."}],  
    "makaleler": [{"makale_adi": "...", "yayin_yeri": "...", "yil": "2023", "yazarlar": ["..."], "etiketler": {...}}]  
  }  

SURUM GECMISI  

1.0 (Ilk Surum)  
- Temel akademisyen bilgileri (unvan, ad, bolum) cekildi.  
- JSON dosyasina basit kayit.  

2.0 (Kitap Odakli)  
- Kitaplarin baslik ve basim yili cekildi.  
- Hata yonetimi iyilestirildi.  

2.1 (Tez Eklentisi)  
- Yonetilen tez bilgileri eklendi (universite, yil, hazirlayan, tez adi).  
- Coklu sekme yonetimi.  

KATKIDA BULUNMA  
- Hata bildirimleri icin Issue acin.  
- Yeni ozellikler icin Pull Request gonderin.  

LISAN  
Bu proje MIT Lisansi altinda lisanslanmistir. Detaylar icin LICENSE dosyasini inceleyin.  

ILETISIM  
vahdeterenbozyil@gmail.com