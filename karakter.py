from abc import ABC, abstractmethod
from lokasyon import Lokasyon

class Karakter(ABC):
    def __init__(self, ad: str, tur: str, konum: Lokasyon):
        self.ad = ad
        self.tur = tur
        self.konum = konum
    
    def getAd(self) -> str:
        return self.ad
    
    def setAd(self, yeniAd: str) -> None:
        self.ad = yeniAd
    
    def getTur(self) -> str:
        return self.tur
    
    def setTur(self, yeniTur: str) -> None:
        self.tur = yeniTur
    
    def getKonum(self) -> Lokasyon:
        return self.konum
    
    def setKonum(self, yeniKonum: Lokasyon) -> None:
        self.konum = yeniKonum
    
    @abstractmethod
    def enKisaYol(self, hedef: Lokasyon, harita: list) -> list:
        """
        Karakterin hedef konuma ulaşmak için en kısa yolu hesaplar
        
        Args:
            hedef: Hedef konum
            harita: Oyun haritası
            
        Returns:
            En kısa yol koordinatları listesi
        """
        pass 