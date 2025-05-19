from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import cita, especialidad, paciente, medico, consultorio, diagnostico, horario_medico, historial_medico, examen, factura, pago, medicamento, medicamento_recetado

load_dotenv()

app = FastAPI(
    title="Medical Office API",
    version="1.0.0",
    description="API for managing medical office operations",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(paciente.router, prefix="/api", tags=["Pacientes"])
app.include_router(cita.router, prefix="/api", tags=["Citas"])
app.include_router(especialidad.router, prefix="/api", tags=["Especialidades"])
app.include_router(medico.router, prefix="/api", tags=["Médicos"])
app.include_router(consultorio.router, prefix="/api", tags=["Consultorios"])
app.include_router(diagnostico.router, prefix="/api", tags=["Diagnósticos"])
app.include_router(horario_medico.router, prefix="/api", tags=["Horarios Médicos"])
app.include_router(historial_medico.router, prefix="/api", tags=["Historial Médico"])
app.include_router(examen.router, prefix="/api", tags=["Exámenes"])
app.include_router(factura.router, prefix="/api", tags=["Facturas"])
app.include_router(pago.router, prefix="/api", tags=["Pagos"])
app.include_router(medicamento.router, prefix="/api", tags=["Medicamentos"])
app.include_router(medicamento_recetado.router, prefix="/api", tags=["Medicamentos Recetados"])