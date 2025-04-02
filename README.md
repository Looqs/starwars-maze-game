# Star Wars Labirent Oyunu

Bu proje, nesne yönelimli programlama (OOP) ve veri yapıları konseptlerini uygulayan bir labirent oyunudur.

## Oyun Hakkında

Oyunda, seçtiğiniz iyi karakter (Luke Skywalker veya Master Yoda) ile labirentte ilerleyerek hedefe ulaşmaya çalışırsınız. Bu sırada kötü karakterlerden (Darth Vader, Kylo Ren ve Stormtrooper) kaçmanız gerekir.

### Karakterler

#### İyi Karakterler
- **Luke Skywalker**: 3 canı vardır
- **Master Yoda**: Yakalandığında canının sadece yarısını kaybeder (6 kez yakalanabilir)

#### Kötü Karakterler
- **Darth Vader**: Duvarları yok sayarak hareket edebilir
- **Kylo Ren**: Her hamlede iki birim ilerleyebilir
- **Stormtrooper**: Normal hareket eder

## Kurulum

1. Python 3.8 veya üstü bir sürüm gereklidir
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

## Oyunu Çalıştırma

```bash
python oyun.py
```

## Kontroller

- Ok tuşları ile karakterinizi yönlendirin
- ESC tuşu ile oyundan çıkın
- Karakter seçim ekranında:
  - 1: Luke Skywalker
  - 2: Master Yoda

## Harita Düzeni

Harita.txt dosyasında:
- 0: Duvar
- 1: Boş alan
- A,B,C,D: Kötü karakter giriş kapıları
- S: İyi karakter doğma noktası

## Oyun Kuralları

1. Oyuncu başlangıçta bir karakter seçer
2. Seçilen karakter klavye ile yönlendirilir
3. Kötü karakterler en kısa yol algoritmaları kullanarak oyuncuyu takip eder
4. Yakalanma durumunda:
   - Luke Skywalker: 1 can kaybeder
   - Master Yoda: Canının yarısını kaybeder
5. Canı tükenen karakter için oyun biter 
