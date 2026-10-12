from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class RobotCreate(BaseModel):
    robot_code: str
    name: str
    ip_address: str
    is_active: bool = True

class RobotResponse(RobotCreate):
    id: int
    
    class Config:
        from_attributes = True

class HandshakeCreate(BaseModel):
    robot_code: str
    station_id: str
    task_type: str

class HandshakeResponse(HandshakeCreate):
    id: int
    status: str = "PENDING"
    
    class Config:
        from_attributes = True

class HandshakeUpdate(BaseModel): # (Pydantic schema for updating handshake session status) -> (El sýkýþma durumunu güncellerken kullanýlacak veri kalýbý)
    status: Optional[str] = None
class EventLogCreate(BaseModel): # (Pydantic schema for creating a new log entry) -> (Yeni bir log kaydý oluþturulurken kullanýlacak veri kalýbý)
    level: str = "INFO"
    message: str

class EventLogResponse(EventLogCreate): # (Pydantic schema for returning log entries) -> (Log kayýtlarýný dýþ dünyaya dönerken kullanýlacak þema)
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True



