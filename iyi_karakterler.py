from karakter import Karakter
from lokasyon import Lokasyon

class LukeSkywalker(Karakter):
    def __init__(self, konum: Lokasyon):
        super().__init__("Luke Skywalker", "İyi", konum)
        self.can = 3
    
    def getCan(self) -> int:
        return self.can
    
    def setCan(self, yeniCan: int) -> None:
        self.can = yeniCan
    
    def enKisaYol(self, hedef: Lokasyon, harita: list) -> list:
        # Oyuncu kontrolünde olduğu için bu metod kullanılmayacak
        return []

class MasterYoda(Karakter):
    def __init__(self, konum: Lokasyon):
        super().__init__("Master Yoda", "İyi", konum)
        self.can = 3.0  # 3 tam can
    
    def getCan(self) -> float:
        return self.can
    
    def setCan(self, yeniCan: float) -> None:
        self.can = yeniCan
    
    def yakalanma(self) -> None:
        """Yakalandığında yarım can kaybeder"""
        self.can -= 0.5  # Yarım can kaybeder
    
    def enKisaYol(self, hedef: Lokasyon, harita: list) -> list:
        # Oyuncu kontrolünde olduğu için bu metod kullanılmayacak
        return [] 