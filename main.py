# main.py
from fastapi import FastAPI, Request, Response

app = FastAPI()

# Este es el endpoint que Twilio llamará al inicio de la llamada
@app.post("/voice")
async def voice():
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice" language="es-US">
    Hola, bienvenido.
  </Say>
  <Start>
    <Transcription
      statusCallbackUrl="https://apr-production.up.railway.app/transcription-log"
      language="es-US"
    />
  </Start>
  <Pause length="8" /> <Say voice="alice" language="es-US">
    Hemos terminado de transcribir. Gracias.
  </Say>
</Response>"""
    return Response(content=twiml, media_type="text/xml")

# Este es el endpoint que recibirá las transcripciones en tiempo real
# Lo hemos llamado '/transcription-log' para reflejar su propósito de solo loguear
@app.post("/transcription-log")
async def transcription_log(request: Request):
    form_data = await request.form()
    
    # Extraemos solo lo que nos interesa ver
    transcription_status = form_data.get("TranscriptionStatus")
    transcription_text = form_data.get("TranscriptionText")
    call_sid = form_data.get("CallSid")
    
    # Imprimimos en la consola/logs
    print(f"--- Transcripción en vivo para Call SID: {call_sid} ---")
    print(f"Estado: {transcription_status}")
    if transcription_text: # Solo imprimimos el texto si existe
        print(f"Texto: {transcription_text}")
    print("---------------------------------------------------\n") # Espacio para mayor claridad en los logs

    # Siempre devuelve un 200 OK
    return Response(content="", status_code=200)