from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_type = Column(String)
    is_active = Column(Boolean, default=False)
    purchased_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="subscription")