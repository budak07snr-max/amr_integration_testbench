from datetime import datetime # (Import datetime for timestamp tracking) -> (Olaylarýn ve iþlemlerin ne zaman yapýldýðýný takip etmek için tarih/saat modülünü içe aktarýr)
from typing import Optional # (Import Optional for nullable database fields) -> (Veritabanýnda boþ býrakýlabilen, yani deðer olmama ihtimali olan alanlar için Optional sýnýfýný içe aktarýr)
from sqlmodel import SQLModel, Field # (Import SQLModel and Field for database table definitions) -> (Veritabaný tablolarýný ve sütunlarýný Python sýnýflarý olarak kolayca tanýmlamak için SQLModel ve Field sýnýflarýný içe aktarýr)



class Robot(SQLModel, table=True): # (Define the Robot database table model) -> (Sistemdeki AMR robotlarýnýn veritabanýnda saklanacaðý 'robots' tablosunun model sýnýfýný tanýmlar)
    id: Optional[int] = Field(default=None, primary_key=True) # (Primary key identifier for the robot) -> (Her robotu benzersiz þekilde ayýran birincil anahtar ID alaný)
    robot_code: str = Field(index=True, unique=True) # (Unique code identifier for the robot, e.g., AMR-01) -> (Robotun sistemdeki benzersiz kodu, örneðin AMR-01; hýzlý arama için indexlenmiþtir)
    name: str # (Human-readable name of the robot) -> (Robotun insan tarafýndan okunabilir adý veya açýklamasý)
    ip_address: str # (IP address of the robot for network communication) -> (Robotun að üzerinden haberleþeceði IP adresi)
    is_active: bool = Field(default=True) # (Status flag indicating if the robot is active in the system) -> (Robotun sistemde aktif olup olmadýðýný belirten durum bayraðý)
    created_at: datetime = Field(default_factory=datetime.utcnow) # (Timestamp when the robot record was created) -> (Robot kaydýnýn sisteme eklendiði tarih ve saat bilgisi)


class HandshakeSession(SQLModel, table=True): # (Define the HandshakeSession database table model) -> (PLC ve AMR arasýndaki anlýk görev, konum ve el sýkýþma adýmlarýný takip eden veritabaný tablosunu tanýmlar)
    id: Optional[int] = Field(default=None, primary_key=True) # (Primary key for the session) -> (Oturum için benzersiz birincil anahtar ID alaný)
    robot_code: str = Field(index=True) # (Associated robot code for this session) -> (Bu el sýkýþma oturumunun hangi robota ait olduðunu belirten kod)
    session_id: str = Field(index=True, unique=True) # (Unique tracking identifier for the handshake task) -> (Görev oturumunu benzersiz þekilde takip etmek için kullanýlan ID)
    current_state: str = Field(default="IDLE") # (Current state of the handshake process, e.g., IDLE, MOVING, READY) -> (El sýkýþma sürecinin anlýk durumu; örn: IDLE, MOVING, READY)
    target_station: str # (Target station identifier for the AMR) -> (Robotun gitmesi gereken hedef istasyon bilgisi)
    error_code: Optional[str] = Field(default=None) # (Error code if any failure occurs during handshake) -> (El sýkýþma veya hareket sýrasýnda hata olursa saklanacak hata kodu)
    updated_at: datetime = Field(default_factory=datetime.utcnow) # (Timestamp of the last state update) -> (Durumun en son güncellendiði tarih ve saat bilgisi)


class EventLog(SQLModel, table=True): # (Define the EventLog database table model) -> (Sistemde gerçekleþen tüm olaylarý, istekleri ve hata loglarýný veritabanýnda saklayan tablo modelini tanýmlar)
    id: Optional[int] = Field(default=None, primary_key=True) # (Primary key identifier for the log) -> (Log kaydý için benzersiz birincil anahtar ID alaný)
    level: str = Field(default="INFO") # (Log severity level, e.g., INFO, WARNING, ERROR) -> (Log seviyesi; örneðin bilgi (INFO), uyarý (WARNING) veya hata (ERROR))
    message: str # (Detailed description of the event or communication message) -> (Olayýn veya haberleþme mesajýnýn detaylý açýklamasý)
    robot_code: Optional[str] = Field(default=None, index=True) # (Associated robot code if applicable) -> (Ýlgili log hangi robota aitse onun kodu, isteðe baðlý)
    timestamp: datetime = Field(default_factory=datetime.utcnow) # (Timestamp when the event occurred) -> (Olayýn gerçekleþtiði tarih ve saat bilgisi)



class EventLog(SQLModel, table=True): # (Database model for storing system event and handshake logs) -> (Sistem olaylarýný ve log kayýtlarýný tutacak veritabaný modeli)
    __tablename__ = "eventlogs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    level: str = "INFO" # (Log level like INFO, WARNING, ERROR) -> (Log seviyesi: INFO, WARNING, ERROR vb.)
    message: str # (Log description message) -> (Log açýklama mesajý)
    created_at: datetime = Field(default_factory=datetime.utcnow) # (Timestamp of the event) -> (Olayýn gerçekleþtiði zaman damgasý)