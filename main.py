# main.py
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/voice")
async def voice():
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <!-- 1) Saludo inicial con TTS en español -->
  <Say voice="Andres-Generative" language="es-MX">
    Hola, por favor dime lo que quieras decir y lo transcribiré.
  </Say>

  <!-- 2) Recoge la voz del usuario y envía la transcripción a /transcription -->
  <Gather
    input="speech"
    language="es-US"
    speechTimeout="auto"
    action="/transcription"
    method="POST"
  />
  
  <!-- 3) Si no se detecta voz, se despide -->
  <Say voice="Andres-Generative" language="es-MX">
    No te escuché bien. Adiós.
  </Say>
  <Hangup/>
</Response>"""
    return Response(content=twiml, media_type="text/xml")


@app.post("/transcription")
async def transcription(request: Request):
    form = await request.form()
    call_sid = form.get("CallSid", "unknown")
    text = form.get("SpeechResult", "")
    print(f"[{call_sid}] Transcripción final: {text}")

    # Respuesta final: te agradece y cuelga
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice" language="es-CL">
    Gracias, adiós.
  </Say>
  <Hangup/>
</Response>"""
    return Response(content=twiml, media_type="text/xml")
