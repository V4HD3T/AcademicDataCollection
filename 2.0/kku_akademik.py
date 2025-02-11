from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Tarayıcıyı başlat
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.maximize_window()

# Kırıkkale Üniversitesi Akademik Arama URL'si
url = "https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=6dpfJJ1BWbMj3e9TzohGWr8bd42xIAaXk95D_unwbs0Rd242XOlgWf9_adZszWwP"
browser.get(url)

# Akademik personel bilgilerini saklamak için liste
personnel_list = []

def get_books():
    kitaplar = []
    try:
        # Kitaplar menüsüne git
        WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@id='booksMenu']/a"))
        ).click()
        
        # Projeler div'inin yüklenmesini bekle
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "projects"))
        )
        
        kitaplar_soup = BeautifulSoup(browser.page_source, "html.parser")
        projects_div = kitaplar_soup.find("div", class_="projects")

        # Her bir row div'ini işle
        for row in projects_div.find_all("div", class_="row"):
            baslik = row.find("strong")
            yil_label = row.find("span", class_="label label-info")
            
            if baslik and yil_label:
                kitaplar.append({
                    "baslik": baslik.text.strip(),
                    "yil": yil_label.text.strip()
                })

    except Exception as e:
        print(f"Kitap çekme hatası: {str(e)}")
    finally:
        # Ana sayfaya geri dön
        browser.back()
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h6"))
        )
    return kitaplar

# Tüm sayfaları dolaşmak için döngü
while True:
    try:
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'AkademisyenGorevOgrenimBilgileri')]"))
        )
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        academic_links = soup.find_all("a", href=True)

        for link in academic_links:
            if "AkademisyenGorevOgrenimBilgileri" in link['href']:
                try:
                    # Yeni sekme aç
                    main_window = browser.current_window_handle
                    browser.switch_to.new_window('tab')
                    person_url = f"https://akademik.yok.gov.tr{link['href']}"
                    browser.get(person_url)
                    
                    # Temel bilgileri çek
                    WebDriverWait(browser, 30).until(
                        EC.presence_of_element_located((By.XPATH, "//h6"))
                    )
                    detail_soup = BeautifulSoup(browser.page_source, "html.parser")
                    title = detail_soup.find("h6").text.strip()
                    name = detail_soup.find("h4").text.strip()
                    department = detail_soup.find("span", class_="label label-primary").text.strip()

                    # Kitapları çek
                    kitaplar = get_books()

                    # Veriyi listeye ekle
                    personnel_list.append({
                        "unvan": title,
                        "ad_soyad": name,
                        "bolum": department,
                        "kitaplar": kitaplar
                    })
                    print(f"Veri çekildi: {name}")

                    # Sekmeyi kapat ve ana pencereye dön
                    browser.close()
                    browser.switch_to.window(main_window)

                except Exception as e:
                    print(f"Hata: {str(e)}")
                    if "no such window" in str(e).lower():
                        browser.quit()
                        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                        browser.get(url)
        
        # Sonraki sayfa
        try:
            next_page = WebDriverWait(browser, 15).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "»"))
            )
            next_page.click()
        except:
            print("Tüm sayfalar tamamlandı!")
            break

    except Exception as e:
        print(f"Ana döngü hatası: {str(e)}")
        break

# Verileri kaydet
with open("C:/Users/v4hd3/Desktop/SeleniumProje/kitaplar.json", "w", encoding="utf-8") as json_file:
    json.dump(personnel_list, json_file, ensure_ascii=False, indent=4)

print("Veriler başarıyla kaydedildi!")
browser.quit()