
# main.py
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.post("/voice")
async def voice():
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice" language="es-CL">
    Hola, bienvenido. Por favor, dime tu nombre.
  </Say>
  <Record
    maxLength="10"
    transcribe="true"
    transcribeLanguage="es-US"  action="https://apr-production.up.railway.app/process-name" />
</Response>"""
    return Response(content=twiml, media_type="text/xml")

@app.post("/process-name")
async def process_name(request: Request):
    form_data = await request.form()
    
    recording_url = form_data.get("RecordingUrl")
    transcription_text = form_data.get("TranscriptionText") # ¡Aquí obtienes la transcripción!
    call_sid = form_data.get("CallSid")

    print(f"--- Grabación Finalizada (Call SID: {call_sid}) ---")
    print(f"URL Grabación: {recording_url}")
    if transcription_text:
        print(f"Transcripción: {transcription_text}")
    else:
        print("Transcripción no disponible o error.")
    print("---------------------------------------------------\n")

    # Ahora, puedes responder con más TwiML para continuar la llamada
    if transcription_text and "juan" in transcription_text.lower():
        next_twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice" language="es-CL">
    Hola Juan, ¿en qué más puedo ayudarte hoy?
  </Say>
</Response>"""
    else:
        next_twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice" language="es-CL">
    Gracias por tu respuesta. Dime, ¿cuál es el motivo de tu llamada?
  </Say>
  <Record
    maxLength="20"
    transcribe="true"
    transcribeLanguage="es-US"
    action="https://apr-production.up.railway.app/process-reason"
  />
</Response>"""
        
    return Response(content=next_twiml, media_type="text/xml")

# Puedes tener más endpoints para cada paso de la conversación
@app.post("/process-reason")
async def process_reason(request: Request):
    form_data = await request.form()
    transcription_text = form_data.get("TranscriptionText")
    call_sid = form_data.get("CallSid")

    print(f"--- Motivo de Llamada (Call SID: {call_sid}) ---")
    if transcription_text:
        print(f"Motivo: {transcription_text}")
    print("---------------------------------------------------\n")

    final_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice" language="es-CL">
    Gracias. Hemos registrado tu solicitud. Adiós.
  </Say>
  <Hangup/>
</Response>"""
    return Response(content=final_twiml, media_type="text/xml")