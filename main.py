# main.py
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/voice")
async def voice():
    # Asegúrate de usar una voz soportada (p.ej. "alice") 
    # y un código de idioma compatible (p.ej. "es-MX" o "es-ES").
    # Además, incluimos un prompt DENTRO del Gather para evitar que Twilio
    # cuelgue esperando input sin indicar nada.
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Gather
    input="speech"
    language="es-MX"
    speechTimeout="auto"
    action="https://<TU_DOMINIO>.railway.app/transcription"
    method="POST">
    <Say voice="alice" language="es-MX">
      Hola, por favor dime lo que quieras que transcriba.
    </Say>
  </Gather>

  <!-- Si no detecta voz en el Gather -->
  <Say voice="alice" language="es-MX">
    No te escuché bien. Adiós.
  </Say>
  <Hangup/>
</Response>"""
    return Response(content=twiml, media_type="text/xml")


@app.post("/transcription")
async def transcription(request: Request):
    form = await request.form()
    call_sid = form.get("CallSid", "unknown")
    speech = form.get("SpeechResult", "")
    confidence = form.get("Confidence", "")
    # Aquí ves la transcripción en los logs de FastAPI / Railway:
    print(f"[{call_sid}] Transcripción: “{speech}”  (confianza: {confidence})")

    # Cuelga la llamada con un breve mensaje
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice" language="es-MX">
    Gracias, adiós.
  </Say>
  <Hangup/>
</Response>"""
    return Response(content=twiml, media_type="text/xml")
