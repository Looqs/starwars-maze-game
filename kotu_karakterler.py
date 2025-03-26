from karakter import Karakter
from lokasyon import Lokasyon
from collections import deque
import numpy as np

class DarthVader(Karakter):
    def __init__(self, konum: Lokasyon):
        super().__init__("Darth Vader", "Kötü", konum)
    
    def enKisaYol(self, hedef: Lokasyon, harita: list) -> list:
        """Duvarları kırarak en kısa yolu bulur (BFS)"""
        if not hedef:  # Hedef None ise boş liste döndür
            return []
            
        baslangic = self.konum
        if not baslangic:  # Başlangıç konumu None ise boş liste döndür
            return []
            
        satir = len(harita)
        sutun = len(harita[0])
        ziyaret_edildi = set()
        kuyruk = deque([(self.konum, [])])
        
        while kuyruk:
            simdiki, yol = kuyruk.popleft()
            if simdiki.getX() == hedef.getX() and simdiki.getY() == hedef.getY():
                return yol + [simdiki]
            
            for dy, dx in [(0,1), (1,0), (0,-1), (-1,0)]:
                yeniY = simdiki.getY() + dy
                yeniX = simdiki.getX() + dx
                
                # Darth Vader duvarları kırabilir, sadece harita sınırlarını kontrol et
                if (0 <= yeniY < satir and 0 <= yeniX < sutun and 
                    f"{yeniY},{yeniX}" not in ziyaret_edildi):
                    yeni_konum = Lokasyon(yeniX, yeniY)
                    ziyaret_edildi.add(f"{yeniY},{yeniX}")
                    kuyruk.append((yeni_konum, yol + [simdiki]))
        return []

class KyloRen(Karakter):
    def __init__(self, konum: Lokasyon):
        super().__init__("Kylo Ren", "Kötü", konum)
    
    def enKisaYol(self, hedef: Lokasyon, harita: list) -> list:
        """İki birim hareket ederek en kısa yolu bulur (BFS)"""
        if not hedef:  # Hedef None ise boş liste döndür
            return []
            
        baslangic = self.konum
        if not baslangic:  # Başlangıç konumu None ise boş liste döndür
            return []
            
        satir = len(harita)
        sutun = len(harita[0])
        ziyaret_edildi = set()
        kuyruk = deque([(self.konum, [])])
        
        while kuyruk:
            simdiki, yol = kuyruk.popleft()
            if simdiki.getX() == hedef.getX() and simdiki.getY() == hedef.getY():
                return yol + [simdiki]
            
            # Kylo Ren'in hareket seçenekleri (2 birim veya 1 birim)
            hareketler = [(0,2), (2,0), (0,-2), (-2,0), (0,1), (1,0), (0,-1), (-1,0)]
            
            for dy, dx in hareketler:
                yeniY = simdiki.getY() + dy
                yeniX = simdiki.getX() + dx
                
                # Harita sınırları ve duvar kontrolü
                if not (0 <= yeniY < satir and 0 <= yeniX < sutun):
                    continue
                    
                # 2 birimlik hareket için ara noktaları kontrol et
                if abs(dx) == 2 or abs(dy) == 2:
                    araY = simdiki.getY() + dy//2
                    araX = simdiki.getX() + dx//2
                    # Eğer ara nokta duvarsa veya hedef nokta duvarsa, bu yolu kullanma
                    if (harita[araY][araX] == '0' or harita[yeniY][yeniX] == '0'):
                        continue
                else:
                    # 1 birimlik hareket için sadece hedef noktayı kontrol et
                    if harita[yeniY][yeniX] == '0':
                        continue
                
                yeni_konum = Lokasyon(yeniX, yeniY)
                if f"{yeniY},{yeniX}" not in ziyaret_edildi:
                    ziyaret_edildi.add(f"{yeniY},{yeniX}")
                    kuyruk.append((yeni_konum, yol + [simdiki]))
        return []

class Stormtrooper(Karakter):
    def __init__(self, konum: Lokasyon):
        super().__init__("Stormtrooper", "Kötü", konum)
    
    def enKisaYol(self, hedef: Lokasyon, harita: list) -> list:
        """Normal hareket ile en kısa yolu bulur (BFS)"""
        if not hedef:  # Hedef None ise boş liste döndür
            return []
            
        baslangic = self.konum
        if not baslangic:  # Başlangıç konumu None ise boş liste döndür
            return []
            
        satir = len(harita)
        sutun = len(harita[0])
        ziyaret_edildi = set()
        kuyruk = deque([(self.konum, [])])
        
        while kuyruk:
            simdiki, yol = kuyruk.popleft()
            if simdiki.getX() == hedef.getX() and simdiki.getY() == hedef.getY():
                return yol + [simdiki]
            
            for dy, dx in [(0,1), (1,0), (0,-1), (-1,0)]:
                yeniY = simdiki.getY() + dy
                yeniX = simdiki.getX() + dx
                
                if (0 <= yeniY < satir and 0 <= yeniX < sutun and 
                    harita[yeniY][yeniX] != '0' and  # 0'lar duvar
                    f"{yeniY},{yeniX}" not in ziyaret_edildi):
                    yeni_konum = Lokasyon(yeniX, yeniY)
                    ziyaret_edildi.add(f"{yeniY},{yeniX}")
                    kuyruk.append((yeni_konum, yol + [simdiki]))
        return [] 