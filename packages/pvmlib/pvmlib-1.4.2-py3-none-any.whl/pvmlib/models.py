from pydantic import BaseModel
from typing import Dict, Any

class Application(BaseModel):
    name: str
    version: str
    env: str
    kind: str

class Measurement(BaseModel):
    method: str
    elapsedTime: int

class DefaultLogger(BaseModel):
    level: str
    schemaVersion: str
    logType: str
    sourceIP: str
    status: str
    message: str
    logOrigin: str
    timestamp: str
    tracingId: str
    hostname: str
    eventType: str
    application: Application
    measurement: Measurement
    destinationIP: str
    additionalInfo: Dict[str, Any]

    def json(self):
        return super().model_dump_json()