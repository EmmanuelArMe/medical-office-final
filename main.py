from fastapi import FastAPI
from app.routers import cita, especialidad, paciente, medico, consultorio, diagnostico, horario_medico, historial_medico

app = FastAPI(title="Medical Office API")

app.include_router(paciente.router, prefix="/api", tags=["Pacientes"])
app.include_router(cita.router, prefix="/api", tags=["Citas"])
app.include_router(especialidad.router, prefix="/api", tags=["Especialidades"])
app.include_router(medico.router, prefix="/api", tags=["Médicos"])
app.include_router(consultorio.router, prefix="/api", tags=["Consultorios"])
app.include_router(diagnostico.router, prefix="/api", tags=["Diagnósticos"])
app.include_router(horario_medico.router, prefix="/api", tags=["Horarios Médicos"])
app.include_router(historial_medico.router, prefix="/api", tags=["Historial Médico"])