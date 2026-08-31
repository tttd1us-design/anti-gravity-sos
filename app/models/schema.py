"
Pydantic Schemas for Cognitive Ontology (RFC 8259 Compliant)
"
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

class IdentityBaseline(BaseModel):
    core_statement: str
    rigidity_score: float = Field(default=0.8, ge=0.0, le=1.0)

class DesireNode(BaseModel):
    desire_id: str = Field(default_factory=lambda: str(uuid4()))
    layer: int = Field(ge=1, le=5)
    statement: str
    emotional_anchor: str
    priority_weight: float = Field(default=0.9, ge=0.0, le=1.0)

class FrictionNode(BaseModel):
    friction_id: str = Field(default_factory=lambda: str(uuid4()))
    target_desire_id: str
    fear_type: str = Field(description=PERFECTIONISM | CRITICISM_FEAR | LOSS_OF_CONTROL | IMPOSTOR_SYNDROME | OVERWHELM)
    trigger_condition: str
    cognitive_distortion: str
    friction_coefficient: float = Field(ge=1.0, le=10.0)
    subconscious_payoff: str

class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    relationship: str = Field(description=DRIVES | BLOCKED_BY | NEUTRALIZES)
    intensity: float = Field(default=0.8, ge=0.0, le=1.0)

class CognitiveOntologyPayload(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str = Field(default=user_default_01)
    identity_baseline: IdentityBaseline
    desires: List[DesireNode]
    frictions: List[FrictionNode]
    graph_edges: List[GraphEdge]
