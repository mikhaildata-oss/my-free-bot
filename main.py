import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
import httpx
from bootstrap import init_ai_adapter, init_message_repo
from domain.ports import IAIAdapter, IMessageRepository
from domain.entities import Message

app = FastAPI(title="My Free Bot", version="1.0")
ai_adapter: IAIAdapter | None = None
msg_repo: IMessageRepository | None = None

@app.on_event("startup")
async def startup_event():
    global ai_adapter, msg_repo
    logger.info("Bootstrapping bot...")
    ai_adapter = init_ai_adapter()
    msg_repo = init_message_repo()
    if ai_adapter:
        logger.success(f"AI Adapter ready: {ai_adapter.get_model_name()}")
    if msg_repo:
        logger.success("Message Repository ready")

@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "healthy", "ai": ai_adapter.get_model_name() if ai_adapter else "init"}

async def send_telegram_message(chat_id: int, text: str):
    bot_token = os.getenv("BOT_TOKEN", "")
    if not bot_token:
        logger.warning("BOT_TOKEN not set")
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})
            logger.info(f"Sent to TG: {chat_id}")
    except Exception as e:
        logger.error(f"TG send error: {e}")

@app.post("/webhook")
async def webhook(request: Request):
    if not ai_adapter or not msg_repo:
        raise HTTPException(status_code=500, detail="Not initialized")
    try:
        data = await request.json()
        if "message" not in data or "text" not in data.get("message", {}):
            return JSONResponse({"status": "ignored"})
        msg_data = data["message"]
        text = msg_data.get("text", "").strip()
        if not text:
            return JSONResponse({"status": "ignored"})
        user_id = msg_data.get("from", {}).get("id")
        username = msg_data.get("from", {}).get("username", "unknown")
        chat_id = msg_data.get("chat", {}).get("id")
        logger.info(f"WEBHOOK: User={user_id}, Text='{text[:30]}...'")
        
        user_msg = Message(user_id=user_id, text=text, username=username)
        response_text = await ai_adapter.generate_response(user_msg, history=[])
        logger.info(f"AI: {response_text[:50]}...")
        
        # SAVE BOTH USER MSG AND AI RESPONSE
        msg_id = await msg_repo.save(user_id=user_id, username=username, message_text=text, ai_response=response_text)
        logger.info(f"SAVED: ID={msg_id}")
        
        await send_telegram_message(chat_id, response_text)
        return JSONResponse({"status": "ok", "msg_id": msg_id})
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

