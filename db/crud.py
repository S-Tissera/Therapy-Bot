from sqlalchemy.orm import Session
from db.database import Base
from model.schemas import ChatRequest, ChatResponse
import uuid
from datetime import datetime

# User Operations
async def create_user_session(db: Session) -> str:
    user_id = str(uuid.uuid4())
    db_user = User(user_id=user_id)
    db.add(db_user)
    db.commit()
    return user_id

# Interaction Operations
async def log_interaction(db: Session, data: dict):
    interaction = Interaction(
        user_id=data["user_id"],
        message=data["message"],
        response=data["response"],
        emotion=data["emotion"],
        sarcasm_score=data["sarcasm"],
        context_emotion=data["context"]
    )
    db.add(interaction)
    db.commit()

async def get_user_history(db: Session, user_id: str, limit: int = 3):
    return db.query(Interaction).filter(
        Interaction.user_id == user_id
    ).order_by(
        Interaction.timestamp.desc()
    ).limit(limit).all()