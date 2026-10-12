from app.schemas import EventLogCreate, EventLogResponse # (Import EventLog Pydantic schemas) -> (Log oluþturma ve yanýt þemalarýný içe aktarýr)
from app.domain.models import EventLog # (Import EventLog database model) -> (EventLog veritabaný modelini içe aktarýr)
from typing import List

from app.schemas import HandshakeUpdate # (Import Pydantic schema for handshake update requests) -> (El sýkýþma durumu güncelleme þemasýný içe aktarýr)

from app.schemas import HandshakeCreate, HandshakeResponse # (Import Pydantic schemas for handshake session creation and response) -> (El sýkýþma oturumu oluþturma ve yanýt þemalarýný içe aktarýr)
from app.domain.models import HandshakeSession # (Import HandshakeSession database model) -> (Veritabaný tablosu ile eþleþen el sýkýþma oturum modelini içe aktarýr)
from fastapi import FastAPI, Depends, HTTPException # (Import core FastAPI modules for web API and dependency injection) -> (Web API ve baðýmlýlýk yönetimi için temel FastAPI modüllerini içe aktarýr)
from app.config import settings # (Import global settings instance) -> (Konfigürasyon ayarlarýna ve proje adýna eriþmek için global settings nesnesini içe aktarýr)
from app.schemas import RobotCreate, RobotResponse # (Import Pydantic request and response schemas for robots) -> (Robot ekleme ve listeleme iþlemleri için Pydantic veri þemalarýný içe aktarýr)
from app.domain.models import Robot # (Import Robot database model class) -> (Veritabaný tablosu ile eþleþen Robot model sýnýfýný içe aktarýr)
from app.domain.database import get_session # (Import database session dependency generator) -> (Veritabaný oturumunu güvenli þekilde açýp kapamak için baðýmlýlýk fonksiyonunu içe aktarýr)
from sqlmodel import Session # (Import Session class for type hinting database sessions) -> (Veritabaný oturum nesnelerinin veri tipini belirtmek için Session sýnýfýný içe aktarýr)



app = FastAPI(title=settings.APP_NAME, version="1.0.0") # (Initialize FastAPI application instance) -> (FastAPI web uygulamasýný baþlatarak sunucu ana nesnesini oluþturur)
from app.domain.database import create_db_and_tables # (Import database initialization function) -> (Veritabaný tablolarýný otomatik oluþturmak için ilgili fonksiyonu içe aktarýr)

@app.on_event("startup") # (Define lifespan/startup event decorator for FastAPI) -> (FastAPI sunucusu ilk açýldýðý anda çalýþacak olan baþlangýç olayýný yakalayan dekoratördür)
def on_startup(): # (Function executed on application startup) -> (Uygulama ayaða kalkarken çalýþtýrýlacak olan fonksiyondur)
    create_db_and_tables() # (Trigger database and table creation) -> (Veritabaný ve tablolarýn var olup olmadýðýný kontrol eder, yoksa sýfýrdan oluþturur)

@app.get("/") # (Define a GET HTTP endpoint for the root URL) -> (Kök URL'ye (/) gelen GET isteklerini karþýlayan API uç noktasýný tanýmlayan dekoratör)
def read_root(): # (Root endpoint function returning a welcome dictionary message) -> (Sunucunun çalýþtýðýný belirten bir sözlük (dictionary) mesajý döndüren ana fonksiyon)
    return {"message": "PLC-AMR Handshake Test Platform is running successfully!"} # (Return a JSON response containing status message) -> (Dýþ dünyaya JSON formatýnda durum mesajý döndürür)

@app.post("/robots/", response_model=RobotResponse) # (Define a POST endpoint to create a new robot) -> (Yeni robot kaydý oluþturan POST uç noktasý)
def create_robot(robot: RobotCreate, session: Session = Depends(get_session)): # (Endpoint function) -> (Gelen veriyi ve oturumu alan fonksiyon)
    db_robot = Robot(**robot.model_dump()) # (Convert Pydantic model to dictionary and initialize Robot object) -> (Pydantic þemasýný sözlüðe çevirip SQLModel robot nesnesine dönüþtürür)
    session.add(db_robot) # (Add robot to session) -> (Robotu oturuma ekler)
    session.commit() # (Commit to database) -> (Veritabanýna kalýcý olarak kaydeder)
    session.refresh(db_robot) # (Refresh instance) -> (ID ve tarih alanlarýný günceller)
    return db_robot # (Return saved robot) -> (Kaydedilen robotu döndürür)
from typing import List # (Import List type hinting for returning multiple records) -> (Birden fazla robot nesnesini liste olarak döndürebilmek için tip tanýmýný içe aktarýr)

