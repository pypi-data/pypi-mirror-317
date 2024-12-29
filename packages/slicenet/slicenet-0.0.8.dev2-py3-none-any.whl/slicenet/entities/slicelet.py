import uuid
from slicenet.utils.slicenetlogger import slicenetLogger as logger
from slicenet.entities.base import Base

class Slicelet(Base):
    def __init__(self, name: str, duration: float, service_id: uuid.UUID):
        super().__init__()
        self.id = uuid.uuid4()
        self.name = name
        self.slaViolation = False
        self.delaySeconds = 0 # We assume no delay initially
        self.duration = duration
        self.service_id = service_id
        self.initRandomDelaySecs = 0 # to be filled as part of scheduling to factor randomness
    
    def getName(self):
        return self.name
    
