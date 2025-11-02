from sqlalchemy.orm import Session
from app.models import ProductReview
from app import schemas

def get_reviews(db: Session):
    return db.query(ProductReview).all()

def get_review(db: Session, review_id: int):
    return db.query(ProductReview).filter(ProductReview.review_id == review_id).first()

def create_review(db: Session, review: schemas.ProductReviewCreate):
    db_review = ProductReview(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, review_id: int, updated: schemas.ProductReviewCreate):
    db_review = get_review(db, review_id)
    if db_review:
        for key, value in updated.dict().items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int):
    db_review = get_review(db, review_id)
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review
