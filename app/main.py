from fastapi import FastAPI
from pydantic import BaseModel


class Message(BaseModel):
    content: str


app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'ChatBot Active'}

@app.post('/send_message/')
async def send_message(message: Message):
    return {
        'status': 200,
        'result': message.content[::-1],
        'extra': 'Hello, Mans',
    }
