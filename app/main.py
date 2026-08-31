"
FastAPI Server Entry Point for AG-SMS
"
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.formula import calculate_activation_energy, dynamic_task_downsizing
from app.models.schema import CognitiveOntologyPayload

app = FastAPI(
    title=Anti-Gravity Success OS (AG-SMS) API,
    version=1.0.0,
    description=Cognitive Ontology Mining & Anti-Friction Execution Engine
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[*],
    allow_credentials=True,
    allow_methods=[*],
    allow_headers=[*],
)

@app.get(/)
def read_root():
    return {status: online, system: Anti-Gravity OS, version: PRD-2026-V1}

@app.post(/api/v1/physics/calculate)
def get_activation_energy(e_base: float, c_f: float, momentum: float):
    e_act = calculate_activation_energy(e_base, c_f, momentum)
    return {e_base: e_base, c_f: c_f, momentum: momentum, e_act: e_act}

@app.post(/api/v1/actions/downsize)
def get_downsized_task(task: str, e_base: float = 8.0, c_f: float = 8.5, momentum: float = 1.0):
    return dynamic_task_downsizing(task, e_base, c_f, momentum)
