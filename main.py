from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.responses import RedirectResponse
from data.dao.dao_hospitales import DaoHospitales
from data.database import database

# Inicialización de la aplicación FastAPI y configuración de plantillas y recursos estáticos
app = FastAPI(debug=True)
templates = Jinja2Templates(directory="templates")
dao_hospitales = DaoHospitales()
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- INICIO ----------------
# Página principal de la aplicación
@app.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nombre": "Hospital"})

# ---------------- HOSPITALES (LISTADO Y FILTRO) ----------------
# Muestra el listado de hospitales y permite filtrar por número de pacientes
@app.get("/hospitales", response_class=HTMLResponse, name="hospitales")
def get_hospitales(request: Request, numero_pacientes: int = None, mensaje: str = None):
    db = database
    if numero_pacientes is not None:
        # Si se pasa el parámetro personas, filtra hospitales con más pacientes que ese número
        hospitales = dao_hospitales.get_by_numero_pacientes(db, numero_pacientes)
    else:
        # Si no, muestra todos los hospitales
        hospitales = dao_hospitales.get_all(db)
    return templates.TemplateResponse("hospitales.html", {"request": request, "hospitales": hospitales, "mensaje": mensaje})

# ---------------- EDITAR HOSPITALES ----------------
# Página para seleccionar hospital a editar (muestra un select con todos)
@app.get("/edithospitales", response_class=HTMLResponse, name="edithospitales")
def get_hospitales_editar(request: Request):
    db = database
    hospitales = dao_hospitales.get_all(db)
    print(hospitales)  # <-- Añade esto
    return templates.TemplateResponse("editarhospitales.html", {"request": request, "hospitales": hospitales})

# Página de edición de un hospital concreto (formulario de edición)
@app.get("/edithospital/{hospital_id}", response_class=HTMLResponse, name="edithospital")
def edithospital(request: Request, hospital_id: str):
    db = database
    hospital = dao_hospitales.get_by_id(db, hospital_id)
    return templates.TemplateResponse("formedithospital.html", {"request": request, "hospital": hospital})

# Procesa el formulario de edición y actualiza el hospital
@app.post("/update_hospital/{hospital_id}", response_class=HTMLResponse)
def update_hospital(request: Request, hospital_id: str, nombre: Annotated[str, Form()], numero_pacientes: Annotated[int, Form()]):
    db = database
    dao_hospitales.update(db, hospital_id, nombre, numero_pacientes)
    mensaje = "Hospital actualizado correctamente."
    hospitales = dao_hospitales.get_all(db)
    return templates.TemplateResponse("hospitales.html", {"request": request, "hospitales": hospitales, "mensaje": mensaje})

# ---------------- BORRAR HOSPITALES ----------------
# Página para mostrar todos los hospitales con opción de borrado
@app.get("/borrarhospitales", response_class=HTMLResponse, name="borrarhospitales")
def borrar_hospitales(request: Request):
    db = database
    hospitales = dao_hospitales.get_all(db)
    return templates.TemplateResponse("borrarhospitales.html", {"request": request, "hospitales": hospitales})

# Borra un hospital por su id (desde enlace)
@app.get("/deletehospital/{hospital_id}", response_class=HTMLResponse, name="deletehospital")
def delete_hospital(request: Request, hospital_id: str):
    db = database
    dao_hospitales.delete(db, hospital_id)
    hospitales = dao_hospitales.get_all(db)
    mensaje = "Hospital borrado correctamente."
    return templates.TemplateResponse("hospitales.html", {"request": request, "hospitales": hospitales, "mensaje": mensaje})

# Borra un hospital por su id (desde formulario)
@app.post("/delhospital", response_class=HTMLResponse)
def del_hospital(request: Request, hospital_id: Annotated[str, Form()]):
    db = database
    dao_hospitales.delete(db, hospital_id)
    hospitales = dao_hospitales.get_all(db)
    mensaje = "Hospital borrado correctamente."
    return templates.TemplateResponse("hospitales.html", {"request": request, "hospitales": hospitales, "mensaje": mensaje})

# ---------------- AÑADIR HOSPITAL ----------------
# Muestra el formulario para añadir un hospital
@app.get("/formaddhospital", response_class=HTMLResponse, name="formaddhospital")
def form_add_hospital(request: Request, mensaje: str = None):
    return templates.TemplateResponse("formaddhospital.html", {"request": request, "mensaje": mensaje})

# Procesa el formulario y añade el hospital a la base de datos
@app.post("/addhospital", response_class=HTMLResponse, name="addhospital")
def add_hospital(request: Request, nombre: Annotated[str, Form()], numero_pacientes: Annotated[int, Form()]):
    db = database
    dao_hospitales.insert(db, nombre, numero_pacientes)
    mensaje = "Hospital añadido correctamente."
    return templates.TemplateResponse("formaddhospital.html", {"request": request, "mensaje": mensaje})
