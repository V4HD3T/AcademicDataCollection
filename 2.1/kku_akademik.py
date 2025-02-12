from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Tarayıcıyı Başlat
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.maximize_window()

# Ana URL
base_url = "https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=6dpfJJ1BWbMj3e9TzohGWr8bd42xIAaXk95D_unwbs0Rd242XOlgWf9_adZszWwP"
browser.get(base_url)

personel_listesi = []

def kitap_cek():
    kitaplar = []
    try:
        WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@id='booksMenu']/a"))
        ).click()
        
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "projects"))
        )
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for row in soup.select("div.projects div.row"):
            baslik = row.find("strong").text.strip() if row.find("strong") else ""
            yil = row.find("span", {"class": "label label-info"}).text.strip() if row.find("span", {"class": "label label-info"}) else ""
            
            if baslik:  # Sadece geçerli verileri ekle
                kitaplar.append({
                    "kitap_adi": baslik,
                    "basim_yili": yil
                })
                
    except Exception as e:
        print(f"Kitap çekme hatası: {str(e)}")
    finally:
        browser.back()
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, "//h6")))
    return kitaplar

def tez_cek():
    tezler = []
    try:
        WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@id='thesisMenu']/a"))
        ).click()
        
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, "//table[contains(., 'Tez Adı')]"))
        )
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        tablo = soup.find("table")
        
        if tablo and tablo.find("tbody"):
            for satir in tablo.find("tbody").find_all("tr"):
                hucreler = satir.find_all("td")
                if len(hucreler) >= 4:
                    tezler.append({
                        "universite": hucreler[3].text.strip(),
                        "yil": hucreler[0].text.strip(),
                        "hazirlayan": hucreler[1].text.strip(),
                        "tez_adi": hucreler[2].text.strip()
                    })
                    
    except Exception as e:
        print(f"Tez çekme hatası: {str(e)}")
    finally:
        browser.back()
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, "//h6")))
    return tezler

try:
    while True:
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'AkademisyenGorevOgrenimBilgileri')]"))
        )
        
        # Sayfadaki tüm akademisyen linklerini bul
        akademisyenler = browser.find_elements(By.XPATH, "//a[contains(@href, 'AkademisyenGorevOgrenimBilgileri')]")
        for link in akademisyenler:
            try:
                # Yeni sekmede aç
                link_url = link.get_attribute("href")
                browser.execute_script("window.open('');")
                browser.switch_to.window(browser.window_handles[1])
                browser.get(link_url)
                
                # Temel bilgiler
                WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, "//h6")))
                soup = BeautifulSoup(browser.page_source, "html.parser")
                
                unvan = soup.find("h6").text.strip()
                ad_soyad = soup.find("h4").text.strip()
                bolum = soup.find("span", {"class": "label label-primary"}).text.strip()
                
                # Veri toplama
                veri = {
                    "unvan": unvan,
                    "ad_soyad": ad_soyad,
                    "bolum": bolum,
                    "kitaplar": kitap_cek(),
                    "tezler": tez_cek()
                }
                
                personel_listesi.append(veri)
                print(f"Kaydedildi: {ad_soyad}")
                
                # Sekmeyi kapat
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                
            except Exception as e:
                print(f"Akademisyen işleme hatası: {str(e)}")
                if "no such window" in str(e).lower():
                    browser.quit()
                    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                    browser.get(base_url)

        # Sonraki sayfa
        try:
            sonraki_sayfa = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "»"))
            )
            sonraki_sayfa.click()
        except:
            print("Tüm sayfalar tamamlandı!")
            break

except Exception as e:
    print(f"Beklenmeyen hata: {str(e)}")
finally:
    # Verileri kaydet
    with open("akademik_veriler.json", "w", encoding="utf-8") as f:
        json.dump(personel_listesi, f, ensure_ascii=False, indent=4)
    
    browser.quit()
    print("İşlem tamamlandı! Veriler 'akademik_veriler.json' dosyasına kaydedildi.")