from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import controllers, schemas, database

router = APIRouter(prefix="/reviews", tags=["Product Reviews"])

@router.get("/", response_model=list[schemas.ProductReview])
def list_reviews(db: Session = Depends(database.get_db)):
    return controllers.reviews.get_reviews(db)

@router.get("/{review_id}", response_model=schemas.ProductReview)
def read_review(review_id: int, db: Session = Depends(database.get_db)):
    db_review = controllers.reviews.get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@router.post("/", response_model=schemas.ProductReview)
def create_review(review: schemas.ProductReviewCreate, db: Session = Depends(database.get_db)):
    return controllers.reviews.create_review(db, review)

@router.put("/{review_id}", response_model=schemas.ProductReview)
def update_review(review_id: int, review: schemas.ProductReviewCreate, db: Session = Depends(database.get_db)):
    return controllers.reviews.update_review(db, review_id, review)

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(database.get_db)):
    return controllers.reviews.delete_review(db, review_id)
