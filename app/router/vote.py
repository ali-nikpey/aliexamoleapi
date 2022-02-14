from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import schimas, database, models, oauth2
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/vote",
    tags=['votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schimas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == models.Votes.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post dose not exist")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_query = vote_query.first()
    if vote.dir == 1:
        if found_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"you voted this post before!!")
        new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        if not found_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id of {vote.post_id} not found")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted message"}
