from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    APP_NAME: str = "PLC-AMR Handshake Test Platform"
    DATABASE_URL: str = "sqlite:///./data/simulator.db"
    REQUEST_VALIDATION_TIMEOUT: int = 3
    START_TIMEOUT: int = 10
    STATION_READY_TIMEOUT: int = 15
    DONE_ACK_TIMEOUT: int = 10
    HEARTBEAT_TIMEOUT: int = 5

class Config:
        env_file = ".env" # (Load variables from .env file if present) -> (.env dosyasý varsa oradaki çevresel deðiþkenleri yükler)

settings = Settings() # (Instantiate settings globally) -> (Ayarlarý global olarak örnekleyerek projenin her yerinden eriþilebilir hale getirir)