import pygame
import sys
from lokasyon import Lokasyon
from iyi_karakterler import LukeSkywalker, MasterYoda
from kotu_karakterler import DarthVader, KyloRen, Stormtrooper

# Pygame başlatma
pygame.init()
pygame.mixer.init()  # Ses modülünü başlat

# Ekran bilgilerini al
info = pygame.display.Info()
ekran_genislik = info.current_w
ekran_yukseklik = info.current_h

# Sabitler
KARE_BOYUTU = 40
IZGARA_BOYUTU = 14  # Harita genişliği için güncellendi
KENAR_BOSLUK = 50

# Oyun penceresini ekranın yarısı boyutunda ayarla
oyun_genislik_min = IZGARA_BOYUTU * KARE_BOYUTU + 2 * KENAR_BOSLUK + 100
oyun_yukseklik_min = IZGARA_BOYUTU * KARE_BOYUTU + 2 * KENAR_BOSLUK + 50

# Ekranın yarısı boyutunu hesapla
hedef_genislik = ekran_genislik // 2
hedef_yukseklik = ekran_yukseklik // 2

# Minimum gerekli boyutlarla karşılaştır ve daha büyük olanı seç
PENCERE_GENISLIK = max(oyun_genislik_min, hedef_genislik)
PENCERE_YUKSEKLIK = max(oyun_yukseklik_min, hedef_yukseklik)

