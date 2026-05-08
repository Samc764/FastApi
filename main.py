from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from pathlib import Path
import random

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

preguntas = []


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        name="formulario.html",
        request=request,
        context={"ano_actual": datetime.now().year},
    )


@app.post("/procesar_pregunta", response_class=HTMLResponse)
async def procesar_pregunta(
    request: Request,
    nombre: str = Form(...),
    pregunta: str = Form(...),
):
    respuesta = random.choice([
        "La respuesta es un sí rotundo.",
        "Mejor espera un poco y vuelve a preguntar.",
        "No puedo decidirlo por ti.",
        "Todo apunta a que será favorable.",
        "La energía no es clara aún.",
    ])
    registro = {
        "nombre": nombre,
        "pregunta": pregunta,
        "respuesta": respuesta,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    preguntas.append(registro)

    return templates.TemplateResponse(
        name="resultado.html",
        request=request,
        context={"registro": registro, "ano_actual": datetime.now().year},
    )


@app.get("/historial", response_class=HTMLResponse)
async def historial(request: Request):
    return templates.TemplateResponse(
        name="historial.html",
        request=request,
        context={"preguntas": preguntas, "ano_actual": datetime.now().year},
    )