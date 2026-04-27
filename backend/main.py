import uvicorn
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List

# Импортируем наш почтовый сервис
import mail_service

# --- НАСТРОЙКА БАЗЫ ДАННЫХ ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

Base.metadata.create_all(bind=engine)

# --- ИНИЦИАЛИЗАЦИЯ APP ---
app = FastAPI(title="ToDo & Mail Lab System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- МЕНЕДЖЕР WEBSOCKET (Лабораторная №5) ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Рассылка сообщения 'refresh' всем подключенным браузерам"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass # Соединение могло закрыться

manager = ConnectionManager()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ЭНДПОИНТЫ WEBSOCKET ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Ждем данных (keep-alive)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- ЭНДПОИНТЫ ЗАДАЧ (CRUD) ---

@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.post("/tasks")
async def create_task(title: str, description: str = "", db: Session = Depends(get_db)):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # Лабораторная №5: Уведомляем всех об изменениях
    await manager.broadcast("refresh")
    return new_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    db.delete(task)
    db.commit()
    
    # Лабораторная №5: Уведомляем всех об изменениях
    await manager.broadcast("refresh")
    return {"status": "deleted"}

# --- ЭНДПОИНТЫ ПОЧТЫ (Интеграция с mail_service) ---

@app.post("/send-mail")
async def api_send_mail(to: str, title: str, content: str):
    """Использует SMTP_SSL из mail_service"""
    success = mail_service.send_smtp(title, content, to)
    if success:
        return {"status": "success", "recipient": to}
    else:
        raise HTTPException(status_code=500, detail="Ошибка при отправке через SMTP")

@app.get("/last-received")
async def api_get_last_email():
    """Использует IMAP_SSL из mail_service"""
    return mail_service.get_last_email_imap()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
