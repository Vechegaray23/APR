# main.py
from fastapi import FastAPI, Request, Response

app = FastAPI()
@app.post("/voice")
async def voice():
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice" language="es-CL">
    Hola, bienvenido. Por favor, dime lo que desees grabar.
  </Say>
  <Record
    maxLength="120"
    transcribe="true"
    transcribeLanguage="es-CL"
    recordingTrack="both_tracks"
  />
</Response>"""
    return Response(content=twiml, media_type="text/xml")
