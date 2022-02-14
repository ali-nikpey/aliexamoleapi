from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional
from .. import models, schimas, oauth2



router = APIRouter(
    prefix="/sqlalchemy",
    tags=['Posts']
)


@router.get("/", response_model=List[schimas.VotePost])
def get_alchemy_post(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user), limit: int= 10, skip: int = 0, search: Optional[str] = ""):
    print(get_current_user)

    result = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return result


@router.post("/",  status_code=status.HTTP_201_CREATED, response_model=schimas.PostResponse)
def creat_alchemy_post(post: schimas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    new_alchemy_post = models.Post(user_id=get_current_user.id, **post.dict())
    db.add(new_alchemy_post)
    db.commit()
    db.refresh(new_alchemy_post)

    return new_alchemy_post


@router.get("/{id}", response_model=schimas.VotePost)
def get_alchemy_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    print(get_current_user)

    result = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id of {id} does not exist!!")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alchemy(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post.title)
    print(post.user_id)
    print(current_user.id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id of {id} does not exist!!")

    if post.user_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT, content="post was successfully deleted!!")


@router.put("/{id}")
def update_alchemy(id: int, post: schimas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post1 = post_query.first()

    if not post1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id of {id} does not exist!!")

    if post1.user_id != int(get_current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"date": post_query.first()}

