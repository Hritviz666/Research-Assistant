import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Research Assistant API")


# ── MODELS ────────────────────────────────────────────────

class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    topic: str
    report: str

class CompareRequest(BaseModel):
    topic1: str
    topic2: str

class CompareResponse(BaseModel):
    topic1: str
    topic2: str
    report: str

class PlannerRequest(BaseModel):
    query: str

class PlannerResponse(BaseModel):
    query: str
    plan: str

class StructuredReportRequest(BaseModel):
    query: str

class StructuredReportResponse(BaseModel):
    query: str
    report: str


# ── ROUTES ────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "Research Assistant API is running"}


@app.post("/research", response_model=ResearchResponse)
def run_research(request: ResearchRequest):
    if not request.topic or len(request.topic.strip()) < 3:
        raise HTTPException(status_code=400, detail="Topic is too short.")
    try:
        from research_crew import build_crew
        crew = build_crew(request.topic)
        result = crew.kickoff()
        return ResearchResponse(topic=request.topic, report=str(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare", response_model=CompareResponse)
def run_comparison(request: CompareRequest):
    if not request.topic1 or not request.topic2:
        raise HTTPException(status_code=400, detail="Both topics are required.")
    if len(request.topic1.strip()) < 3 or len(request.topic2.strip()) < 3:
        raise HTTPException(status_code=400, detail="Topics are too short.")
    try:
        from research_crew import build_comparison_crew
        crew = build_comparison_crew(request.topic1, request.topic2)
        result = crew.kickoff()
        return CompareResponse(
            topic1=request.topic1,
            topic2=request.topic2,
            report=str(result)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/plan", response_model=PlannerResponse)
def run_planner(request: PlannerRequest):
    if not request.query or len(request.query.strip()) < 3:
        raise HTTPException(status_code=400, detail="Query is too short.")
    try:
        from research_crew import build_planner_crew
        crew = build_planner_crew(request.query)
        result = crew.kickoff()
        return PlannerResponse(query=request.query, plan=str(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/structured-report", response_model=StructuredReportResponse)
def run_structured_report(request: StructuredReportRequest):
    if not request.query or len(request.query.strip()) < 3:
        raise HTTPException(status_code=400, detail="Query is too short.")
    try:
        from research_crew import build_structured_report_crew
        crew = build_structured_report_crew(request.query)
        result = crew.kickoff()
        return StructuredReportResponse(query=request.query, report=str(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))