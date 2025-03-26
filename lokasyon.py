class Lokasyon:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def getX(self) -> int:
        return self.x
    
    def getY(self) -> int:
        return self.y
    
    def setX(self, x: int):
        self.x = x
    
    def setY(self, y: int):
        self.y = y
    
    def __eq__(self, other):
        """Eşitlik karşılaştırması için"""
        if not isinstance(other, Lokasyon):
            return False
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        """Küçüktür karşılaştırması için"""
        if not isinstance(other, Lokasyon):
            return NotImplemented
        # Önce x'e göre, sonra y'ye göre karşılaştır
        return (self.x, self.y) < (other.x, other.y)
    
    def __le__(self, other):
        """Küçük eşittir karşılaştırması için"""
        if not isinstance(other, Lokasyon):
            return NotImplemented
        return (self.x, self.y) <= (other.x, other.y)
    
    def __gt__(self, other):
        """Büyüktür karşılaştırması için"""
        if not isinstance(other, Lokasyon):
            return NotImplemented
        return (self.x, self.y) > (other.x, other.y)
    
    def __ge__(self, other):
        """Büyük eşittir karşılaştırması için"""
        if not isinstance(other, Lokasyon):
            return NotImplemented
        return (self.x, self.y) >= (other.x, other.y)
    
    def __hash__(self):
        """Set ve dictionary'lerde kullanılabilmesi için"""
        return hash((self.x, self.y))
    
    def __str__(self):
        """String gösterimi için"""
        return f"({self.x}, {self.y})" 