@app.get("/robots/", response_model=List[RobotResponse]) # (Define a GET endpoint to fetch all registered robots) -> (Sistemdeki tüm robotlarý listeleyen GET uç noktasýný tanýmlar)
def get_robots(session: Session = Depends(get_session)): # (Endpoint function to retrieve robots using database session) -> (Veritabaný oturumunu kullanarak robotlarý çekecek olan fonksiyonu tanýmlar)
     return session.query(Robot).all() # (Query all robot records from database and return as list) -> (Veritabanýndaki robot tablosundan tüm kayýtlarý sorgular ve liste olarak dýþarýya döndürür)
import uuid # (Import uuid for generating unique session IDs) -> (Benzersiz oturum ID'leri üretmek için uuid kütüphanesini içe aktarýr)

@app.post("/handshakes/", response_model=HandshakeResponse)
def start_handshake(handshake: HandshakeCreate, session: Session = Depends(get_session)):
    import uuid
    db_handshake = HandshakeSession(
        robot_code=handshake.robot_code,
        target_station=handshake.station_id,
        session_id=f"SES-{str(uuid.uuid4())[:8].upper()}",
        current_state="IDLE",
        error_code=0
    )
    session.add(db_handshake)
    session.commit()
    session.refresh(db_handshake)
    
    # Dýþ dünyaya dönerken þemanýn beklediði alanlarý eþleyerek dönüyoruz
    return {
        "id": db_handshake.id,
        "robot_code": db_handshake.robot_code,
        "station_id": db_handshake.target_station,
        "task_type": "TRANSPORT",
        "status": "PENDING"
    }
@app.get("/handshakes/", response_model=List[HandshakeResponse]) # (Define a GET endpoint to fetch all handshake sessions) -> (Tüm el sýkýþma oturumlarýný listeleyen GET uç noktasýný tanýmlar)
def get_handshakes(session: Session = Depends(get_session)): # (Endpoint function to retrieve all handshake sessions) -> (Veritabanýndaki el sýkýþma kayýtlarýný çeken fonksiyon)
 return session.query(HandshakeSession).all() # (Query all handshake session records from database and return as list) -> (Veritabanýndaki el sýkýþma tablosundan tüm kayýtlarý sorgular ve liste olarak döndürür)

 @app.patch("/handshakes/{handshake_id}", response_model=HandshakeResponse) # (Define a PATCH endpoint to update a handshake session status) -> (Bir el sýkýþma oturumunun durumunu güncelleyen PATCH uç noktasýný tanýmlar)
 def update_handshake(handshake_id: int, handshake_update: HandshakeUpdate, session: Session = Depends(get_session)): # (Endpoint function to update handshake status) -> (Oturum ID'sini ve güncellenecek veriyi alarak iþlemi yapan fonksiyon)
    handshake = session.get(HandshakeSession, handshake_id) # (Find handshake session by ID) -> (Veritabanýndan ID'ye göre el sýkýþma oturumunu arar)
    if not handshake: # (Check if session exists) -> (Oturum bulunamadýysa hata fýrlatýr)
        raise HTTPException(status_code=404, detail="Handshake session not found")
    
    update_data = handshake_update.model_dump(exclude_unset=True) # (Get only provided update fields) -> (Sadece güncellenmek istenen alanlarý sözlüðe çevirir)
    for key, value in update_data.items():
        setattr(handshake, key, value) # (Update fields dynamically) -> (Ýlgili alanlarý günceller)
        
    session.add(handshake)
    session.commit()
    session.session.refresh(handshake) if hasattr(session, "session") else session.refresh(handshake) # (Refresh database instance) -> (Veritabaný kaydýný tazeler)
    return handshake # (Return updated handshake session) -> (Güncellenen oturumu dýþ dünyaya döndürür)

@app.post("/logs/", response_model=EventLogResponse) # (Define a POST endpoint to create a new system log) -> (Yeni bir sistem logu oluþturan POST uç noktasýný tanýmlar)
def create_log(log: EventLogCreate, session: Session = Depends(get_session)): # (Endpoint function to save a log entry) -> (Gelen log verisini veritabanýna kaydeden fonksiyon)
    db_log = EventLog(**log.model_dump())
    session.add(db_log)
    session.commit()
    session.refresh(db_log)
    return db_log

@app.get("/logs/", response_model=List[EventLogResponse]) # (Define a GET endpoint to fetch all system logs) -> (Tüm sistem loglarýný listeleyen GET uç noktasýný tanýmlar)
def get_logs(session: Session = Depends(get_session)): # (Endpoint function to retrieve all log entries) -> (Veritabanýndaki tüm log kayýtlarýný çeken fonksiyon)
    return session.query(EventLog).all()