FPS = 60

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
SARI = (255, 255, 0)
MAVI = (0, 0, 255)
KIRMIZI = (255, 0, 0)
KOYU_KIRMIZI = (180, 0, 0)
PARLAK_KIRMIZI = (255, 40, 40)  # Daha parlak kırmızı (kalpler için)
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
        
        # Müzik dosyalarını yükle
        try:
            self.main_theme = pygame.mixer.Sound("assets\\sounds\\main_theme.mp3")
            self.win_muzik = pygame.mixer.Sound("assets\\sounds\\win.mp3")
            self.lose_muzik = pygame.mixer.Sound("assets\\sounds\\lose.mp3")
            self.muzik_yuklendi = True
            # Ana tema müziğini başlat ve sonsuz döngüye al
            self.main_theme.play(-1)  # -1 parametresi sürekli tekrarı sağlar
        except pygame.error as e:
            print(f"Uyarı: Müzik dosyaları yüklenemedi: {e}")
            self.muzik_yuklendi = False
        
        # Karakter ikonlarını yükle
        try:
            self.luke_icon = self.resize_image(pygame.image.load("assets\\images\\luke.png"), KARE_BOYUTU-10, KARE_BOYUTU-10)
            self.yoda_icon = self.resize_image(pygame.image.load("assets\\images\\yoda.png"), KARE_BOYUTU-10, KARE_BOYUTU-10)
            self.stormtrooper_icon = self.resize_image(pygame.image.load("assets\\images\\stormtrooper.png"), KARE_BOYUTU-10, KARE_BOYUTU-10)
            self.kylo_icon = self.resize_image(pygame.image.load("assets\\images\\kylo.png"), KARE_BOYUTU-10, KARE_BOYUTU-10)
            self.vader_icon = self.resize_image(pygame.image.load("assets\\images\\vader.png"), KARE_BOYUTU-10, KARE_BOYUTU-10)
            self.iconlar_yuklendi = True
            
            # Kalp resimlerini yükle
            self.tam_kalp_icon = self.resize_image(pygame.image.load("assets\\images\\heart.png"), 25, 25)
            self.yarim_kalp_icon = self.resize_image(pygame.image.load("assets\\images\\half_heart.PNG"), 25, 25)
            self.kalpler_yuklendi = True
        except pygame.error as e:
            print(f"Uyarı: İkonlar yüklenemedi: {e}")
            print("Uyarı: Karakter ikonları yüklenemedi, harf gösterimi kullanılacak")
            self.iconlar_yuklendi = False
            self.kalpler_yuklendi = False
        
        # Kalp resmi boyutları
        self.kalp_genislik = 25
        self.kalp_yukseklik = 25
        
        # Kupa resmi
        self.kupa_resmi = pygame.Surface((KARE_BOYUTU-10, KARE_BOYUTU-10))
        self.kupa_resmi.fill(ALTIN)
        
        # Haritayı yükle
        self.harita = self.harita_yukle("harita.txt")
        
        # Orijinal haritanın bir kopyasını sakla (Darth Vader duvarları yıktığında geri döndürmek için)
        self.orijinal_harita = [satir[:] for satir in self.harita]  # Derin kopya
    
    def resize_image(self, image, width, height):
        """Resmi belirtilen boyuta yeniden boyutlandırır"""
        return pygame.transform.scale(image, (width, height))
    
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
        
        self.ekran.blit(baslik, (PENCERE_GENISLIK//2 - baslik.get_width()//2, 100))
        
        # Luke seçim alanı
        luke_rect = pygame.Rect(PENCERE_GENISLIK//2 - 150, 200, 300, 100)
        pygame.draw.rect(self.ekran, SARI, luke_rect, 2)
        self.ekran.blit(luke, (luke_rect.centerx - luke.get_width()//2, luke_rect.y + 10))
        
        # Luke ikonunu göster
        luke_icon_rect = self.luke_icon.get_rect(center=(luke_rect.centerx, luke_rect.y + 60))
        self.ekran.blit(self.luke_icon, luke_icon_rect)
        
        # Yoda seçim alanı
        yoda_rect = pygame.Rect(PENCERE_GENISLIK//2 - 150, 320, 300, 100)
        pygame.draw.rect(self.ekran, SARI, yoda_rect, 2)
        self.ekran.blit(yoda, (yoda_rect.centerx - yoda.get_width()//2, yoda_rect.y + 10))
        
        # Yoda ikonunu göster
        yoda_icon_rect = self.yoda_icon.get_rect(center=(yoda_rect.centerx, yoda_rect.y + 60))
        self.ekran.blit(self.yoda_icon, yoda_icon_rect)
        
        pygame.display.flip()
    
    def kotu_karakter_sec_ekrani(self):
        """Kötü karakter seçim ekranını gösterir"""
        self.ekran.fill(SIYAH)
        font = pygame.font.Font(None, 36)
        
        baslik = font.render("Düşmanınızı Seçin", True, BEYAZ)
        self.ekran.blit(baslik, (PENCERE_GENISLIK//2 - baslik.get_width()//2, 100))
        
        # Stormtrooper seçim alanı
        st_rect = pygame.Rect(PENCERE_GENISLIK//2 - 300, 200, 140, 160)
        pygame.draw.rect(self.ekran, KIRMIZI, st_rect, 2)
        st_text = font.render("1 - Stormtrooper", True, BEYAZ)
        self.ekran.blit(st_text, (st_rect.centerx - st_text.get_width()//2, st_rect.y + 10))
        st_icon_rect = self.stormtrooper_icon.get_rect(center=(st_rect.centerx, st_rect.y + 90))
        self.ekran.blit(self.stormtrooper_icon, st_icon_rect)
        
        # Kylo Ren seçim alanı
        kr_rect = pygame.Rect(PENCERE_GENISLIK//2 - 140, 200, 140, 160)
        pygame.draw.rect(self.ekran, KIRMIZI, kr_rect, 2)
        kr_text = font.render("2 - Kylo Ren", True, BEYAZ)
        self.ekran.blit(kr_text, (kr_rect.centerx - kr_text.get_width()//2, kr_rect.y + 10))
        kr_icon_rect = self.kylo_icon.get_rect(center=(kr_rect.centerx, kr_rect.y + 90))
        self.ekran.blit(self.kylo_icon, kr_icon_rect)
        
        # Darth Vader seçim alanı
        dv_rect = pygame.Rect(PENCERE_GENISLIK//2 + 20, 200, 140, 160)
        pygame.draw.rect(self.ekran, KIRMIZI, dv_rect, 2)
        dv_text = font.render("3 - Darth Vader", True, BEYAZ)
        self.ekran.blit(dv_text, (dv_rect.centerx - dv_text.get_width()//2, dv_rect.y + 10))
        dv_icon_rect = self.vader_icon.get_rect(center=(dv_rect.centerx, dv_rect.y + 90))
        self.ekran.blit(self.vader_icon, dv_icon_rect)
        
        # Hepsi seçim alanı
        all_rect = pygame.Rect(PENCERE_GENISLIK//2 + 180, 200, 140, 160)
        pygame.draw.rect(self.ekran, KIRMIZI, all_rect, 2)
        all_text = font.render("4 - Hepsi", True, BEYAZ)
        self.ekran.blit(all_text, (all_rect.centerx - all_text.get_width()//2, all_rect.y + 10))
        
        # Tüm ikonları küçük halde göster
        self.ekran.blit(pygame.transform.scale(self.stormtrooper_icon, (30, 30)), 
                       (all_rect.centerx - 45, all_rect.y + 90))
        self.ekran.blit(pygame.transform.scale(self.kylo_icon, (30, 30)), 
                       (all_rect.centerx, all_rect.y + 90))
        self.ekran.blit(pygame.transform.scale(self.vader_icon, (30, 30)), 
                       (all_rect.centerx + 45, all_rect.y + 90))
        
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
        # Darth Vader'ın yıktığı duvarları geri yükle
        self.harita = [satir[:] for satir in self.orijinal_harita]  # Derin kopya
        
        spawn_konum = self.spawn_konumu_bul()
        # Karakteri yeniden oluştur
        if self.secilen_karakter == "Luke":
            self.iyi_karakter = LukeSkywalker(spawn_konum)  # S noktasından başla
        else:  # Yoda
            self.iyi_karakter = MasterYoda(spawn_konum)  # S noktasından başla
        
        # Seçilen kötü karakteri yeniden oluştur
        self.kotu_karakterleri_olustur()
    
    def kalp_ciz(self, ekran, x, y, genislik, yukseklik, dolgu=1.0):
        """Kalp şekli çizer
        
        Args:
            ekran: Çizim yapılacak yüzey
            x, y: Kalbin sol üst köşesinin koordinatları
            genislik, yukseklik: Kalbin boyutları
            dolgu: 0.0-1.0 arası doldurma oranı (0: boş, 0.5: yarım, 1.0: tam dolu)
        """
        # Kalp daireleri için boyutlar
        yaricap = min(genislik, yukseklik) / 3
        
        # Dairelerin merkezleri
        sol_merkez_x = x + genislik * 0.33
        sag_merkez_x = x + genislik * 0.67
        daire_merkez_y = y + yukseklik * 0.33
        
        # Kalp şeklinin alt kısmı için noktalar
        alt_x1 = x + genislik * 0.1
        alt_y1 = y + yukseklik * 0.4
        alt_x2 = x + genislik * 0.5
        alt_y2 = y + yukseklik * 0.95
        alt_x3 = x + genislik * 0.9
        alt_y3 = y + yukseklik * 0.4
        
        # Kalp renklerini ayarla - daha doygun ve parlak
        parlak_renk = PARLAK_KIRMIZI
        cerceve_renk = KOYU_KIRMIZI
        
        # Daireleri çiz
        pygame.draw.circle(ekran, parlak_renk, (int(sol_merkez_x), int(daire_merkez_y)), int(yaricap))
        pygame.draw.circle(ekran, parlak_renk, (int(sag_merkez_x), int(daire_merkez_y)), int(yaricap))
        
        # Alt kısmı için üçgen çiz 
        points = [
            (int(sol_merkez_x - yaricap/2), int(daire_merkez_y + yaricap/3)),
            (int(alt_x2), int(alt_y2)),
            (int(sag_merkez_x + yaricap/2), int(daire_merkez_y + yaricap/3))
        ]
        pygame.draw.polygon(ekran, parlak_renk, points)
        
        # Eğer yarım kalp ise (dolgu < 1.0), üst kısmı beyaz ile kapat
        if dolgu < 1.0:
            # Dolgu seviyesini hesapla
            dolgu_y = y + (1.0 - dolgu) * yukseklik
            
            # Dolgu seviyesinin üstünü beyaz ile kapla
            if dolgu_y < daire_merkez_y:
                # Üst kısım - dairelerin üstünü kapla
                kaplama_dikdortgen = pygame.Rect(x, y, genislik, dolgu_y - y)
                ekran_kopyasi = ekran.copy()
                pygame.draw.rect(ekran, BEYAZ, kaplama_dikdortgen)
                # Orijinal kalp şeklinin sınırlarını yeniden çiz
                pygame.draw.circle(ekran, cerceve_renk, (int(sol_merkez_x), int(daire_merkez_y)), int(yaricap), 1)
                pygame.draw.circle(ekran, cerceve_renk, (int(sag_merkez_x), int(daire_merkez_y)), int(yaricap), 1)
            else:
                # Alt kısım - üçgenin üst kısmını kapla
                # Beyaz kaplamanın alt noktaları
                beyaz_alt_sol = (int(sol_merkez_x - yaricap/2), int(daire_merkez_y + yaricap/3))
                beyaz_alt_orta = (int(alt_x2), int(dolgu_y))
                beyaz_alt_sag = (int(sag_merkez_x + yaricap/2), int(daire_merkez_y + yaricap/3))
                
                # Beyaz üçgensel kaplamayı çiz
                beyaz_noktalar = [
                    beyaz_alt_sol,
                    (int(sol_merkez_x - yaricap/2), y),
                    (int(sag_merkez_x + yaricap/2), y),
                    beyaz_alt_sag
                ]
                pygame.draw.polygon(ekran, BEYAZ, beyaz_noktalar)
                
                # Kalp çerçevesini yeniden çiz
                pygame.draw.circle(ekran, cerceve_renk, (int(sol_merkez_x), int(daire_merkez_y)), int(yaricap), 1)
                pygame.draw.circle(ekran, cerceve_renk, (int(sag_merkez_x), int(daire_merkez_y)), int(yaricap), 1)
                pygame.draw.line(ekran, cerceve_renk, beyaz_alt_sol, beyaz_alt_sag, 1)
        
        # Kalp çerçevesini çiz
        pygame.draw.circle(ekran, cerceve_renk, (int(sol_merkez_x), int(daire_merkez_y)), int(yaricap), 1)
        pygame.draw.circle(ekran, cerceve_renk, (int(sag_merkez_x), int(daire_merkez_y)), int(yaricap), 1)
        pygame.draw.line(ekran, cerceve_renk, 
                        (int(sol_merkez_x - yaricap/2), int(daire_merkez_y + yaricap/3)),
                        (int(alt_x2), int(alt_y2)), 1)
        pygame.draw.line(ekran, cerceve_renk, 
                        (int(alt_x2), int(alt_y2)),
                        (int(sag_merkez_x + yaricap/2), int(daire_merkez_y + yaricap/3)), 1)

    def can_goster(self):
        """Canları kalp şeklinde gösterir"""
        font = pygame.font.Font(None, 36)
        can_text = font.render("Canlar:", True, SIYAH)
        self.ekran.blit(can_text, (20, 20))
        
        x_baslangic = 120
        y_baslangic = 15
        
        if self.kalpler_yuklendi:
            # PNG kalp resimleri kullanarak canları göster
            if isinstance(self.iyi_karakter, LukeSkywalker):
                # Luke için tam kalpler
                for i in range(self.iyi_karakter.getCan()):
                    self.ekran.blit(self.tam_kalp_icon, (x_baslangic + i * 30, y_baslangic))
            else:  # Master Yoda
                can = self.iyi_karakter.getCan()
                tam_can = int(can)  # Tam kalp sayısı
                yarim_can = can % 1  # Kalan can (0.5)
                
                # Tam kalpler
                for i in range(tam_can):
                    self.ekran.blit(self.tam_kalp_icon, (x_baslangic + i * 30, y_baslangic))
                
                # Yarım kalp (eğer varsa)
                if yarim_can > 0:
                    self.ekran.blit(self.yarim_kalp_icon, (x_baslangic + tam_can * 30, y_baslangic))
        else:
            # PNG yüklenemediyse çizim fonksiyonu kullan
            if isinstance(self.iyi_karakter, LukeSkywalker):
                # Luke için tam kalpler
                for i in range(self.iyi_karakter.getCan()):
                    self.kalp_ciz(self.ekran, x_baslangic + i * 30, y_baslangic, 
                                self.kalp_genislik, self.kalp_yukseklik, 1.0)
            else:  # Master Yoda
                can = self.iyi_karakter.getCan()
                tam_can = int(can)  # Tam kalp sayısı
                yarim_can = can % 1  # Kalan can (0.5)
                
                # Tam kalpler
                for i in range(tam_can):
                    self.kalp_ciz(self.ekran, x_baslangic + i * 30, y_baslangic, 
                                self.kalp_genislik, self.kalp_yukseklik, 1.0)
                
                # Yarım kalp (eğer varsa)
                if yarim_can > 0:
                    self.kalp_ciz(self.ekran, x_baslangic + tam_can * 30, y_baslangic, 
                                self.kalp_genislik, self.kalp_yukseklik, 0.5)
    
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
        
        # Harita boyutlarını hesapla
        harita_genislik = len(self.harita[0]) * KARE_BOYUTU
        harita_yukseklik = len(self.harita) * KARE_BOYUTU
        
        # Labirenti merkeze konumlandırmak için offset hesapla
        x_offset = (PENCERE_GENISLIK - harita_genislik) // 2
        y_offset = (PENCERE_YUKSEKLIK - harita_yukseklik) // 2 + 25  # Üst kısımda can bilgisi için biraz daha yer bırak
        
        # Haritayı çiz
        for y in range(len(self.harita)):
            for x in range(len(self.harita[0])):
                rect = pygame.Rect(
                    x_offset + x * KARE_BOYUTU, 
                    y_offset + y * KARE_BOYUTU,
                    KARE_BOYUTU, 
                    KARE_BOYUTU
                )
                
                # Izgara çizgilerini çiz
                pygame.draw.rect(self.ekran, ACIK_GRI, rect, 1)
                
                # Harita elemanlarını çiz
                if self.harita[y][x] == '0':  # Duvar
                    pygame.draw.rect(self.ekran, BEYAZ, rect)
                    pygame.draw.rect(self.ekran, SIYAH, rect, 1)  # Çerçeve kalınlığını 1 piksel yaptım
                    font = pygame.font.Font(None, 24)
                    text = font.render('0', True, SIYAH)
                    text_rect = text.get_rect(center=rect.center)
                    self.ekran.blit(text, text_rect)
                elif x == 13 and y == 9:  # Kupa
                    kupa_rect = self.kupa_resmi.get_rect(center=rect.center)
                    self.ekran.blit(self.kupa_resmi, kupa_rect)
                elif self.harita[y][x] in ['A', 'B', 'C', 'D', 'E']:  # Kapılar
                    pygame.draw.rect(self.ekran, MAVI, rect)
                    # Kapı harfi
                    font = pygame.font.Font(None, 36)
                    text = font.render(self.harita[y][x], True, BEYAZ)
                    text_rect = text.get_rect(center=rect.center)
                    self.ekran.blit(text, text_rect)
                    
                    # Kapı pozisyonuna göre okun yönünü ve konumunu ayarla
                    ok_uzunluk = 15
                    ok_genislik = 8
                    
                    # Harita kenarındaysa, ok dışarı doğru çizilsin
                    if x == 0:  # Sol kenar
                        merkez_x = rect.left - 15
                        merkez_y = rect.centery
                        # Sağa ok (sola doğru dışarıda ama sağa bakan ok)
                        pygame.draw.polygon(self.ekran, BEYAZ, [
                            (merkez_x - ok_uzunluk/2, merkez_y - ok_genislik),
                            (merkez_x - ok_uzunluk/2, merkez_y + ok_genislik),
                            (merkez_x + ok_uzunluk/2, merkez_y)
                        ])
                    elif x == len(self.harita[0]) - 1:  # Sağ kenar
                        merkez_x = rect.right + 15
                        merkez_y = rect.centery
                        # Sola ok (sağa doğru dışarıda ama sola bakan ok)
                        pygame.draw.polygon(self.ekran, BEYAZ, [
                            (merkez_x + ok_uzunluk/2, merkez_y - ok_genislik),
                            (merkez_x + ok_uzunluk/2, merkez_y + ok_genislik),
                            (merkez_x - ok_uzunluk/2, merkez_y)
                        ])
                    elif y == 0:  # Üst kenar
                        merkez_x = rect.centerx
                        merkez_y = rect.top - 15
                        # Aşağı ok (yukarı doğru dışarıda ama aşağı bakan ok)
                        pygame.draw.polygon(self.ekran, BEYAZ, [
                            (merkez_x - ok_genislik, merkez_y - ok_uzunluk/2),
                            (merkez_x + ok_genislik, merkez_y - ok_uzunluk/2),
                            (merkez_x, merkez_y + ok_uzunluk/2)
                        ])
                    elif y == len(self.harita) - 1:  # Alt kenar
                        merkez_x = rect.centerx
                        merkez_y = rect.bottom + 15
                        # Yukarı ok (aşağı doğru dışarıda ama yukarı bakan ok)
                        pygame.draw.polygon(self.ekran, BEYAZ, [
                            (merkez_x - ok_genislik, merkez_y + ok_uzunluk/2),
                            (merkez_x + ok_genislik, merkez_y + ok_uzunluk/2),
                            (merkez_x, merkez_y - ok_uzunluk/2)
                        ])
                    else:  # Harita kenarında değilse, kapının dışında ok göster
                        # Yan duvarları kontrol et
                        sol_duvar = x > 0 and self.harita[y][x-1] == '0'
                        sag_duvar = x < len(self.harita[0])-1 and self.harita[y][x+1] == '0'
                        ust_duvar = y > 0 and self.harita[y-1][x] == '0'
                        alt_duvar = y < len(self.harita)-1 and self.harita[y+1][x] == '0'
                        
                        # Duvarların olmadığı yöne ok göster
                        if not sol_duvar:  # Sol tarafta duvar yoksa
                            merkez_x = rect.left - 15
                            merkez_y = rect.centery
                            # Sağa ok (sola doğru dışarıda ama sağa bakan ok)
                            pygame.draw.polygon(self.ekran, BEYAZ, [
                                (merkez_x - ok_uzunluk/2, merkez_y - ok_genislik),
                                (merkez_x - ok_uzunluk/2, merkez_y + ok_genislik),
                                (merkez_x + ok_uzunluk/2, merkez_y)
                            ])
                        elif not sag_duvar:  # Sağ tarafta duvar yoksa
                            merkez_x = rect.right + 15
                            merkez_y = rect.centery
                            # Sola ok (sağa doğru dışarıda ama sola bakan ok)
                            pygame.draw.polygon(self.ekran, BEYAZ, [
                                (merkez_x + ok_uzunluk/2, merkez_y - ok_genislik),
                                (merkez_x + ok_uzunluk/2, merkez_y + ok_genislik),
                                (merkez_x - ok_uzunluk/2, merkez_y)
                            ])
                        elif not ust_duvar:  # Üst tarafta duvar yoksa
                            merkez_x = rect.centerx
                            merkez_y = rect.top - 15
                            # Aşağı ok (yukarı doğru dışarıda ama aşağı bakan ok)
                            pygame.draw.polygon(self.ekran, BEYAZ, [
                                (merkez_x - ok_genislik, merkez_y - ok_uzunluk/2),
                                (merkez_x + ok_genislik, merkez_y - ok_uzunluk/2),
                                (merkez_x, merkez_y + ok_uzunluk/2)
                            ])
                        elif not alt_duvar:  # Alt tarafta duvar yoksa
                            merkez_x = rect.centerx
                            merkez_y = rect.bottom + 15
                            # Yukarı ok (aşağı doğru dışarıda ama yukarı bakan ok)
                            pygame.draw.polygon(self.ekran, BEYAZ, [
                                (merkez_x - ok_genislik, merkez_y + ok_uzunluk/2),
                                (merkez_x + ok_genislik, merkez_y + ok_uzunluk/2),
                                (merkez_x, merkez_y - ok_uzunluk/2)
                            ])
                        else:  # Tüm yönlerde duvar varsa, kapının içine ok koy
                            merkez_x = rect.centerx
                            merkez_y = rect.centery
                            # Yukarı ok (kapının içinde)
                            pygame.draw.polygon(self.ekran, BEYAZ, [
                                (merkez_x - ok_genislik, merkez_y + ok_uzunluk/2),
                                (merkez_x + ok_genislik, merkez_y + ok_uzunluk/2),
                                (merkez_x, merkez_y - ok_uzunluk/2)
                            ])
                
                # Sayıları göster (1'ler için)
                if self.harita[y][x] == '1':
                    font = pygame.font.Font(None, 24)
                    text = font.render('1', True, SIYAH)
                    text_rect = text.get_rect(center=rect.center)
                    self.ekran.blit(text, text_rect)
                
                # Spawn noktasını (S) göster
                elif self.harita[y][x] == 'S':
                    font = pygame.font.Font(None, 24)
                    text = font.render('1', True, SIYAH)  # S noktasındaki 1 yazısı
                    text_rect = text.get_rect(center=rect.center)
                    self.ekran.blit(text, text_rect)
        
        # İyi karakteri çiz
        if self.iyi_karakter:
            iyi_x = x_offset + self.iyi_karakter.getKonum().getX() * KARE_BOYUTU
            iyi_y = y_offset + self.iyi_karakter.getKonum().getY() * KARE_BOYUTU
            iyi_rect = pygame.Rect(iyi_x, iyi_y, KARE_BOYUTU, KARE_BOYUTU)
            
            # Karakterin arkaplanını çiz
            pygame.draw.rect(self.ekran, SARI, iyi_rect)
            
            # Karakterin ikonunu çiz (eğer yüklendiyse)
            if self.iconlar_yuklendi:
                if isinstance(self.iyi_karakter, LukeSkywalker):
                    icon_rect = self.luke_icon.get_rect(center=iyi_rect.center)
                    self.ekran.blit(self.luke_icon, icon_rect)
                else:  # Master Yoda
                    icon_rect = self.yoda_icon.get_rect(center=iyi_rect.center)
                    self.ekran.blit(self.yoda_icon, icon_rect)
            else:
                # İkonlar yüklenemezse harfleri göster
                font = pygame.font.Font(None, 36)
                text = font.render('L' if isinstance(self.iyi_karakter, LukeSkywalker) else 'Y', True, SIYAH)
                text_rect = text.get_rect(center=iyi_rect.center)
                self.ekran.blit(text, text_rect)
        
        # Kötü karakterleri çiz
        for karakter in self.kotu_karakterler:
            kotu_x = x_offset + karakter.getKonum().getX() * KARE_BOYUTU
            kotu_y = y_offset + karakter.getKonum().getY() * KARE_BOYUTU
            kotu_rect = pygame.Rect(kotu_x, kotu_y, KARE_BOYUTU, KARE_BOYUTU)
            
            # Karakterin arkaplanını çiz
            pygame.draw.rect(self.ekran, KIRMIZI, kotu_rect)
            
            # Karakter tipine göre ikon seç ve çiz
            if self.iconlar_yuklendi:
                if isinstance(karakter, Stormtrooper):
                    icon_rect = self.stormtrooper_icon.get_rect(center=kotu_rect.center)
                    self.ekran.blit(self.stormtrooper_icon, icon_rect)
                elif isinstance(karakter, KyloRen):
                    icon_rect = self.kylo_icon.get_rect(center=kotu_rect.center)
                    self.ekran.blit(self.kylo_icon, icon_rect)
                else:  # Darth Vader
                    icon_rect = self.vader_icon.get_rect(center=kotu_rect.center)
                    self.ekran.blit(self.vader_icon, icon_rect)
            else:
                # İkonlar yüklenemezse harfleri göster
                font = pygame.font.Font(None, 36)
                harf = 'S' if isinstance(karakter, Stormtrooper) else ('K' if isinstance(karakter, KyloRen) else 'D')
                text = font.render(harf, True, SIYAH)
                text_rect = text.get_rect(center=kotu_rect.center)
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
                    baslangic_x = x_offset + baslangic.getX() * KARE_BOYUTU + KARE_BOYUTU // 2
                    baslangic_y = y_offset + baslangic.getY() * KARE_BOYUTU + KARE_BOYUTU // 2
                    bitis_x = x_offset + bitis.getX() * KARE_BOYUTU + KARE_BOYUTU // 2
                    bitis_y = y_offset + bitis.getY() * KARE_BOYUTU + KARE_BOYUTU // 2
                    pygame.draw.line(self.ekran, renk, (baslangic_x, baslangic_y), (bitis_x, bitis_y), 2)
        
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
                    # Oyundan çıkarken tüm müzikleri durdur
                    if hasattr(self, 'muzik_yuklendi') and self.muzik_yuklendi:
                        pygame.mixer.stop()
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
                                # Ana tema müziğini durdur ve kazanma müziğini çal
                                if self.muzik_yuklendi:
                                    self.main_theme.stop()
                                    self.win_muzik.play()
                                continue
                            
                            # Kötü karakterlerin hareketi
                            for karakter in self.kotu_karakterler:
                                yol = karakter.enKisaYol(self.iyi_karakter.getKonum(), self.harita)
                                if yol and len(yol) > 1:  # Yol varsa ve en az 2 nokta içeriyorsa
                                    yeni_konum = yol[1]  # Bir sonraki noktaya hareket et
                                    
                                    # Darth Vader özel hareketi: Duvarları yıkma
                                    if isinstance(karakter, DarthVader):
                                        # Eğer yeni konum bir duvar ise, onu yola dönüştür
                                        if (self.harita[yeni_konum.getY()][yeni_konum.getX()] == '0'):
                                            self.harita[yeni_konum.getY()][yeni_konum.getX()] = '1'
                                            print("Darth Vader duvarı yıktı!")
                                    
                                    karakter.setKonum(yeni_konum)
                                
                                # Çarpışma kontrolü
                                if (self.iyi_karakter.getKonum().getX() == karakter.getKonum().getX() and 
                                    self.iyi_karakter.getKonum().getY() == karakter.getKonum().getY()):
                                    # Karakter yakalandığında canı azalt
                                    if isinstance(self.iyi_karakter, LukeSkywalker):
                                        self.iyi_karakter.setCan(self.iyi_karakter.getCan() - 1)  # Luke 1 can kaybeder
                                    elif isinstance(self.iyi_karakter, MasterYoda):
                                        # Yoda'nın canı her zaman yarım kalpten azalsın
                                        mevcut_can = self.iyi_karakter.getCan()
                                        tam_can = int(mevcut_can)  # Tam can kısmı
                                        kalan_can = mevcut_can % 1  # Yarım can kısmı
                                        
                                        if kalan_can >= 0.5:
                                            # Eğer yarım can varsa, yarım canı azalt
                                            self.iyi_karakter.setCan(tam_can)
                                        else:
                                            # Yarım can yoksa, bir tam canı azalt
                                            self.iyi_karakter.setCan(tam_can - 0.5)
                                    
                                    # Darth Vader'ın yıktığı duvarları geri yükle
                                    self.harita = [satir[:] for satir in self.orijinal_harita]  # Derin kopya
                                    
                                    # Karakteri başlangıç noktasına geri gönder
                                    spawn_konum = self.spawn_konumu_bul()
                                    self.iyi_karakter.setKonum(spawn_konum)  # S noktasından başla
                                    
                                    # Yakalayan kötü karakteri başlangıç noktasına geri gönder
                                    if isinstance(karakter, Stormtrooper):
                                        stormtrooper_konum = self.kapi_konumu_bul('E', self.harita)
                                        if stormtrooper_konum:
                                            karakter.setKonum(stormtrooper_konum)
                                    elif isinstance(karakter, KyloRen):
                                        kylo_konum = self.kapi_konumu_bul('C', self.harita)
                                        if kylo_konum:
                                            karakter.setKonum(kylo_konum)
                                    elif isinstance(karakter, DarthVader):
                                        vader_konum = self.kapi_konumu_bul('B', self.harita)
                                        if vader_konum:
                                            karakter.setKonum(vader_konum)
                                    
                                    # Diğer kötü karakterleri de başlangıç noktalarına geri gönder
                                    for diger_karakter in self.kotu_karakterler:
                                        if diger_karakter != karakter:  # Yakalayan karakter dışındakiler
                                            if isinstance(diger_karakter, Stormtrooper):
                                                stormtrooper_konum = self.kapi_konumu_bul('E', self.harita)
                                                if stormtrooper_konum:
                                                    diger_karakter.setKonum(stormtrooper_konum)
                                            elif isinstance(diger_karakter, KyloRen):
                                                kylo_konum = self.kapi_konumu_bul('C', self.harita)
                                                if kylo_konum:
                                                    diger_karakter.setKonum(kylo_konum)
                                            elif isinstance(diger_karakter, DarthVader):
                                                vader_konum = self.kapi_konumu_bul('B', self.harita)
                                                if vader_konum:
                                                    diger_karakter.setKonum(vader_konum)
                                    
                                    print(f"\n{karakter.getAd()} sizi yakaladı! Başlangıç noktasına geri döndünüz.")
                                    print(f"Kalan canınız: {self.iyi_karakter.getCan()}")
                                    
                                    # Can kontrolü
                                    if (isinstance(self.iyi_karakter, LukeSkywalker) and self.iyi_karakter.getCan() <= 0) or \
                                       (isinstance(self.iyi_karakter, MasterYoda) and self.iyi_karakter.getCan() <= 0.2):
                                        self.oyun_durumu = "kaybetti"
                                        # Ana tema müziğini durdur ve kaybetme müziğini çal
                                        if self.muzik_yuklendi:
                                            self.main_theme.stop()
                                            self.lose_muzik.play()
                                    break
                
                elif self.oyun_durumu in ["kazandi", "kaybetti"]:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        # Haritayı orijinal haline geri döndür
                        self.harita = [satir[:] for satir in self.orijinal_harita]  # Derin kopya
                        
                        self.oyun_durumu = "karakter_sec"
                        self.secilen_karakter = None
                        self.secilen_kotu = None
                        self.iyi_karakter = None
                        self.kotu_karakterler = []
                        # Müzikleri durdur ve ana tema müziğini yeniden başlat
                        if self.muzik_yuklendi:
                            self.win_muzik.stop()
                            self.lose_muzik.stop()
                            self.main_theme.play(-1)
            
            if self.oyun_durumu == "karakter_sec":
                self.karakter_sec_ekrani()
            elif self.oyun_durumu == "kotu_karakter_sec":
                self.kotu_karakter_sec_ekrani()
            elif self.oyun_durumu == "oyunda":
                self.harita_ciz()
            elif self.oyun_durumu == "kazandi":
                # Ana tema müziğini durdur ve kazanma müziğini çal (eğer henüz çalınmadıysa)
                if self.muzik_yuklendi and not pygame.mixer.get_busy():
                    self.main_theme.stop()
                    self.win_muzik.play()
                
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