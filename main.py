import os
from fastapi import FastAPI, Response

app = FastAPI()

  
@app.get("/health")
async def health():
    print("🩺 /health invocado")
    return {"status":"ok"}

@app.post("/voice")
async def voice():
    print("📞 /voice invocado por Twilio")

    # TwiML que saluda, graba la llamada y pide transcripción
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <!-- 1) Saludo con TTS nativo de Twilio -->
  <Say language="es-US" voice="es-US-Chirp3-HD-Charon">
    Hola, bienvenido. Por favor, dime lo que desees grabar.
  </Say>

  <!-- 2) Graba todo el audio (inbound+outbound) y transcribe -->
  <Record
    maxLength="120"
    transcribe="true"
    recordingTrack="both_tracks"
  />
</Response>
"""
    return Response(content=twiml, media_type="text/xml")
