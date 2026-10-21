
from fastapi import FastAPI, status

from app.schemas.claim import ClaimCreate, ClaimResponse

app = FastAPI(
    title="ClaimWise AI",
    description="Healthcare claims analytics and risk assessment platform",
    version="0.2.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to ClaimWise AI",
        "status": "running",
        "version": "0.2.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "claimwise-ai"}


@app.post(
    "/api/v1/claims",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_claim(claim: ClaimCreate):
    # Temporary response until database persistence is implemented.
    return ClaimResponse(
        id=1,
        **claim.model_dump(),
    )
