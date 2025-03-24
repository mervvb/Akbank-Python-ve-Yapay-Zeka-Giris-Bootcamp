from collections import defaultdict, deque
from heapq import heappop,heappush
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        # TODO: Bu fonksiyonu 
        """
        Bir başlangıç istasyonundan hedef istasyona en az aktarmalı yolu bulmak için 
        Genişlik Öncelikli Arama (BFS) algoritmasını kullanır.

        Parametreler:
            baslangic_id (str): Başlangıç istasyonunun kimliği.
            hedef_id (str): Hedef istasyonun kimliği.

        Dönüş:
            list: Hedefe giden istasyonların sıralı listesi (rota).
            None: Eğer bir rota bulunamazsa None döndürülür.
        """ 
              
        # 1. Başlangıç ve hedef istasyonların varlığını kontrol et
        if baslangic_id not in self.istasyonlar:
            raise ValueError(f"Başlangıç istasyonu bulunamadı: {baslangic_id}")
        if hedef_id not in self.istasyonlar:
            raise ValueError(f"Hedef istasyonu bulunamadı: {hedef_id}")
        
        # Başlangıç ve hedef istasyonlarını al     
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        # 2. BFS için gerekli veri yapılarının oluşturulması
        kuyruk = deque([(baslangic, [baslangic])])  # (mevcut istasyon, o ana kadar izlenen rota)
        ziyaret_edildi = {baslangic}  # Ziyaret edilen istasyonlar kümesi
        
        while kuyruk:
                # Kuyruğun başındaki istasyonu ve mevcut rotayı al
                suanki_istasyon, rota = kuyruk.popleft()
                
                # Hedef istasyona ulaşıldıysa, rotayı döndür
                if suanki_istasyon == hedef:
                    return rota
                
                # Komşu istasyonları dolaş
                for komsu, _ in suanki_istasyon.komsular: # süre değerini kullanmadığımız için "_"
                    if komsu not in ziyaret_edildi:
                # Yeni istasyonu kuyruğa ekle ve ziyaret edildi olarak işaretle
                        kuyruk.append((komsu, rota + [komsu]))
                        ziyaret_edildi.add(komsu)
                    
        # 3. Rota bulunamazsa None döndür
        return None     
        
    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        # TODO: Bu fonksiyonu tamamlayın       
        """
        A* algoritması kullanarak iki istasyon arasındaki en hızlı rotayı bulur.

        Parametreler:
            baslangic_id (str): Başlangıç istasyonunun kimliği.
            hedef_id (str): Hedef istasyonunun kimliği.

        Dönüş:
            Tuple[List, int] veya None: En kısa rota ve toplam süre.
            Eğer bir yol bulunamazsa None döndürülür.
        """
        # 1. Başlangıç ve hedef istasyonların varlığını kontrol et
        if baslangic_id not in self.istasyonlar:
            raise ValueError(f"Başlangıç istasyonu bulunamadı: {baslangic_id}")
        if hedef_id not in self.istasyonlar:
            raise ValueError(f"Hedef istasyonu bulunamadı: {hedef_id}")
        
        # Başlangıç ve hedef istasyonlarını al
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
    
        # 2. A* algoritması için öncelikli kuyruk (heap) oluşturuyoruz
        """
        pq öncelikli kuyruğu (priority queue) saklar ve en düşük toplam süreye sahip istasyonu önce işler.
        İçerik:
        * (toplam_sure, istasyon_id, istasyon, rota)
        ! toplam_sure (int): O ana kadar geçen toplam süre.
        ! id(istasyon) (int): Aynı süreye sahip istasyonları ayırt etmek için kullanılır.
        ! istasyon (obj): Şu an işlenen istasyon.
        ! rota (List): Şu ana kadar izlenen yol.
        """
        pq = [(0, id(baslangic), baslangic, [baslangic])] 
        self.ziyaret_edilen: Set[str] = set() # Ziyaret edilen istasyonlar bir kümede saklanır, böylece her istasyon yalnızca bir kez işlenir.
        
        # 3. Öncelikli kuyruğu işle.
        while pq:
            """
            * heappop() kullanarak en düşük süreye sahip istasyonu al.
            * `_` değişkeni id(istasyon) değeridir ancak kullanılmadığı için `_` ile temsil edilmiştir.
            """                                                         
            toplam_sure, _, istasyon, rota = heappop(pq)
              
            # Eğer bu istasyon daha önce ziyaret edildiyse, işlemi atla       
            if istasyon in self.ziyaret_edilen: 
                continue
            
            # Şu anki istasyonu ziyaret_edilen kümesine ekle.     
            self.ziyaret_edilen.add(istasyon) 

            # Eğer hedef istasyona ulaşıldıysa, sonucu döndür       
            if istasyon == hedef:   
                return rota, toplam_sure  
        
            # 4. Mevcut istasyonun komşularını işle
            for komsu, sure in istasyon.komsular:
                if komsu not in self.ziyaret_edilen:  
                    """
                    * Yeni toplam süreyi hesapla.
                    * Öncelikli kuyruğa ekleyerek, en kısa sürede ulaşılabilen istasyonları önceliklendir.
                    * Yeni rota listesine bu komşuyu ekleyerek ilerleyen yolları takip et.
                    """
                    yeni_toplam_sure = toplam_sure + sure 
                    heappush(pq, (yeni_toplam_sure, id(komsu), komsu, rota + [komsu])) 
                    
        # Eğer rota bulunamazsa None döndür   
        return None
    
# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 