
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.claim import Claim
from app.schemas.claim import ClaimCreate, ClaimResponse

app = FastAPI(
    title="ClaimWise AI",
    description="Healthcare claims analytics and risk assessment platform",
    version="0.3.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to ClaimWise AI",
        "status": "running",
        "version": "0.3.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "claimwise-ai"}


@app.post(
    "/api/v1/claims",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_claim(
    claim_data: ClaimCreate,
    db: Session = Depends(get_db),
):
    claim = Claim(**claim_data.model_dump())

    try:
        db.add(claim)
        db.commit()
        db.refresh(claim)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A claim with this reference already exists.",
        ) from exc

    return claim


@app.get(
    "/api/v1/claims",
    response_model=list[ClaimResponse],
)
def list_claims(db: Session = Depends(get_db)):
    statement = select(Claim).order_by(Claim.id)
    claims = db.scalars(statement).all()
    return claims


@app.get(
    "/api/v1/claims/{claim_id}",
    response_model=ClaimResponse,
)
def get_claim(
    claim_id: int,
    db: Session = Depends(get_db),
):
    claim = db.get(Claim, claim_id)

    if claim is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found.",
        )

    return claim
