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
  <Gather input="speech" timeout="5" speechTimeout="auto" language="es-US" action="/handle_recording">
    <Say language="es-US" voice="es-US-Chirp3-HD-Charon">
      Hola, bienvenido. Por favor, dime lo que desees grabar.
    </Say>
  </Gather>

  <Record
    maxLength="120"
    transcribe="true"
    recordingTrack="both_tracks"
    transcribeLanguage="es-CL"
    action="/process_recording"
  />

  <Say language="es-US" voice="es-US-Chirp3-HD-Charon">
    No he recibido ninguna entrada. Adiós.
  </Say>
</Response>
"""
    return Response(content=twiml, media_type="text/xml")
