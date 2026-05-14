from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Message
from app.config import settings


router = APIRouter()

connections: dict[int, list[WebSocket]] = {}

@router.websocket("/{room_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: int,
    db: AsyncSession = Depends(get_db),
):
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        return

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("id")

        if not user_id:
            await websocket.close(code=1008)
            return

    except JWTError:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    if room_id not in connections:
        connections[room_id] = []

    connections[room_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            message = Message(
                room_id=room_id,
                content=data,
                sender_id=int(user_id),
            )

            db.add(message)

            await db.commit()
            await db.refresh(message)

            for connection in connections[room_id]:
                await connection.send_json({
                    "message": data,
                    "sender_id": user_id,
                    "room_id": room_id,
                })

    except WebSocketDisconnect:
        connections[room_id].remove(websocket)


@router.get("/chat/{room_id}/history")
async def get_history(
    room_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Message).where(
            Message.room_id == room_id
        )
    )

    messages = result.scalars().all()

    return messages