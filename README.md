# Temizlik Robotu

Bu proje, bir temizlik robotunun otomatik olarak belirli bir haritayı temizlemesini sağlayan bir Python programını içerir. Robot, belirli bir hızda hareket eder ve engelleri algılayarak onları temizler veya geçer.

## Özellikler

- Harita dosyası üzerinden odaları ve engelleri okuma
- Temizlik modunu seçme (süpürme veya silme)
- Hız seviyesini seçme
- Tüm odaları veya belirli odaları temizleme seçeneği
- Temizlik işlemini başlatma ve durdurma
- Temizlik raporunu görüntüleme

Nasıl Kullanılır?
Proje dosyalarını bilgisayarınıza indirin.
Ana dizindeki temizlikrobotu.py dosyasını çalıştırın.
Program başladığında, temizlik işlemi için bir harita dosyası seçmeniz istenecektir.
Harita dosyası seçildikten sonra, istenilen temizlik modu, hız seviyesi ve temizlik tipi seçilir.
"Temizliği Başlat" butonuna tıklanarak temizlik işlemi başlatılır.
İşlem sırasında "Temizliği Durdur" butonu ile temizlik işlemi durdurulabilir.
İşlem tamamlandığında "Raporu Göster" butonuna tıklayarak temizlik raporu görüntülenebilir.
Harita Dosyasına Oda Ekleme
Harita dosyasına oda eklerken şu adımları izleyebilirsiniz:

Her oda için bir satır kullanın.
Her satırda oda adı, x koordinatı, y koordinatı, genişlik, yükseklik ve engel sayısı sırasıyla virgülle ayrılmış olmalıdır.
Engellerin koordinatları, oda içindeki konumları olarak belirtilmelidir.

Örnek:

Oda1,0,0,5,5,2,1,2,3,4

Oda2,5,0,4,4,1,1,1

Oda3,0,5,3,3,0

Oda4,6,6,4,4,2,2,3,3,2

Oda5,0,8,3,3,1,1,1

Oda6,3,3,2,2,0

Oda7,8,8,3,3,0

Oda8,2,7,3,3,1,2,2

Dikkat Edilmesi Gerekenler
Her satırda doğru sayıda ve doğru sırayla bilgilerin olduğundan emin olun.
Engellerin, oda sınırları içinde ve birbirleriyle çakışmadan yerleştirildiğinden emin olun.


## Gereksinimler

- Python 3.x
- tkinter (Python'un bir kütüphanesi, genellikle varsayılan olarak yüklenir)

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasını inceleyin.
