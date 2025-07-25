# main.py
from fastapi import FastAPI, Request, Response

app = FastAPI()

# Este es el endpoint que Twilio llamará al inicio de la llamada
@app.post("/voice")
async def voice():
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="Pedro-Neural" language="es-US">
    Hola, bienvenido.
  </Say>
  <Start>
    <Transcription
      statusCallbackUrl="https://apr-production.up.railway.app/transcription-log"
      language="en-US"
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

    print(f"--- Datos completos recibidos de Twilio para Call SID: {form_data.get('CallSid')} ---")
    for key, value in form_data.items():
        print(f"{key}: {value}")
    print("---------------------------------------------------\n")

    # Devuelve un 200 OK
    return Response(content="", status_code=200)