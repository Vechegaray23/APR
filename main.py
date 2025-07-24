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
    twiml = """
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say language="es-US" voice="es-US-Chirp3-HD-Charon">
    Hola, bienvenido. Por favor, dime lo que desees grabar.
  </Say>

  <Record
    maxLength="120"
    transcribe="true"
    recordingTrack="both_tracks"
    transcribeLanguage="es-US"  />

  <Say language="es-US" voice="es-US-Chirp3-HD-Charon">
    Gracias por tu grabación. Adiós.
  </Say>
</Response>
"""
    return Response(content=twiml, media_type="text/xml")
