from sqlmodel import SQLModel, create_engine, Session # (Import SQLModel components for database engine and session management) -> (Veritabaný motorunu oluþturmak ve oturumlarý yönetmek için SQLModel bileþenlerini içe aktarýr)
from app.config import settings # (Import global settings to access database URL) -> (Veritabaný baðlantý adresine eriþmek için global ayarlarý içe aktarýr)

# (Create SQLite database engine using the URL from settings) -> (Ayarlar dosyasýndaki URL'yi kullanarak SQLite veritabaný motorunu oluþturur)
sqlite_url = settings.DATABASE_URL
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables(): # (Function to initialize database tables) -> (Modellerde tanýmlanan tablolarý veritabanýnda otomatik olarak oluþturan fonksiyon)
    SQLModel.metadata.create_all(engine)

def get_session(): # (Dependency function to yield a database session for API requests) -> (API istekleri sýrasýnda veritabaný oturumu açan ve iþlem bitince güvenli þekilde kapatan baðýmlýlýk fonksiyonu)
    with Session(engine) as session:
        yield session