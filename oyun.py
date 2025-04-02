import pygame
import sys
from lokasyon import Lokasyon
from iyi_karakterler import LukeSkywalker, MasterYoda
from kotu_karakterler import DarthVader, KyloRen, Stormtrooper

# Pygame başlatma
pygame.init()

# Sabitler
KARE_BOYUTU = 40
IZGARA_BOYUTU = 14  # Harita genişliği için güncellendi
KENAR_BOSLUK = 50
PENCERE_GENISLIK = IZGARA_BOYUTU * KARE_BOYUTU + 2 * KENAR_BOSLUK + 100  # Genişlik artırıldı
PENCERE_YUKSEKLIK = IZGARA_BOYUTU * KARE_BOYUTU + 2 * KENAR_BOSLUK + 50
FPS = 60

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
SARI = (255, 255, 0)
MAVI = (0, 0, 255)
KIRMIZI = (255, 0, 0)
ACIK_GRI = (200, 200, 200)
ARKAPLAN = (180, 200, 200)
ALTIN = (255, 215, 0)

class Oyun:
    def __init__(self):
        self.ekran = pygame.display.set_mode((PENCERE_GENISLIK, PENCERE_YUKSEKLIK))
        pygame.display.set_caption("Star Wars Labirent Oyunu")
        self.saat = pygame.time.Clock()
        self.iyi_karakter = None
        self.kotu_karakterler = []
        self.oyun_durumu = "karakter_sec"
        self.secilen_karakter = None
        self.secilen_kotu = None  # Seçilen kötü karakter(ler)
        
        # Kalp resmi
        self.kalp_resmi = pygame.Surface((20, 20))
        self.kalp_resmi.fill(KIRMIZI)
        
        # Yarım kalp resmi
        self.yarim_kalp_resmi = pygame.Surface((10, 20))
        self.yarim_kalp_resmi.fill(KIRMIZI)
        
        # Kupa resmi
        self.kupa_resmi = pygame.Surface((KARE_BOYUTU-10, KARE_BOYUTU-10))
        self.kupa_resmi.fill(ALTIN)
        
        # En kısa yol gösterimi için
        self.en_kisa_yol = []
        
        # Haritayı yükle
        self.harita = self.harita_yukle("harita.txt")
    
    def harita_yukle(self, dosya_adi: str) -> list:
        """Haritayı dosyadan yükler"""
        try:
            with open(dosya_adi, 'r') as f:
                harita_data = []
                
                # Harita verilerini oku
                satir = f.readline().strip()
                while satir and not satir.startswith("KARAKTERLER"):
                    harita_data.append(list(satir))
                    satir = f.readline().strip()
                
                # Haritanın boyutlarını kontrol et
                max_uzunluk = max(len(row) for row in harita_data)
                for i in range(len(harita_data)):
                    # Eksik sütunları 0 ile doldur
                    while len(harita_data[i]) < max_uzunluk:
                        harita_data[i].append('0')
                
                return harita_data
        except FileNotFoundError:
            print(f"Hata: {dosya_adi} dosyası bulunamadı!")
            sys.exit(1)
        except Exception as e:
            print(f"Hata: Harita yüklenirken bir sorun oluştu - {str(e)}")
            sys.exit(1)
    
    def kapi_konumu_bul(self, kapi: str, harita: list) -> Lokasyon:
        """Verilen kapının konumunu haritada bulur"""
        try:
            for y in range(len(harita)):
                for x in range(len(harita[y])):  # Her satırın kendi uzunluğunu kullan
                    if harita[y][x] == kapi:
                        return Lokasyon(x, y)
            return None
        except Exception as e:
            print(f"Hata: Kapı konumu bulunurken bir sorun oluştu - {str(e)}")
            return None

    def spawn_konumu_bul(self) -> Lokasyon:
        """S harfinin konumunu haritada bulur"""
        try:
            for y in range(len(self.harita)):
                for x in range(len(self.harita[y])):
                    if self.harita[y][x] == 'S':
                        return Lokasyon(x, y)
            return Lokasyon(0, 5)  # S bulunamazsa varsayılan konum
        except Exception as e:
            print(f"Hata: Spawn konumu bulunurken bir sorun oluştu - {str(e)}")
            return Lokasyon(0, 5)  # Hata durumunda varsayılan konum

    def karakter_sec_ekrani(self):
        """Karakter seçim ekranını gösterir"""
        self.ekran.fill(SIYAH)
        font = pygame.font.Font(None, 36)
        
        baslik = font.render("Karakterinizi Seçin", True, BEYAZ)
        luke = font.render("1 - Luke Skywalker", True, BEYAZ)
        yoda = font.render("2 - Master Yoda", True, BEYAZ)
        
        self.ekran.blit(baslik, (PENCERE_GENISLIK//2 - baslik.get_width()//2, 200))
        self.ekran.blit(luke, (PENCERE_GENISLIK//2 - luke.get_width()//2, 300))
        self.ekran.blit(yoda, (PENCERE_GENISLIK//2 - yoda.get_width()//2, 350))
        
        pygame.display.flip()
    
    def kotu_karakter_sec_ekrani(self):
        """Kötü karakter seçim ekranını gösterir"""
        self.ekran.fill(SIYAH)
        font = pygame.font.Font(None, 36)
        
        baslik = font.render("Düşmanınızı Seçin", True, BEYAZ)
        stormtrooper = font.render("1 - Stormtrooper", True, BEYAZ)
        kylo = font.render("2 - Kylo Ren", True, BEYAZ)
        vader = font.render("3 - Darth Vader", True, BEYAZ)
        hepsi = font.render("4 - Hepsi", True, BEYAZ)
        
        self.ekran.blit(baslik, (PENCERE_GENISLIK//2 - baslik.get_width()//2, 200))
        self.ekran.blit(stormtrooper, (PENCERE_GENISLIK//2 - stormtrooper.get_width()//2, 300))
        self.ekran.blit(kylo, (PENCERE_GENISLIK//2 - kylo.get_width()//2, 350))
        self.ekran.blit(vader, (PENCERE_GENISLIK//2 - vader.get_width()//2, 400))
        self.ekran.blit(hepsi, (PENCERE_GENISLIK//2 - hepsi.get_width()//2, 450))
        
        pygame.display.flip()

    def kotu_karakterleri_olustur(self):
        """Seçilen kötü karakterleri oluşturur"""
        self.kotu_karakterler = []  # Önceki karakterleri temizle
        
        if self.secilen_kotu == "1":  # Stormtrooper
            konum = self.kapi_konumu_bul('E', self.harita)
            if konum:
                self.kotu_karakterler.append(Stormtrooper(konum))
        elif self.secilen_kotu == "2":  # Kylo Ren
            konum = self.kapi_konumu_bul('C', self.harita)  # C kapısından spawn olacak
            if konum:
                self.kotu_karakterler.append(KyloRen(konum))
        elif self.secilen_kotu == "3":  # Darth Vader
            konum = self.kapi_konumu_bul('B', self.harita)  # B kapısından spawn olacak
            if konum:
                self.kotu_karakterler.append(DarthVader(konum))
        elif self.secilen_kotu == "4":  # Hepsi
            konumE = self.kapi_konumu_bul('E', self.harita)
            konumC = self.kapi_konumu_bul('C', self.harita)  # Kylo Ren için C kapısı
            konumB = self.kapi_konumu_bul('B', self.harita)  # Darth Vader için B kapısı
            
            if konumE:
                self.kotu_karakterler.append(Stormtrooper(konumE))
            if konumC:  # C kapısından Kylo Ren spawn olacak
                self.kotu_karakterler.append(KyloRen(konumC))
            if konumB:  # B kapısından Darth Vader spawn olacak
                self.kotu_karakterler.append(DarthVader(konumB))

    def oyunu_sifirla(self):
        """Oyunu başlangıç durumuna getirir"""
        spawn_konum = self.spawn_konumu_bul()
        # Karakteri yeniden oluştur
        if self.secilen_karakter == "Luke":
            self.iyi_karakter = LukeSkywalker(spawn_konum)  # S noktasından başla
        else:  # Yoda
            self.iyi_karakter = MasterYoda(spawn_konum)  # S noktasından başla
        
        # Seçilen kötü karakteri yeniden oluştur
        self.kotu_karakterleri_olustur()
        
        # En kısa yol listesini temizle
        self.en_kisa_yol = []
    
    def can_goster(self):
        """Canları kalp şeklinde gösterir"""
        font = pygame.font.Font(None, 36)
        can_text = font.render("Canlar:", True, SIYAH)
        self.ekran.blit(can_text, (20, 20))
        
        x_baslangic = 120
        
        if isinstance(self.iyi_karakter, LukeSkywalker):
            # Luke için tam kalpler
            for i in range(self.iyi_karakter.getCan()):
                self.ekran.blit(self.kalp_resmi, (x_baslangic + i * 30, 20))
        else:  # Master Yoda
            can = self.iyi_karakter.getCan()
            tam_can = int(can)  # Tam kalp sayısı
            yarim_can = can % 1 > 0  # Yarım kalp var mı?
            
            # Tam kalpler
            for i in range(tam_can):
                self.ekran.blit(self.kalp_resmi, (x_baslangic + i * 30, 20))
            
            # Yarım kalp
            if yarim_can:
                self.ekran.blit(self.yarim_kalp_resmi, (x_baslangic + tam_can * 30, 20))
    
    def en_kisa_yol_ciz(self):
        """En kısa yolu ekrana çizer"""
        if self.en_kisa_yol:
            for i in range(len(self.en_kisa_yol) - 1):
                baslangic = self.en_kisa_yol[i]
                bitis = self.en_kisa_yol[i + 1]
                
                baslangic_x = KENAR_BOSLUK + baslangic.getX() * KARE_BOYUTU + KARE_BOYUTU//2
                baslangic_y = KENAR_BOSLUK + baslangic.getY() * KARE_BOYUTU + 50 + KARE_BOYUTU//2
                bitis_x = KENAR_BOSLUK + bitis.getX() * KARE_BOYUTU + KARE_BOYUTU//2
                bitis_y = KENAR_BOSLUK + bitis.getY() * KARE_BOYUTU + 50 + KARE_BOYUTU//2
                
                pygame.draw.line(self.ekran, KIRMIZI, (baslangic_x, baslangic_y), 
                               (bitis_x, bitis_y), 2)
    
    def kupa_kontrol(self) -> bool:
        """Oyuncunun kupaya ulaşıp ulaşmadığını kontrol eder"""
        x = self.iyi_karakter.getKonum().getX()
        y = self.iyi_karakter.getKonum().getY()
        return x == 13 and y == 9  # Kupa bir blok sağa kaydırıldı
    
    def harita_ciz(self):
        """Haritayı ekrana çizer"""
        self.ekran.fill(ARKAPLAN)
        
        # Can göstergesi
        if self.iyi_karakter:
            self.can_goster()
        
        # Haritayı çiz
        for y in range(len(self.harita)):
            for x in range(len(self.harita[0])):
                rect = pygame.Rect(
                    KENAR_BOSLUK + x * KARE_BOYUTU, 
                    KENAR_BOSLUK + y * KARE_BOYUTU + 50,
                    KARE_BOYUTU, 
                    KARE_BOYUTU
                )
                
                # Izgara çizgilerini çiz
                pygame.draw.rect(self.ekran, ACIK_GRI, rect, 1)
                
                # Harita elemanlarını çiz
                if self.harita[y][x] == '0':  # Duvar
                    pygame.draw.rect(self.ekran, BEYAZ, rect)
                elif x == 13 and y == 9:  # Kupa
                    kupa_rect = self.kupa_resmi.get_rect(center=rect.center)
                    self.ekran.blit(self.kupa_resmi, kupa_rect)
                elif self.harita[y][x] in ['A', 'B', 'C', 'D', 'E']:  # Kapılar
                    pygame.draw.rect(self.ekran, MAVI, rect)
                    # Mavi ok
                    ok_uzunluk = 20
                    ok_genislik = 10
                    merkez_x = rect.centerx
                    merkez_y = rect.centery
                    pygame.draw.polygon(self.ekran, MAVI, [
                        (merkez_x - ok_genislik, merkez_y - ok_uzunluk/2),
                        (merkez_x + ok_genislik, merkez_y - ok_uzunluk/2),
                        (merkez_x, merkez_y + ok_uzunluk/2)
                    ])
                
                # Sayıları göster
                if self.harita[y][x] in ['0', '1']:
                    font = pygame.font.Font(None, 24)
                    text = font.render(self.harita[y][x], True, SIYAH if self.harita[y][x] == '1' else BEYAZ)
                    text_rect = text.get_rect(center=rect.center)
                    self.ekran.blit(text, text_rect)
        
        # Her kötü karakterin en kısa yolunu çiz
        for karakter in self.kotu_karakterler:
            yol = karakter.enKisaYol(self.iyi_karakter.getKonum(), self.harita)
            if yol:
                # Her karakter için farklı renk kullan
                if isinstance(karakter, Stormtrooper):
                    renk = KIRMIZI
                elif isinstance(karakter, KyloRen):
                    renk = (128, 0, 0)  # Koyu kırmızı
                else:  # Darth Vader
                    renk = (64, 0, 0)   # Daha koyu kırmızı
                
                # Yolu çiz
                for i in range(len(yol) - 1):
                    baslangic = yol[i]
                    bitis = yol[i + 1]
                    baslangic_x = KENAR_BOSLUK + baslangic.getX() * KARE_BOYUTU + KARE_BOYUTU // 2
                    baslangic_y = KENAR_BOSLUK + baslangic.getY() * KARE_BOYUTU + 50 + KARE_BOYUTU // 2
                    bitis_x = KENAR_BOSLUK + bitis.getX() * KARE_BOYUTU + KARE_BOYUTU // 2
                    bitis_y = KENAR_BOSLUK + bitis.getY() * KARE_BOYUTU + 50 + KARE_BOYUTU // 2
                    pygame.draw.line(self.ekran, renk, (baslangic_x, baslangic_y), (bitis_x, bitis_y), 2)
        
        # İyi karakteri çiz
        if self.iyi_karakter:
            iyi_x = KENAR_BOSLUK + self.iyi_karakter.getKonum().getX() * KARE_BOYUTU
            iyi_y = KENAR_BOSLUK + self.iyi_karakter.getKonum().getY() * KARE_BOYUTU + 50
            iyi_rect = pygame.Rect(iyi_x, iyi_y, KARE_BOYUTU, KARE_BOYUTU)
            pygame.draw.rect(self.ekran, SARI, iyi_rect)
            font = pygame.font.Font(None, 36)
            text = font.render('L' if isinstance(self.iyi_karakter, LukeSkywalker) else 'Y', True, SIYAH)
            text_rect = text.get_rect(center=iyi_rect.center)
            self.ekran.blit(text, text_rect)
        
        # Kötü karakterleri çiz
        for karakter in self.kotu_karakterler:
            kotu_x = KENAR_BOSLUK + karakter.getKonum().getX() * KARE_BOYUTU
            kotu_y = KENAR_BOSLUK + karakter.getKonum().getY() * KARE_BOYUTU + 50
            kotu_rect = pygame.Rect(kotu_x, kotu_y, KARE_BOYUTU, KARE_BOYUTU)
            pygame.draw.rect(self.ekran, KIRMIZI, kotu_rect)
            font = pygame.font.Font(None, 36)
            # Karakter tipine göre harf seç
            if isinstance(karakter, Stormtrooper):
                harf = 'S'
            elif isinstance(karakter, KyloRen):
                harf = 'K'
            else:  # Darth Vader
                harf = 'D'
            text = font.render(harf, True, SIYAH)
            text_rect = text.get_rect(center=kotu_rect.center)
            self.ekran.blit(text, text_rect)
        
        pygame.display.flip()
    
    def oyuncu_hareket(self, dx: int, dy: int) -> bool:
        """Oyuncuyu hareket ettirir ve çarpışma kontrolü yapar"""
        yeni_x = self.iyi_karakter.getKonum().getX() + dx
        yeni_y = self.iyi_karakter.getKonum().getY() + dy
        
        # Harita sınırları kontrolü
        if not (0 <= yeni_y < len(self.harita) and 0 <= yeni_x < len(self.harita[0])):
            return False
            
        # Duvar kontrolü - hem Luke hem Yoda için duvarlardan geçememe
        if self.harita[yeni_y][yeni_x] == '0':  # 0'lar duvar
            return False
            
        self.iyi_karakter.setKonum(Lokasyon(yeni_x, yeni_y))
        return True
    
    def oyun_dongusu(self):
        """Ana oyun döngüsü"""
        hareket_sayaci = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.oyun_durumu == "karakter_sec":
                    if event.type == pygame.KEYDOWN:
                        spawn_konum = self.spawn_konumu_bul()
                        if event.key == pygame.K_1:
                            self.secilen_karakter = "Luke"
                            self.iyi_karakter = LukeSkywalker(spawn_konum)
                            self.oyun_durumu = "kotu_karakter_sec"
                        elif event.key == pygame.K_2:
                            self.secilen_karakter = "Yoda"
                            self.iyi_karakter = MasterYoda(spawn_konum)
                            self.oyun_durumu = "kotu_karakter_sec"
                
                elif self.oyun_durumu == "kotu_karakter_sec":
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                            self.secilen_kotu = str(event.key - pygame.K_0)  # Tuş numarasını al
                            self.kotu_karakterleri_olustur()
                            self.oyun_durumu = "oyunda"
                
                elif self.oyun_durumu == "oyunda":
                    if event.type == pygame.KEYDOWN:
                        hareket_yapildi = False
                        if event.key == pygame.K_LEFT:
                            hareket_yapildi = self.oyuncu_hareket(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            hareket_yapildi = self.oyuncu_hareket(1, 0)
                        elif event.key == pygame.K_UP:
                            hareket_yapildi = self.oyuncu_hareket(0, -1)
                        elif event.key == pygame.K_DOWN:
                            hareket_yapildi = self.oyuncu_hareket(0, 1)
                        
                        if hareket_yapildi:
                            # Kupa kontrolü
                            if self.kupa_kontrol():
                                self.oyun_durumu = "kazandi"
                                continue
                            
                            # Kötü karakterlerin hareketi
                            for karakter in self.kotu_karakterler:
                                yol = karakter.enKisaYol(self.iyi_karakter.getKonum(), self.harita)
                                if yol and len(yol) > 1:  # Yol varsa ve en az 2 nokta içeriyorsa
                                    karakter.setKonum(yol[1])  # Bir sonraki noktaya hareket et
                                    if isinstance(karakter, Stormtrooper):
                                        self.en_kisa_yol = yol
                                
                                # Çarpışma kontrolü
                                if (self.iyi_karakter.getKonum().getX() == karakter.getKonum().getX() and 
                                    self.iyi_karakter.getKonum().getY() == karakter.getKonum().getY()):
                                    # Karakter yakalandığında canı azalt
                                    if isinstance(self.iyi_karakter, LukeSkywalker):
                                        self.iyi_karakter.setCan(self.iyi_karakter.getCan() - 1)  # Luke 1 can kaybeder
                                    elif isinstance(self.iyi_karakter, MasterYoda):
                                        self.iyi_karakter.setCan(self.iyi_karakter.getCan() - 0.5)  # Yoda 0.5 can kaybeder
                                    
                                    # Karakteri başlangıç noktasına geri gönder
                                    spawn_konum = self.spawn_konumu_bul()
                                    self.iyi_karakter.setKonum(spawn_konum)  # S noktasından başla
                                    # Kötü karakteri de kendi başlangıç noktasına geri gönder
                                    if isinstance(karakter, Stormtrooper):
                                        karakter.setKonum(self.kapi_konumu_bul('E', self.harita))
                                    elif isinstance(karakter, KyloRen):
                                        karakter.setKonum(self.kapi_konumu_bul('C', self.harita))
                                    elif isinstance(karakter, DarthVader):
                                        karakter.setKonum(self.kapi_konumu_bul('B', self.harita))
                                    
                                    print(f"\n{karakter.getAd()} sizi yakaladı! Başlangıç noktasına geri döndünüz.")
                                    print(f"Kalan canınız: {self.iyi_karakter.getCan()}")
                                    
                                    # Can kontrolü
                                    if (isinstance(self.iyi_karakter, LukeSkywalker) and self.iyi_karakter.getCan() <= 0) or \
                                       (isinstance(self.iyi_karakter, MasterYoda) and self.iyi_karakter.getCan() <= 0.2):
                                        self.oyun_durumu = "kaybetti"
                                    break
                
                elif self.oyun_durumu in ["kazandi", "kaybetti"]:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.oyun_durumu = "karakter_sec"
                        self.secilen_karakter = None
                        self.secilen_kotu = None
                        self.iyi_karakter = None
                        self.kotu_karakterler = []
            
            if self.oyun_durumu == "karakter_sec":
                self.karakter_sec_ekrani()
            elif self.oyun_durumu == "kotu_karakter_sec":
                self.kotu_karakter_sec_ekrani()
            elif self.oyun_durumu == "oyunda":
                self.harita_ciz()
            elif self.oyun_durumu == "kazandi":
                self.ekran.fill(SIYAH)
                font = pygame.font.Font(None, 74)
                text = font.render("Tebrikler! Kazandınız!", True, ALTIN)
                font_kucuk = pygame.font.Font(None, 36)
                text_tekrar = font_kucuk.render("Tekrar oynamak için SPACE tuşuna basın", True, BEYAZ)
                self.ekran.blit(text, (PENCERE_GENISLIK//2 - text.get_width()//2, 
                                     PENCERE_YUKSEKLIK//2 - text.get_height()//2))
                self.ekran.blit(text_tekrar, (PENCERE_GENISLIK//2 - text_tekrar.get_width()//2,
                                            PENCERE_YUKSEKLIK//2 + text.get_height()))
                pygame.display.flip()
            elif self.oyun_durumu == "kaybetti":
                self.ekran.fill(SIYAH)
                font = pygame.font.Font(None, 74)
                text = font.render("Game Over!", True, KIRMIZI)
                font_kucuk = pygame.font.Font(None, 36)
                text_tekrar = font_kucuk.render("Tekrar oynamak için SPACE tuşuna basın", True, BEYAZ)
                self.ekran.blit(text, (PENCERE_GENISLIK//2 - text.get_width()//2, 
                                     PENCERE_YUKSEKLIK//2 - text.get_height()//2))
                self.ekran.blit(text_tekrar, (PENCERE_GENISLIK//2 - text_tekrar.get_width()//2,
                                            PENCERE_YUKSEKLIK//2 + text.get_height()))
                pygame.display.flip()
            
            self.saat.tick(FPS)

if __name__ == "__main__":
    oyun = Oyun()
    oyun.oyun_dongusu() 