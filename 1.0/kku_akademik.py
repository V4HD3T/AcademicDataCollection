from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time

# ChromeDriver yolu
driver_path = "C:/Users/v4hd3/Desktop/SeleniumProje/chromedriver.exe"  # Güncellendi
service = Service(driver_path)

# Tarayıcı ayarları
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Selenium WebDriver'ı başlat
browser = webdriver.Chrome(service=service, options=options)

# Kırıkkale Üniversitesi Akademik Arama URL'si
url = "https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=6dpfJJ1BWbMj3e9TzohGWr8bd42xIAaXk95D_unwbs0Rd242XOlgWf9_adZszWwP"
browser.get(url)

# Verilerin yüklenmesini bekle
WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'AkademisyenGorevOgrenimBilgileri')]"))
)

# Akademik personel bilgilerini saklamak için liste
personnel_list = []

# Tüm sayfaları dolaşmak için döngü
while True:
    # Sayfa kaynağını çek ve BeautifulSoup ile işle
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    
    # Sayfadaki akademik personel linklerini bul
    academic_links = soup.find_all("a", href=True)
    
    for link in academic_links:
        if "AkademisyenGorevOgrenimBilgileri" in link['href']:
            # Kişiye özel sayfa bağlantısı
            person_url = f"https://akademik.yok.gov.tr{link['href']}"
            
            # Kişiye özel sayfaya git
            browser.get(person_url)
            WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.XPATH, "//h6"))
            )
            
            # Detay sayfasının kaynağını çek ve analiz et
            detail_source = browser.page_source
            detail_soup = BeautifulSoup(detail_source, "html.parser")
            
            try:
                # Unvan, ad-soyad bilgilerini bul
                title = detail_soup.find("h6").text.strip()
                name = detail_soup.find("h4").text.strip()

                # Bölüm bilgilerini al
                department = "Bilinmiyor"
                department_tag = detail_soup.find("span", class_="label label-primary")
                if department_tag:
                    department = department_tag.text.strip()

                # Eğer bu personel daha önce eklenmediyse, ekle
                if not any(person["name"] == name and person["department"] == department for person in personnel_list):
                    personnel_list.append({
                        "title": title,
                        "name": name,
                        "department": department
                    })
                    
                    # Çekilen bilgiyi ekrana yazdır
                    print(f"Personel: {name}, Unvan: {title}, Bölüm: {department}")
                
            except Exception as e:
                print(f"Bilgiler çekilirken hata oluştu: {e}")
            
            # Kişiye özel sayfadan ana sayfaya dön
            browser.back()
            WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'AkademisyenGorevOgrenimBilgileri')]"))
            )
    
    # Sonraki sayfa butonunu bul ve tıkla, yoksa döngüyü kır
    try:
        next_page = browser.find_element(By.LINK_TEXT, "»")
        next_page.click()
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'AkademisyenGorevOgrenimBilgileri')]"))
        )
    except:
        print("Tüm sayfalar tamamlandı!")
        break

# Verileri JSON formatında kaydet
with open("C:/Users/v4hd3/Desktop/SeleniumProje/kku_academic_personnel.json", "w", encoding="utf-8") as json_file:  # Güncellendi
    json.dump(personnel_list, json_file, ensure_ascii=False, indent=4)

print("Veriler başarıyla çekildi ve JSON dosyasına kaydedildi!")

# Tarayıcıyı kapat
browser.quit()